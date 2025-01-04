import json
from datetime import datetime, timedelta
import threading
from plyer import notification
from tkinter import *
from tkinter import messagebox, ttk
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# Task storage
tasks = []

# Load tasks from JSON file
def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as f:
            tasks.extend(json.load(f))
    except FileNotFoundError:
        pass

# Save tasks to JSON file
def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

# Add a task
def add_task_gui():
    title = title_entry.get()
    description = desc_entry.get()
    due_date = due_date_entry.get()

    if not title or not due_date:
        messagebox.showerror("Error", "Title and Due Date are required.")
        return

    task = {"title": title, "description": description, "due_date": due_date, "done": False}
    tasks.append(task)
    save_tasks()
    refresh_task_list()
    title_entry.delete(0, END)
    desc_entry.delete(0, END)
    due_date_entry.delete(0, END)

# Refresh task list
def refresh_task_list():
    task_list.delete(*task_list.get_children())
    for i, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "Pending"
        task_list.insert("", "end", values=(i, task["title"], task["due_date"], status))

# Mark a task as done
def mark_as_done_gui():
    try:
        selected_item = task_list.selection()[0]
        task_index = int(task_list.item(selected_item, "values")[0]) - 1
        tasks[task_index]["done"] = True
        save_tasks()
        refresh_task_list()
    except IndexError:
        messagebox.showerror("Error", "No task selected.")

# Delete a task
def delete_task_gui():
    try:
        selected_item = task_list.selection()[0]
        task_index = int(task_list.item(selected_item, "values")[0]) - 1
        tasks.pop(task_index)
        save_tasks()
        refresh_task_list()
    except IndexError:
        messagebox.showerror("Error", "No task selected.")

# Enhanced reminders system
def send_reminders():
    while True:
        now = datetime.now()
        for task in tasks:
            if not task["done"]:
                try:
                    due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                    if 0 <= (due_date - now).days <= 1:
                        notification.notify(
                            title=f"Task Reminder: {task['title']}",
                            message=f"Due on {task['due_date']}. {task['description']}",
                            timeout=10
                        )
                except ValueError:
                    pass
        threading.Event().wait(60)  # Check every 60 seconds

# System tray integration
def on_exit(icon, item):
    icon.stop()
    root.quit()

def create_image():
    # Create a small icon for the system tray
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill=(0, 128, 255))
    return image

def minimize_to_tray():
    root.withdraw()
    tray_icon = Icon("Task Manager", create_image(), menu=Menu(MenuItem("Open", lambda icon, item: root.deiconify()), MenuItem("Exit", on_exit)))
    threading.Thread(target=tray_icon.run, daemon=True).start()

# Create GUI window
root = Tk()
root.title("Task Manager")
root.geometry("600x400")

# Input frame
input_frame = Frame(root, padx=10, pady=10)
input_frame.pack(fill="x")

Label(input_frame, text="Title", font=("Arial", 12)).grid(row=0, column=0, sticky=W, padx=5)
title_entry = Entry(input_frame, width=40, font=("Arial", 12))
title_entry.grid(row=0, column=1, padx=5)

Label(input_frame, text="Description", font=("Arial", 12)).grid(row=1, column=0, sticky=W, padx=5)
desc_entry = Entry(input_frame, width=40, font=("Arial", 12))
desc_entry.grid(row=1, column=1, padx=5)

Label(input_frame, text="Due Date (YYYY-MM-DD)", font=("Arial", 12)).grid(row=2, column=0, sticky=W, padx=5)
due_date_entry = Entry(input_frame, width=40, font=("Arial", 12))
due_date_entry.grid(row=2, column=1, padx=5)

add_button = Button(input_frame, text="Add Task", font=("Arial", 12), bg="#4CAF50", fg="white", command=add_task_gui)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Task list frame
task_frame = Frame(root, padx=10, pady=10)
task_frame.pack(fill="both", expand=True)

task_list = ttk.Treeview(task_frame, columns=("ID", "Title", "Due Date", "Status"), show="headings")
task_list.heading("ID", text="#")
task_list.heading("Title", text="Title")
task_list.heading("Due Date", text="Due Date")
task_list.heading("Status", text="Status")
task_list.column("ID", width=30)
task_list.column("Title", width=200)
task_list.column("Due Date", width=120)
task_list.column("Status", width=80)
task_list.pack(fill="both", expand=True)

# Action buttons
action_frame = Frame(root, padx=10, pady=10)
action_frame.pack(fill="x")

mark_done_button = Button(action_frame, text="Mark as Done", font=("Arial", 12), bg="#2196F3", fg="white", command=mark_as_done_gui)
mark_done_button.pack(side="left", padx=5)

delete_button = Button(action_frame, text="Delete Task", font=("Arial", 12), bg="#F44336", fg="white", command=delete_task_gui)
delete_button.pack(side="left", padx=5)

minimize_button = Button(action_frame, text="Minimize to Tray", font=("Arial", 12), bg="#FF9800", fg="white", command=minimize_to_tray)
minimize_button.pack(side="right", padx=5)

# Load tasks and start GUI loop
load_tasks()
refresh_task_list()

# Start reminder thread
reminder_thread = threading.Thread(target=send_reminders, daemon=True)
reminder_thread.start()

root.mainloop()
