import json
import os
import sys
import shutil
from datetime import datetime

class TaskManager:
    def __init__(self, base_dir):
        # When bundled, use persistent directory
        if hasattr(sys, '_MEIPASS'):
            # Define persistent directory in home folder.
            self.data_dir = os.path.join(os.path.expanduser("~"), ".tasklogger")
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            self.tasks_file = os.path.join(self.data_dir, "tl_tasks.json")
            # Copy the bundled default tasks.json if it doesn't exist.
            bundled_tasks_path = os.path.join(sys._MEIPASS, "static", "json", "tl_tasks.json")
            if not os.path.exists(self.tasks_file):
                if os.path.exists(bundled_tasks_path):
                    shutil.copy(bundled_tasks_path, self.tasks_file)
                else:
                    with open(self.tasks_file, "w") as f:
                        json.dump({"tasks": [], "complete": []}, f)
        else:
            # In development, use the original file location.
            self.base_dir = base_dir
            self.tasks_file = os.path.join(self.base_dir, "static", "json", "tl_tasks.json")
        
        self.tasks = []
        self.completed_tasks = []
        self.load_tasks()
        
    def ensure_tasks_file(self):
        if not os.path.exists(self.tasks_file):
            default_tasks_path = os.path.join(self.base_dir, "tl_tasks.json")
            if os.path.exists(default_tasks_path):
                shutil.copy(default_tasks_path, self.tasks_file)
            else:
                with open(self.tasks_file, "w") as f:
                    json.dump({"tasks": [], "complete": []}, f)
    
    def load_tasks(self):
        try:
            with open(self.tasks_file, "r") as file:
                data = json.load(file)
                self.tasks = data.get("tasks", [])
                self.completed_tasks = data.get("complete", [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
            self.completed_tasks = []
        
        # Ensure each task has a time; if missing, default to "23:59"
        for i, task in enumerate(self.tasks):
            if len(task) == 2:
                self.tasks[i] = (*task, "23:59")
    
    def save_tasks(self):
        with open(self.tasks_file, "w") as file:
            json.dump({"tasks": self.tasks, "complete": self.completed_tasks}, file)
            
    def add_task(self, task_name, due_date=None, due_time=None):
        if not due_date:
            due_date = datetime.now().strftime("%Y-%m-%d")
        if not due_time:
            due_time = "23:59"
        self.tasks.append((task_name, due_date, due_time))
        self.save_tasks()
    
    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.completed_tasks.append(self.tasks.pop(index))
            self.save_tasks()
    
    def edit_task(self, index, new_task, new_date, new_time=None):
        if 0 <= index < len(self.tasks):
            if not new_time:
                new_time = "23:59"
            self.tasks[index] = (new_task, new_date, new_time)
            self.save_tasks()
    
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()
    
    def mark_task_incomplete(self, index):
        if 0 <= index < len(self.completed_tasks):
            self.tasks.append(self.completed_tasks.pop(index))
            self.save_tasks()
