import json
from datetime import datetime, timedelta
import threading

tasks = []

# Load tasks from JSON file
def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

# Save tasks to JSON file
def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

# Add a task
def add_task(title, description, due_date):
    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "done": False
    }
    tasks.append(task)
    save_tasks()

# List all tasks
def list_tasks():
    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "Pending"
        print(f"{i}. {task['title']} - Due: {task['due_date']} - Status: {status}")
        print(f"   Description: {task['description']}")

# Mark a task as done
def mark_as_done(task_index):
    try:
        tasks[task_index]["done"] = True
        save_tasks()
        print("Task marked as done.")
    except IndexError:
        print("Invalid task number.")

# Delete a task
def delete_task(task_index):
    try:
        removed_task = tasks.pop(task_index)
        save_tasks()
        print(f"Task '{removed_task['title']}' deleted.")
    except IndexError:
        print("Invalid task number.")

# Reminders
def send_reminders():
    while True:
        now = datetime.now()
        for task in tasks:
            if not task["done"]:
                try:
                    due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                    if 0 <= (due_date - now).days <= 1:
                        print(f"Reminder: Task '{task['title']}' is due on {task['due_date']}.")
                except ValueError:
                    print(f"Invalid date format for task '{task['title']}'.")
        threading.Event().wait(60)  # Check every 60 seconds

# Main menu
def main_menu():
    load_tasks()

    # Start reminder thread
    reminder_thread = threading.Thread(target=send_reminders, daemon=True)
    reminder_thread.start()

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark as Done")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            add_task(title, description, due_date)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            list_tasks()
            try:
                task_index = int(input("Enter task number to mark as done: ")) - 1
                mark_as_done(task_index)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "4":
            list_tasks()
            try:
                task_index = int(input("Enter task number to delete: ")) - 1
                delete_task(task_index)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "5":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()