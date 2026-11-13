# converters.py
# All the file conversion logic lives here. No GUI code.

import os


def detect_format(path):
    """Return the file's format in uppercase, like 'PDF' or 'JPG'."""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    if ext == "jpeg":
        ext = "jpg"  # treat .jpeg and .jpg as the same thing
    return ext.upper()


def convert_image(src, dest, target):
    """Convert an image to 'JPG' or 'PNG' and save it at dest."""
    from PIL import Image
    from pillow_heif import register_heif_opener
    register_heif_opener()
    img = Image.open(src)
    if target == "JPG":
        img = img.convert("RGB")  # JPG can't store transparency
        img.save(dest, "JPEG", quality=95)
    else:
        img.save(dest, "PNG")


def txt_to_docx(src, dest):
    """Turn a plain text file into a Word document."""
    from docx import Document
    with open(src, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)  # one paragraph per line
    doc.save(dest)


def txt_to_pdf(src, dest):
    """Turn a plain text file into a PDF."""
    from fpdf import FPDF
    with open(src, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    # The built-in PDF font only knows basic Latin characters
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 7, text)
    pdf.output(dest)


def pdf_to_docx(src, dest):
    """Convert a PDF into an editable Word document."""
    from pdf2docx import Converter
    cv = Converter(src)
    try:
        cv.convert(dest)
    finally:
        cv.close()  # always release the file, even if it fails


def docx_to_pdf(src, dest):
    """Convert a Word document to PDF. Needs Microsoft Word installed."""
    from docx2pdf import convert
    if not os.path.exists("/Applications/Microsoft Word.app"):
        raise RuntimeError("DOCX to PDF needs Microsoft Word installed on this Mac.")
    convert(src, dest)


# Every supported (from, to) pair and the function that handles it
CONVERSIONS = {
    ("JPG", "PNG"): lambda s, d: convert_image(s, d, "PNG"),
    ("PNG", "JPG"): lambda s, d: convert_image(s, d, "JPG"),
    ("TXT", "PDF"): txt_to_pdf,
    ("TXT", "DOCX"): txt_to_docx,
    ("PDF", "DOCX"): pdf_to_docx,
    ("DOCX", "PDF"): docx_to_pdf,
    ("HEIC", "JPG"): lambda s, d: convert_image(s, d, "JPG"),
    ("HEIC", "PNG"): lambda s, d: convert_image(s, d, "PNG"),
}


def supported_targets(source):
    """List the formats a file of this type can be converted into."""
    return [to for (frm, to) in CONVERSIONS if frm == source]


def convert_file(src, dest, target):
    """Convert src into the target format. Raises an error if it fails."""
    source = detect_format(src)
    func = CONVERSIONS.get((source, target))
    if func is None:
        raise ValueError(f"Can't convert {source} to {target}.")
    func(src, dest)
    # Never claim success unless the output file really exists
    if not os.path.exists(dest):
        raise RuntimeError("Conversion finished but no file was created.")