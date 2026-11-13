# FileForge

A small Mac desktop file converter. Click a slice of the orange, pick a file, and it converts to that format.

## Supported conversions

- JPG ↔ PNG
- HEIC → JPG / PNG
- TXT → PDF / DOCX
- PDF → DOCX
- DOCX → PDF (needs Microsoft Word installed)

## Run it

```bash
git clone https://github.com/Zahid-Attahi/FileForge.git
cd FileForge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Build the Mac app

```bash
pip install pyinstaller
pyinstaller --windowed --name FileForge --collect-all pillow_heif --collect-all pdf2docx --collect-all docx --collect-all docx2pdf --collect-all fpdf main.py
```

The app lands in `dist/FileForge.app`. It's unsigned, so the first time, right-click it and choose **Open**.

## Files

- `main.py`: the window and click handling
- `orange.py`: draws the clickable orange
- `converters.py`: all the conversion logic

Built with Python, Tkinter, Pillow, python-docx, fpdf2, pdf2docx and docx2pdf.