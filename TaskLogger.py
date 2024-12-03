from customtkinter import *
from PIL import Image
from datetime import datetime, timedelta
import json

# Initialize the app
app = CTk()
app.geometry("800x480")
app.resizable(0, 0)
app.title("Task Logger")

# Ensure tasks.json is created in the same directory as the executable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")
IMAGE_FILE = os.path.join(BASE_DIR, "tk_sky.jpg")

# Load and set the left-side image
side_img_data = CTkImage(dark_image=Image.open(IMAGE_FILE), size=(400, 480))

# Left-side Image Label
CTkLabel(master=app, text="", image=side_img_data).pack(side="left", fill="both", expand=False)

# Right-side Frame for Tasks
right_frame = CTkFrame(master=app, width=400, height=480, fg_color="#1F1F1F")  # Dark theme
right_frame.pack_propagate(False)
right_frame.pack(side="right", fill="both", expand=True)

# Title Section
CTkLabel(
    master=right_frame,
    text="Welcome to TaskLogger",
    text_color="#A569BD",  # Purple title color
    font=("Arial Bold", 24),
).pack(pady=(32.5, 5))

CTkLabel(
    master=right_frame,
    text="Manage your tasks efficiently",
    text_color="#A0A0A0",  # Gray subtitle
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


def save_tasks():
    """Save tasks and completed tasks to the JSON file."""
    with open("TASKS_FILE", "w") as file:
        json.dump({"tasks": tasks, "complete": completed_tasks}, file)


def update_task_list():
    """Update the task list display."""
    global selected_task_index
    for widget in task_list.winfo_children():
        widget.destroy()

    # Sort tasks by due date
    tasks.sort(key=lambda task: datetime.strptime(task[1], "%Y-%m-%d"))

    for index, (task, date) in enumerate(tasks):
        due_date = datetime.strptime(date, "%Y-%m-%d")
        now = datetime.now()
        time_remaining = due_date - now
        if time_remaining.total_seconds() > 0:
            days, seconds = divmod(time_remaining.total_seconds(), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            time_str = f"Remaining: {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
            time_color = "#FFFFFF"
        else:
            time_str = "Overdue!"
            time_color = "#FF4C4C"  # Red for overdue

        task_label = CTkLabel(
            master=task_list,
            text=f"{task} (Due: {date})\n{time_str}",
            fg_color="#3B3B3B" if index != selected_task_index else "#601E88",
            text_color=time_color if time_str == "Overdue!" else "#FFFFFF",
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
    task_name = CTkInputDialog(title="Add Task", text="Enter the task name:").get_input()
    due_date = CTkInputDialog(title="Add Due Date", text="Enter the due date (YYYY-MM-DD):").get_input()
    if task_name and due_date:
        tasks.append((task_name, due_date))
        save_tasks()
        update_task_list()


def mark_task_completed():
    """Mark the selected task as completed."""
    global selected_task_index
    if selected_task_index is not None:
        completed_tasks.append(tasks.pop(selected_task_index))
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

        for index, (task, date) in enumerate(completed_tasks):
            task_label = CTkLabel(
                master=completed_task_list,
                text=f"{task} (Due: {date})",
                fg_color="#3B3B3B" if index != selected_completed_index else "#601E88",
                text_color="#FFFFFF" if index != selected_completed_index else "#FFFFFF",
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

    # Create a Toplevel window
    completed_window = CTkToplevel(app)
    completed_window.title("Completed Tasks")
    completed_window.geometry("400x350")
    completed_window.resizable(False, False)

    CTkLabel(
        master=completed_window,
        text="Completed Tasks",
        text_color="#A569BD",
        font=("Arial Bold", 18),
    ).pack(pady=(10, 10))

    completed_task_list = CTkScrollableFrame(master=completed_window, fg_color="#2B2B2B", width=350, height=150)
    completed_task_list.pack(fill="both", expand=True, padx=10, pady=10)

    update_completed_list()

    # Button for marking incomplete
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
        current_task, current_date = tasks[selected_task_index]

        # Create a custom edit dialog
        edit_dialog = CTkToplevel(app)
        edit_dialog.title("Edit Task")
        edit_dialog.geometry("400x250")
        edit_dialog.resizable(False, False)
        edit_dialog.configure(fg_color="#1F1F1F")  # Dark theme

        CTkLabel(master=edit_dialog, text="Edit Task Name:", text_color="#FFFFFF", font=("Arial", 12)).pack(pady=10)
        task_entry = CTkEntry(master=edit_dialog, width=300, fg_color="#3B3B3B", text_color="#FFFFFF")
        task_entry.insert(0, current_task)
        task_entry.pack(pady=5)

        CTkLabel(master=edit_dialog, text="Edit Due Date (YYYY-MM-DD):", text_color="#FFFFFF", font=("Arial", 12)).pack(pady=10)
        date_entry = CTkEntry(master=edit_dialog, width=300, fg_color="#3B3B3B", text_color="#FFFFFF")
        date_entry.insert(0, current_date)
        date_entry.pack(pady=5)

        def save_edits():
            new_task = task_entry.get()
            new_date = date_entry.get()
            if new_task and new_date:
                tasks[selected_task_index] = (new_task, new_date)
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
    app.after(1000, update_time)  # Update every second


# Button Section
button_frame = CTkFrame(master=right_frame, fg_color="#1F1F1F", corner_radius=0)
button_frame.pack(pady=(10, 0))

# Styling Buttons
button_style = {
    "fg_color": "#601E88",  # Purple button color
    "hover_color": "#E44982",  # Hover effect
    "font": ("Arial Bold", 12),
    "text_color": "#FFFFFF",
    "width": 180,
    "corner_radius": 8,
}

# Adding Buttons
CTkButton(
    master=button_frame,
    text="Add Task",
    **button_style,
    command=add_task,
).grid(row=0, column=0, padx=10, pady=5)

CTkButton(
    master=button_frame,
    text="Mark Completed",
    **button_style,
    command=mark_task_completed,
).grid(row=0, column=1, padx=10, pady=5)

CTkButton(
    master=button_frame,
    text="View Completed",
    **button_style,
    command=view_completed_tasks,
).grid(row=1, column=0, padx=10, pady=5)

CTkButton(
    master=button_frame,
    text="Edit Task",
    **button_style,
    command=edit_task,
).grid(row=1, column=1, padx=10, pady=5)

CTkButton(
    master=button_frame,
    text="Delete Task",
    **button_style,
    command=delete_task,
).grid(row=2, column=0, columnspan=2, pady=10)

# Load tasks on startup
load_tasks()
update_time()  # Start the time updates
update_task_list()

# Run the app
app.mainloop()
