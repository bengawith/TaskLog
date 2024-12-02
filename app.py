import tkinter as tk
from tkinter import messagebox, simpledialog
import difflib
import json
import os

class TaskLogger:
    def __init__(self, tasks_file='tasks.json'):
        self.tasks_file = os.path.join(os.path.expanduser('~'), tasks_file)
        self.tasks = []
        self.complete = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as file:
                data = json.load(file)
                self.tasks = data.get('tasks', [])
                self.complete = data.get('complete', [])

    def save_tasks(self):
        with open(self.tasks_file, 'w') as file:
            json.dump({'tasks': self.tasks, 'complete': self.complete}, file)

    def add_task(self, task, date):
        for existing_task in self.tasks:
            similarity = difflib.SequenceMatcher(None, existing_task[0].lower(), task.lower()).ratio()
            if similarity >= 0.8 and existing_task[1] == date:
                return False
        self.tasks.append([task, date])
        self.save_tasks()
        return True

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            completed_task = self.tasks.pop(index)
            self.complete.append(completed_task)
            self.save_tasks()
            return True
        return False

class TaskLoggerGUI:
    def __init__(self, root, task_logger):
        self.root = root
        self.task_logger = task_logger
        self.root.title("To-Do List App")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.task_listbox.pack(side=tk.LEFT, padx=10)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.complete_button = tk.Button(root, text="Mark as Completed", command=self.mark_task_completed)
        self.complete_button.pack(pady=5)

        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task, date in self.task_logger.tasks:
            self.task_listbox.insert(tk.END, f"{task} (Due: {date})")

    def add_task(self):
        task = simpledialog.askstring("New Task", "Enter the new task:")
        date = simpledialog.askstring("Due Date", "Enter the due date for the task:")
        if task and date:
            if self.task_logger.add_task(task, date):
                self.load_tasks()
            else:
                messagebox.showwarning("Duplicate Task", "This task is already logged.")

    def mark_task_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            if self.task_logger.mark_task_completed(index):
                self.load_tasks()
            else:
                messagebox.showerror("Error", "Failed to mark task as completed.")
        else:
            messagebox.showwarning("No Selection", "Please select a task to mark as completed.")

if __name__ == "__main__":
    task_logger = TaskLogger()
    root = tk.Tk()
    gui = TaskLoggerGUI(root, task_logger)
    root.mainloop()
