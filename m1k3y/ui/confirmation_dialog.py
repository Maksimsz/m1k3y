import tkinter as tk
from tkinter import ttk

def confirm_action(message: str) -> bool:
    result = {"ok": False}
    root = tk.Tk()
    root.title("Confirm Action")
    frm = ttk.Frame(root, padding=12)
    frm.pack(fill="both", expand=True)
    ttk.Label(frm, text=message, wraplength=300).pack(pady=10)
    def accept():
        result["ok"] = True
        root.destroy()
    def reject():
        result["ok"] = False
        root.destroy()
    btnf = ttk.Frame(frm)
    btnf.pack()
    ttk.Button(btnf, text="Confirm", command=accept).pack(side="left", padx=5)
    ttk.Button(btnf, text="Cancel", command=reject).pack(side="left", padx=5)
    root.mainloop()
    return result["ok"]