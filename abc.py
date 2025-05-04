import tkinter as tk

root = tk.Tk()
root.geometry("1000x1000")  # Размер окна

# Для HiDPI-экранов (Windows)
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

canvas = tk.Canvas(root, width=900, height=900, bg="lightblue")
canvas.pack(fill="both", expand=True)

root.mainloop()