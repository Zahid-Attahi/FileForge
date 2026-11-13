import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import converters
from orange import draw_segment, BG

root = tk.Tk()
root.title("FileForge")
root.geometry("460x640")
root.configure(bg=BG)
root.resizable(False, False)

title = tk.Label(root, text="FileForge", bg=BG, fg="#2B2B2B",
                 font=("Helvetica", 28, "bold"))
title.pack(pady=(24, 0))

status = tk.Label(root, text="", bg=BG, fg="#2B2B2B", font=("Helvetica", 14))
status.pack()

busy = False


def finish(ok, msg):
    global busy
    busy = False
    status.config(text="")
    if ok:
        messagebox.showinfo("Done", msg)
    else:
        messagebox.showerror("Conversion failed", msg)


def run_conversion(path, dest, name):
    try:
        converters.convert_file(path, dest, name)
        root.after(0, lambda: finish(True, f"Saved:\n{dest}"))
    except Exception as e:
        err = str(e)
        root.after(0, lambda: finish(False, err))


def on_segment_click(name):
    global busy
    if busy:
        return

    path = filedialog.askopenfilename(
        title=f"Pick a file to convert to {name}",
               filetypes=[("Supported files", "*.pdf *.docx *.jpg *.jpeg *.png *.txt *.heic")],
    )
    if not path:
        return

    source = converters.detect_format(path)
    if name not in converters.supported_targets(source):
        messagebox.showerror("Not supported", f"Can't convert {source} to {name}.")
        return

    base = os.path.splitext(os.path.basename(path))[0]
    dest = filedialog.asksaveasfilename(
        title="Save converted file as",
        initialfile=f"{base}.{name.lower()}",
        defaultextension=f".{name.lower()}",
    )
    if not dest:
        return

    busy = True
    status.config(text="Converting...")
    threading.Thread(target=run_conversion, args=(path, dest, name), daemon=True).start()


canvas = tk.Canvas(root, width=420, height=420, bg=BG, highlightthickness=0)
canvas.pack(pady=20)

for i in range(5):
    draw_segment(canvas, 210, 210, 180, i, on_segment_click)

root.mainloop()