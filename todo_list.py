import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
import os

FILE = "tasks_pro.txt"

root = tk.Tk()
root.title("To-Do Pro")
root.geometry("520x520")

# -------- Data helpers --------
def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            for line in f:
                task_list.insert(tk.END, line.strip())
    update_counts()
    remind_today()

def save_tasks():
    with open(FILE, "w", encoding="utf-8") as f:
        for i in range(task_list.size()):
            f.write(task_list.get(i) + "\n")
    update_counts()

def format_task(title, due, cat, done=False):
    status = "✔" if done else "•"
    return f"{status} | {title} | Due: {due} | {cat}"

def parse_task(s):
    parts = [p.strip() for p in s.split("|")]
    done = parts[0] == "✔"
    title = parts[1]
    due = parts[2].replace("Due: ", "")
    cat = parts[3]
    return done, title, due, cat

# -------- Core actions --------
def add_task():
    title = title_entry.get().strip()
    due = due_entry.get().strip()
    cat = cat_var.get()

    if not title:
        messagebox.showwarning("Warning", "Enter a task title")
        return

    try:
        if due:
            datetime.strptime(due, "%Y-%m-%d")
        else:
            due = "None"
    except:
        messagebox.showwarning("Warning", "Use date format YYYY-MM-DD")
        return

    task_list.insert(tk.END, format_task(title, due, cat, False))
    title_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)
    save_tasks()

def delete_task():
    try:
        i = task_list.curselection()[0]
        task_list.delete(i)
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task")

def toggle_done(event=None):
    try:
        i = task_list.curselection()[0]
        done, title, due, cat = parse_task(task_list.get(i))
        task_list.delete(i)
        task_list.insert(i, format_task(title, due, cat, not done))
        save_tasks()
    except:
        pass

def clear_completed():
    items = list(task_list.get(0, tk.END))
    task_list.delete(0, tk.END)
    for s in items:
        done, title, due, cat = parse_task(s)
        if not done:
            task_list.insert(tk.END, s)
    save_tasks()

# -------- Search & stats --------
def search_tasks():
    q = search_entry.get().lower().strip()
    task_list.delete(0, tk.END)
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            for line in f:
                if q in line.lower():
                    task_list.insert(tk.END, line.strip())
    update_counts()

def reset_search():
    task_list.delete(0, tk.END)
    load_tasks()

def update_counts():
    total = task_list.size()
    done = 0
    for i in range(total):
        d, *_ = parse_task(task_list.get(i))
        if d: done += 1
    pending = total - done
    stats_var.set(f"Pending: {pending}   Completed: {done}")

# -------- Reminder --------
def remind_today():
    today = date.today().isoformat()
    due_today = []
    for i in range(task_list.size()):
        done, title, due, cat = parse_task(task_list.get(i))
        if (not done) and due == today:
            due_today.append(f"- {title} ({cat})")
    if due_today:
        messagebox.showinfo("Reminder", "Due today:\n" + "\n".join(due_today))

# -------- UI --------
top = tk.Frame(root); top.pack(pady=8)
tk.Label(top, text="Task").grid(row=0, column=0, padx=4)
title_entry = tk.Entry(top, width=20); title_entry.grid(row=0, column=1, padx=4)

tk.Label(top, text="Due (YYYY-MM-DD)").grid(row=0, column=2, padx=4)
due_entry = tk.Entry(top, width=12); due_entry.grid(row=0, column=3, padx=4)

tk.Label(top, text="Category").grid(row=0, column=4, padx=4)
cat_var = tk.StringVar(value="Work")
tk.OptionMenu(top, cat_var, "Work", "Study", "Personal", "Other").grid(row=0, column=5, padx=4)

tk.Button(root, text="Add Task", command=add_task).pack(pady=4)

mid = tk.Frame(root); mid.pack(pady=6)
search_entry = tk.Entry(mid, width=25); search_entry.pack(side=tk.LEFT, padx=4)
tk.Button(mid, text="Search", command=search_tasks).pack(side=tk.LEFT, padx=2)
tk.Button(mid, text="Reset", command=reset_search).pack(side=tk.LEFT, padx=2)

frame = tk.Frame(root); frame.pack(pady=8)
task_list = tk.Listbox(frame, width=75, height=12)
task_list.pack()
task_list.bind("<Double-Button-1>", toggle_done)

btns = tk.Frame(root); btns.pack(pady=6)
tk.Button(btns, text="Delete", command=delete_task).pack(side=tk.LEFT, padx=6)
tk.Button(btns, text="Clear Completed", command=clear_completed).pack(side=tk.LEFT, padx=6)

stats_var = tk.StringVar(value="Pending: 0   Completed: 0")
tk.Label(root, textvariable=stats_var).pack(pady=6)

load_tasks()
root.mainloop()