import math
import tkinter as tk

FORMATS = ["PDF", "DOCX", "JPG", "PNG", "TXT"]
COLORS = ["#E5484D", "#3E7BFA", "#F5B83D", "#30A46C", "#8E7CC3"]
HOVER = ["#FF6B70", "#6B9AFF", "#FFCB63", "#4CC48A", "#A895DB"]
BG = "#FFF4E0"

def draw_segment(canvas, cx, cy, r, i, on_click):
    """Draw segment number i (0 to 4) as a pie slice."""
    start=90-(i+1) * 72
    seg = canvas.create_arc(
        cx-r, cy-r, cx+r, cy+r,
        start=start, extent=72,
        fill=COLORS[i], activefill=HOVER[i], outline=BG, width=6,
               style=tk.PIESLICE,
    )

        # Find the middle of the slice, then put the label there
    mid = math.radians(start + 36)
    x = cx + r * 0.6 * math.cos(mid)
    y = cy - r * 0.6 * math.sin(mid)
    canvas.create_text(x, y, text=FORMATS[i], fill="white",
                       font=("Helvetica", 16, "bold"), state=tk.DISABLED)
        # When this slice is clicked, call on_click with its format name
    canvas.tag_bind(seg, "<Button-1>", lambda event: on_click(FORMATS[i]))
    
    
    return seg



if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=400, bg=BG, highlightthickness=0)
    canvas.pack()

    def show(name):
        print("Selected:", name)

    for i in range(5):
        draw_segment(canvas, 200, 200, 170, i, show)
    root.mainloop()
