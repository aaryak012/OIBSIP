
import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip

AMBIGUOUS = "0O1lI"

history = []

def build_pool():
    pool = ""
    groups = []

    if upper_var.get():
        chars = string.ascii_uppercase
        if exclude_var.get():
            chars = "".join(c for c in chars if c not in AMBIGUOUS)
        pool += chars
        groups.append(chars)

    if lower_var.get():
        chars = string.ascii_lowercase
        if exclude_var.get():
            chars = "".join(c for c in chars if c not in AMBIGUOUS)
        pool += chars
        groups.append(chars)

    if digit_var.get():
        chars = string.digits
        if exclude_var.get():
            chars = "".join(c for c in chars if c not in AMBIGUOUS)
        pool += chars
        groups.append(chars)

    if symbol_var.get():
        chars = string.punctuation
        pool += chars
        groups.append(chars)

    return pool, groups

def strength(length, types):
    score = 0
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    score += max(0, types-1)

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    return "Strong"

def generate():
    length = length_var.get()
    pool, groups = build_pool()

    if length < 8:
        messagebox.showerror("Error","Password length must be at least 8.")
        return

    if len(groups) < 2:
        messagebox.showerror("Error","Select at least two character types.")
        return

    pwd = [secrets.choice(g) for g in groups]
    while len(pwd) < length:
        pwd.append(secrets.choice(pool))
    secrets.SystemRandom().shuffle(pwd)
    password = "".join(pwd)

    password_var.set(password)
    pyperclip.copy(password)

    s = strength(length, len(groups))
    strength_label.config(text=f"Strength: {s}")

    history.insert(0, password)
    del history[5:]
    history_box.delete(0, tk.END)
    for p in history:
        history_box.insert(tk.END, p)

def copy_password():
    if password_var.get():
        pyperclip.copy(password_var.get())
        messagebox.showinfo("Copied","Password copied to clipboard.")

root = tk.Tk()
root.title("Advanced Random Password Generator")
root.geometry("520x620")
root.resizable(False, False)

password_var = tk.StringVar()
length_var = tk.IntVar(value=12)

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar()

tk.Label(root,text="Random Password Generator",font=("Arial",18,"bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame,text="Password Length").grid(row=0,column=0,sticky="w")
tk.Spinbox(frame,from_=8,to=64,textvariable=length_var,width=8).grid(row=0,column=1,padx=5)

tk.Checkbutton(frame,text="Uppercase",variable=upper_var).grid(row=1,column=0,sticky="w")
tk.Checkbutton(frame,text="Lowercase",variable=lower_var).grid(row=1,column=1,sticky="w")
tk.Checkbutton(frame,text="Numbers",variable=digit_var).grid(row=2,column=0,sticky="w")
tk.Checkbutton(frame,text="Symbols",variable=symbol_var).grid(row=2,column=1,sticky="w")
tk.Checkbutton(frame,text="Exclude Ambiguous (0,O,1,l,I)",variable=exclude_var).grid(row=3,column=0,columnspan=2,sticky="w",pady=5)

ttk.Button(root,text="Generate Password",command=generate).pack(pady=10)

tk.Entry(root,textvariable=password_var,font=("Consolas",13),justify="center",width=40).pack(pady=5)

ttk.Button(root,text="Copy to Clipboard",command=copy_password).pack()

strength_label = tk.Label(root,text="Strength: -",font=("Arial",12,"bold"))
strength_label.pack(pady=10)

tk.Label(root,text="Last 5 Generated Passwords").pack()

history_box = tk.Listbox(root,width=55,height=5)
history_box.pack(pady=5)

tk.Label(
    root,
    text="Passwords are copied automatically when generated.",
    fg="gray"
).pack(pady=10)

root.mainloop()
