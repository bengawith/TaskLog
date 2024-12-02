import difflib
import json
import os

class TaskLogger:
    """
    Class of a to-do list app.
    """
    def __init__(self, tasks_file='tasks.json'):
        self.tasks_file = os.path.join(os.path.expanduser('~'), tasks_file)
        self.tasks = []
        self.complete = []
        self.start = True
        self._load_tasks()

    def _load_tasks(self)
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as file:
                data = json.load(file)
                self.tasks = data.get('tasks', [])
                self.complete = data.get('complete', [])

    def _save_tasks(self):
        with open(self.tasks_file, 'w') as file:
            json.dump({'tasks': self.tasks, 'complete': self.complete}, file)

    def main(self):
        while self.start:
            self.display_menu()
            choice = input("Choose an option: ")
            if choice == "1":
                self.view_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.mark_task_completed()
            elif choice == "4":
                print("Exiting the application. Goodbye!")
                self._save_tasks()
                self.start = False
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print("\nTo-Do List Menu:")
        print("1. View all tasks")
        print("2. Add a new task")
        print("3. Mark a task as completed")
        print("4. Exit")

    def add_task(self):
        task = input("Enter the new task: ")
        date = input("Enter the due date for the task: ")

        # Check for similar tasks
        for existing_task in self.tasks:
            similarity = difflib.SequenceMatcher(None, existing_task[0].lower(), task.lower()).ratio()
            if similarity >= 0.8 and existing_task[1] == date:
                response = input(f"Have you already logged this task? (Y/n) ").lower()
                if response == 'y':
                    response = input("Would you like to log a different task? (Y/n) ").lower()
                    if response == 'y':
                        self.add_task()
                    return

        self.tasks.append([task, date])
        print(f"Task '{task}' added.")
        self.save_tasks()

        self.tasks.append([task, date])
        print(f"Task '{task}' added.")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks currently.")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task[0]} (Due: {task[1]})")

    def view_complete(self):
        if not self.complete:
            print("No complete tasks.")
        else:
            for i, task in enumerate(self.complete, 1):
                print(f"{i}. {task[0]} (Due: {task[1]})")

    def mark_task_completed(self):
        self.view_tasks()
        task_number = int(input("Enter the task number to mark as completed: "))
        if 0 < task_number <= len(self.tasks):
            completed_task = self.tasks.pop(task_number - 1)
            self.complete.append(completed_task)
            print(f"Task '{completed_task[0]}' marked as completed.")
            self.save_tasks()
        else:
            print("Invalid task number.")

if __name__ == "__main__":
    todo = TaskLogger()
    todo.main()
