from customtkinter import *
from PIL import Image
from datetime import datetime, timedelta
import json
import os
import sys
import shutil

# Initialize the app
app = CTk()
app.geometry("800x480")
app.resizable(0, 0)
app.title("Task Logger")

# Determine the base directory for bundled and non-bundled execution
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS  # Directory for PyInstaller's temp folder
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_FILE = os.path.join(BASE_DIR, "tk_sky.jpg")

# Writable directory for tasks.json (user's home directory)
USER_DATA_DIR = os.path.expanduser("~")  # Example: C:\Users\<username>
TASKS_FILE = os.path.join(USER_DATA_DIR, "tasks.json")

# Ensure the tasks.json exists in the writable directory
if not os.path.exists(TASKS_FILE):
    default_tasks_path = os.path.join(BASE_DIR, "tasks.json")
    if os.path.exists(default_tasks_path):
        shutil.copy(default_tasks_path, TASKS_FILE)  # Copy default tasks.json
    else:
        with open(TASKS_FILE, "w") as f:
            json.dump({"tasks": [], "complete": []}, f)  # Create a blank JSON


# Load and set the left-side image
side_img_data = CTkImage(dark_image=Image.open(IMAGE_FILE), size=(400, 480))

# Left-side Image Label
CTkLabel(master=app, text="", image=side_img_data).pack(side="left", fill="both", expand=False)

# Right-side Frame for Tasks
right_frame = CTkFrame(master=app, width=400, height=480, fg_color="#1F1F1F")
right_frame.pack_propagate(False)
right_frame.pack(side="right", fill="both", expand=True)

# Title Section
CTkLabel(
    master=right_frame,
    text="Welcome to TaskLogger",
    text_color="#A569BD",
    font=("Arial Bold", 24),
).pack(pady=(32.5, 5))

CTkLabel(
    master=right_frame,
    text="Manage your tasks efficiently",
    text_color="#A0A0A0",
    font=("Arial", 12),
).pack(pady=(0, 20))

# Current Date and Time Label
time_label = CTkLabel(
    master=right_frame,
    text="",
    text_color="#FFFFFF",
    font=("Arial Bold", 12),
)
time_label.place(relx=1, rely=0, x=-10, y=10, anchor="ne")

# Task List Frame
task_frame = CTkFrame(master=right_frame, fg_color="#2B2B2B", corner_radius=10, width=350, height=200)
task_frame.pack_propagate(False)
task_frame.pack(pady=(10, 20))

# Scrollable Task List
task_list = CTkScrollableFrame(master=task_frame, fg_color="#3B3B3B", corner_radius=10, width=350, height=200)
task_list.pack(fill="both", expand=True, anchor="center", padx=10, pady=10)

# Task Data
tasks = []
completed_tasks = []
selected_task_index = None


def load_tasks():
    """Load tasks from the JSON file."""
    global tasks, completed_tasks
    try:
        with open(TASKS_FILE, "r") as file:
            data = json.load(file)
            tasks = data.get("tasks", [])
            completed_tasks = data.get("complete", [])
    except FileNotFoundError:
        tasks = []
        completed_tasks = []

    # Ensure tasks without time have a default time of 23:59:59
    for i, task in enumerate(tasks):
        if len(task) == 2:
            tasks[i] = (*task, "23:59:59")


def save_tasks():
    """Save tasks and completed tasks to the JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump({"tasks": tasks, "complete": completed_tasks}, file)


def update_task_list():
    """Update the task list display."""
    global selected_task_index
    for widget in task_list.winfo_children():
        widget.destroy()

    # Sort tasks by combined date and time
    tasks.sort(key=lambda task: datetime.strptime(f"{task[1]} {task[2]}", "%Y-%m-%d %H:%M:%S"))

    for index, (task, date, time) in enumerate(tasks):
        due_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_remaining = due_datetime - now

        if time_remaining.total_seconds() <= 0:
            time_str = "Overdue!"
            time_color = "#FF4C4C"  # Red for overdue
        elif time_remaining.days < 7:
            time_str = f"Remaining: {time_remaining.days}d {time_remaining.seconds // 3600}h"
            time_color = "#FFA500"  # Orange for less than 7 days
        else:
            time_str = f"Remaining: {time_remaining.days}d {time_remaining.seconds // 3600}h"
            time_color = "#00FF00"  # Green for more than 7 days

        task_label = CTkLabel(
            master=task_list,
            text=f"{task} ({date} {time})\n{time_str}",
            fg_color="#3B3B3B" if index != selected_task_index else "#601E88",
            text_color=time_color,
            font=("Arial", 12),
            corner_radius=8,
            anchor="center",
            justify="center"
        )
        task_label.pack(fill="x", padx=5, pady=2)
        task_label.bind("<Button-1>", lambda event, idx=index: select_task(idx))


def select_task(index):
    """Select a task."""
    global selected_task_index
    selected_task_index = index
    update_task_list()


def add_task():
    """Add a new task."""
    task_name = CTkInputDialog(
        title="Add Task",
        text="Enter the task name:",
        button_fg_color="#601E88",
        fg_color="#3B3B3B",
        text_color="#F2F2F2",
        font=("Arial", 12),
        button_hover_color="#E44982"
    ).get_input()

    due_date = CTkInputDialog(
        title="Add Due Date",
        text="Enter the due date (YYYY-MM-DD):",
        button_fg_color="#601E88",
        fg_color="#3B3B3B",
        text_color="#F2F2F2",
        font=("Arial", 12),
        button_hover_color="#E44982"
    ).get_input()

    due_time = CTkInputDialog(
        title="Add Due Time",
        text="Enter the due time (H:M:S) [Optional]:",
        button_fg_color="#601E88",
        fg_color="#3B3B3B",
        text_color="#F2F2F2",
        font=("Arial", 12),
        button_hover_color="#E44982"
    ).get_input()

    if task_name and due_date:
        if not due_time:
            due_time = "23:59:59"  # Default time
        tasks.append((task_name, due_date, due_time))
        save_tasks()
        update_task_list()


def mark_task_completed():
    """Mark the selected task as completed."""
    global selected_task_index
    if selected_task_index is not None:
        completed_tasks.append(tasks.pop(tasks[selected_task_index]))
        selected_task_index = None
        save_tasks()
        update_task_list()


def view_completed_tasks():
    """View completed tasks."""
    def mark_incomplete():
        """Mark selected completed task as incomplete."""
        nonlocal selected_completed_index
        if selected_completed_index is not None:
            tasks.append(completed_tasks.pop(selected_completed_index))
            selected_completed_index = None
            save_tasks()
            update_completed_list()
            update_task_list()

    def update_completed_list():
        """Update the completed tasks list in the dialog."""
        for widget in completed_task_list.winfo_children():
            widget.destroy()

        for index, (task, date, time) in enumerate(completed_tasks):
            task_label = CTkLabel(
                master=completed_task_list,
                text=f"{task} ({date} {time})",
                fg_color="#3B3B3B" if index != selected_completed_index else "#601E88",
                text_color="#FFFFFF",
                font=("Arial", 12),
                corner_radius=8,
                anchor="center",
                justify="center"
            )
            task_label.pack(fill="x", padx=5, pady=2)
            task_label.bind("<Button-1>", lambda event, idx=index: select_completed_task(idx))

    def select_completed_task(index):
        """Select a completed task."""
        nonlocal selected_completed_index
        selected_completed_index = index
        update_completed_list()

    selected_completed_index = None

    completed_window = CTkToplevel(app)
    completed_window.title("Completed Tasks")
    completed_window.geometry("400x350")
    completed_window.resizable(True, False)

    CTkLabel(
        master=completed_window,
        text="Completed Tasks",
        text_color="#A569BD",
        font=("Arial Bold", 18),
    ).pack(pady=(10, 10))

    completed_task_list = CTkScrollableFrame(master=completed_window, fg_color="#2B2B2B", width=350, height=150)
    completed_task_list.pack(fill="both", expand=True, padx=10, pady=10)

    update_completed_list()

    CTkButton(
        master=completed_window,
        text="Mark Incomplete",
        fg_color="#601E88",
        hover_color="#E44982",
        font=("Arial Bold", 12),
        text_color="#FFFFFF",
        command=mark_incomplete,
    ).pack(pady=10)


def edit_task():
    """Edit the selected task."""
    global selected_task_index
    if selected_task_index is not None:
        current_task, current_date, current_time = tasks[selected_task_index]

        edit_dialog = CTkToplevel(app)
        edit_dialog.title("Edit Task")
        edit_dialog.geometry("400x300")
        edit_dialog.resizable(False, False)
        edit_dialog.configure(fg_color="#1F1F1F")

        CTkLabel(master=edit_dialog, text="Edit Task Name:", text_color="#FFFFFF", font=("Arial", 12)).pack(pady=10)
        task_entry = CTkEntry(master=edit_dialog, width=300, fg_color="#3B3B3B", text_color="#FFFFFF")
        task_entry.insert(0, current_task)
        task_entry.pack(pady=5)

        CTkLabel(master=edit_dialog, text="Edit Due Date (YYYY-MM-DD):", text_color="#FFFFFF", font=("Arial", 12)).pack(pady=10)
        date_entry = CTkEntry(master=edit_dialog, width=300, fg_color="#3B3B3B", text_color="#FFFFFF")
        date_entry.insert(0, current_date)
        date_entry.pack(pady=5)

        CTkLabel(master=edit_dialog, text="Edit Due Time (H:M:S):", text_color="#FFFFFF", font=("Arial", 12)).pack(pady=10)
        time_entry = CTkEntry(master=edit_dialog, width=300, fg_color="#3B3B3B", text_color="#FFFFFF")
        time_entry.insert(0, current_time)
        time_entry.pack(pady=5)

        def save_edits():
            new_task = task_entry.get()
            new_date = date_entry.get()
            new_time = time_entry.get() or "23:59:59"
            if new_task and new_date:
                tasks[selected_task_index] = (new_task, new_date, new_time)
                save_tasks()
                update_task_list()
                edit_dialog.destroy()

        CTkButton(
            master=edit_dialog,
            text="Save",
            fg_color="#601E88",
            hover_color="#E44982",
            font=("Arial Bold", 12),
            text_color="#FFFFFF",
            command=save_edits,
        ).pack(pady=10)


def delete_task():
    """Delete the selected task."""
    global selected_task_index
    if selected_task_index is not None:
        tasks.pop(selected_task_index)
        selected_task_index = None
        save_tasks()
        update_task_list()


def update_time():
    """Update the current time and refresh the task list."""
    now = datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")
    time_label.configure(text=now)
    update_task_list()
    app.after(1000, update_time)


# Button Section
button_frame = CTkFrame(master=right_frame, fg_color="#1F1F1F", corner_radius=0)
button_frame.pack(pady=(10, 0))

button_style = {
    "fg_color": "#601E88",
    "hover_color": "#E44982",
    "font": ("Arial Bold", 12),
    "text_color": "#FFFFFF",
    "width": 180,
    "corner_radius": 8,
}

CTkButton(master=button_frame, text="Add Task", **button_style, command=add_task).grid(row=0, column=0, padx=10, pady=5)
CTkButton(master=button_frame, text="Mark Completed", **button_style, command=mark_task_completed).grid(row=0, column=1, padx=10, pady=5)
CTkButton(master=button_frame, text="View Completed", **button_style, command=view_completed_tasks).grid(row=1, column=0, padx=10, pady=5)
CTkButton(master=button_frame, text="Edit Task", **button_style, command=edit_task).grid(row=1, column=1, padx=10, pady=5)
CTkButton(master=button_frame, text="Delete Task", **button_style, command=delete_task).grid(row=2, column=0, columnspan=2, pady=10)

# Load tasks on startup
load_tasks()
update_time()
update_task_list()

# Run the app
app.mainloop()
