from customtkinter import *
from PIL import Image
from datetime import datetime
import os
import sys
import tkinter.messagebox as mbox
from constants import *
from task_manager import TaskManager
from random import sample

class TaskLoggerApp:
    def __init__(self):
        # Initialize the main app window.
        self.app = CTk()
        self.app.geometry("800x480")
        self.app.resizable(0, 0)
        self.app.title("Task Logger")
        
        # Determine base directory (bundled vs. non-bundled)
        if hasattr(sys, '_MEIPASS'):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Initialize the task manager.
        self.task_manager = TaskManager(self.base_dir)
        
        # Load and set the left-side image.
        self.image_file = os.path.join(self.base_dir, "static", "images", "tk_sky.jpg")
        self.side_img_data = CTkImage(dark_image=Image.open(self.image_file), size=(400, 480))
        CTkLabel(master=self.app, text="", image=self.side_img_data).pack(side="left", fill="both", expand=False)
        
        # Create right-side frame.
        self.right_frame = CTkFrame(master=self.app, width=400, height=480, fg_color=COLOURS['BLACK'])
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side="right", fill="both", expand=True)
        
        # Title and subtitle.
        CTkLabel(
            master=self.right_frame,
            text="Welcome to TaskLogger",
            text_color=COLOURS['LIGHT_PURPLE'],
            font=LARGE_BOLD
        ).pack(pady=(32.5, 5))
        CTkLabel(
            master=self.right_frame,
            text="Manage your tasks efficiently",
            text_color=COLOURS['LIGHT_GREY'],
            font=SMALL
        ).pack(pady=(0, 20))
        
        # Current time label.
        self.time_label = CTkLabel(
            master=self.right_frame,
            text="",
            text_color=COLOURS['WHITE'],
            font=SMALL_BOLD
        )
        self.time_label.place(relx=1, rely=0, x=-10, y=10, anchor="ne")
        
        # Task list frame.
        self.task_frame = CTkFrame(master=self.right_frame, fg_color=COLOURS['GREY'], corner_radius=10, width=350, height=200)
        self.task_frame.pack_propagate(False)
        self.task_frame.pack(pady=(10,20))
        self.task_list = CTkScrollableFrame(master=self.task_frame, fg_color=COLOURS['DARK_GREY'], corner_radius=10, width=350, height=200)
        self.task_list.pack(fill="both", expand=True, anchor="center", padx=10, pady=10)
        
        self.selected_tasks = []
        
        # Button frame.
        self.button_frame = CTkFrame(master=self.right_frame, fg_color=COLOURS['BLACK'], corner_radius=0)
        self.button_frame.pack(pady=(10, 0))
        self.button_style = {
            "fg_color": COLOURS['PURPLE'],
            "hover_color": COLOURS['PINK'],
            "font": SMALL_BOLD,
            "text_color": COLOURS['WHITE'],
            "width": 180,
            "corner_radius": 8,
        }
        
        CTkButton(master=self.button_frame, text="Add Task", **self.button_style, command=self.add_task_dialog).grid(row=0, column=0, padx=10, pady=5)
        CTkButton(master=self.button_frame, text="Mark Completed", **self.button_style, command=self.mark_task_completed_ui).grid(row=0, column=1, padx=10, pady=5)
        CTkButton(master=self.button_frame, text="View Completed", **self.button_style, command=self.view_completed_tasks).grid(row=1, column=0, padx=10, pady=5)
        CTkButton(master=self.button_frame, text="Edit Task", **self.button_style, command=self.edit_task_dialog).grid(row=1, column=1, padx=10, pady=5)
        CTkButton(master=self.button_frame, text="Delete Task", **self.button_style, command=self.delete_task_ui).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Start the update routines.
        self.update_time()
        self.update_task_list()
    
    def update_time(self):
        now = datetime.now().strftime("%A, %Y-%m-%d %H:%M")
        self.time_label.configure(text=now)
        self.update_task_list()
        self.app.after(1000, self.update_time)
    
    def update_task_list(self):
        # Clear the current task list.
        for widget in self.task_list.winfo_children():
            widget.destroy()

        if len(self.task_manager.tasks) == 0:
            self.no_tasks()
            

            
        # Sort tasks by date and time.
        try:
            self.task_manager.tasks.sort(key=lambda task: datetime.strptime(f"{task[1]} {task[2]}", "%Y-%m-%d %H:%M"))
        except Exception:
            pass
        
        # Create a label for each task.
        for index, (task, date, time) in enumerate(self.task_manager.tasks):
            due_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            now = datetime.now()
            time_remaining = due_datetime - now
            
            if time_remaining.total_seconds() <= 0:
                time_str = "Overdue!"
                time_color = COLOURS['RED']
            elif time_remaining.days < 7:
                time_str = f"Remaining: {time_remaining.days}d {time_remaining.seconds // 3600}h"
                time_color = COLOURS['ORANGE']
            else:
                time_str = f"Remaining: {time_remaining.days}d {time_remaining.seconds // 3600}h"
                time_color = COLOURS['GREEN']
            
            task_label = CTkLabel(
                master=self.task_list,
                text=f"{task} ({date} {time})\n{time_str}",
                fg_color=COLOURS['DARK_GREY'] if index not in self.selected_tasks else COLOURS['PURPLE'],
                text_color=time_color,
                font=SMALL,
                corner_radius=8,
                anchor="center",
                justify="center"
            )
            task_label.pack(fill="x", padx=5, pady=2)
            task_label.bind("<Button-1>", lambda event, idx=index: self.select_task(idx))

    def select_task(self, index):
        if index in self.selected_tasks:
            self.selected_tasks.remove(index)
        else:
            self.selected_tasks.append(index)
        self.update_task_list()
    
    def add_task_dialog(self):
        task_name = CTkInputDialog(
            title="Add Task",
            text="Enter the task name:",
            button_fg_color=COLOURS['PURPLE'],
            fg_color=COLOURS['DARK_GREY'],
            text_color=COLOURS['WHITE'],
            font=SMALL,
            button_hover_color=COLOURS['PINK']
        ).get_input()
        
        if task_name:
            due_date = CTkInputDialog(
                title="Add Due Date",
                text="Enter the due date (YYYY-MM-DD):\nIf not provided, current date used",
                button_fg_color=COLOURS['PURPLE'],
                fg_color=COLOURS['DARK_GREY'],
                text_color=COLOURS['WHITE'],
                font=SMALL,
                button_hover_color=COLOURS['PINK']
            ).get_input()
            due_time = CTkInputDialog(
                title="Add Due Time",
                text="Enter the due time (H:M) [Optional]:",
                button_fg_color=COLOURS['PURPLE'],
                fg_color=COLOURS['DARK_GREY'],
                text_color=COLOURS['WHITE'],
                font=SMALL,
                button_hover_color=COLOURS['PINK']
            ).get_input()
            
            # Validate the due_date format.
            try:
                if due_date:
                    datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                mbox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
                return
            
            self.task_manager.add_task(task_name, due_date, due_time)
            self.update_task_list()
    
    def mark_task_completed_ui(self):
        if len(self.selected_tasks) > 0:
            for task_index in self.selected_tasks:
                self.task_manager.mark_task_completed(task_index)
                self.selected_tasks.remove(task_index)
                self.update_task_list()
    
    def delete_task_ui(self):
        if len(self.selected_tasks) > 0:
            for task_index in self.selected_tasks:
                self.task_manager.delete_task(task_index)
                self.selected_tasks.remove(task_index)
                self.update_task_list()
    
    def edit_task_dialog(self):
        if len(self.selected_tasks) > 0:
            for task_index in self.selected_tasks:
                current_task, current_date, current_time = self.task_manager.tasks[task_index]
                
                edit_dialog = CTkToplevel(self.app)
                edit_dialog.title("Edit Task")
                edit_dialog.geometry("400x300")
                edit_dialog.resizable(False, False)
                edit_dialog.configure(fg_color=COLOURS['BLACK'])
                edit_dialog.lift()
                edit_dialog.focus_force()
                
                CTkLabel(edit_dialog, text="Edit Task Name:", text_color=COLOURS['WHITE'], font=SMALL).pack(pady=10)
                task_entry = CTkEntry(edit_dialog, width=300, fg_color=COLOURS['DARK_GREY'], text_color=COLOURS['WHITE'])
                task_entry.insert(0, current_task)
                task_entry.pack(pady=5)
                
                CTkLabel(edit_dialog, text="Edit Due Date (YYYY-MM-DD):", text_color=COLOURS['WHITE'], font=SMALL).pack(pady=10)
                date_entry = CTkEntry(edit_dialog, width=300, fg_color=COLOURS['DARK_GREY'], text_color=COLOURS['WHITE'])
                date_entry.insert(0, current_date)
                date_entry.pack(pady=5)
                
                CTkLabel(edit_dialog, text="Edit Due Time (H:M) [Optional]:", text_color=COLOURS['WHITE'], font=SMALL).pack(pady=10)
                time_entry = CTkEntry(edit_dialog, width=300, fg_color=COLOURS['DARK_GREY'], text_color=COLOURS['WHITE'])
                time_entry.insert(0, current_time)
                time_entry.pack(pady=5)
                
                def save_edits():
                    new_task = task_entry.get()
                    new_date = date_entry.get()
                    new_time = time_entry.get() or "23:59"
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                    except ValueError:
                        mbox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
                        return
                    self.task_manager.edit_task(task_index, new_task, new_date, new_time)
                    self.update_task_list()
                    edit_dialog.destroy()
                
                CTkButton(
                    edit_dialog,
                    text="Save",
                    fg_color=COLOURS['PURPLE'],
                    hover_color=COLOURS['PINK'],
                    font=SMALL_BOLD,
                    text_color=COLOURS['WHITE'],
                    command=save_edits
                ).pack(pady=10)
    
    def view_completed_tasks(self):
        def mark_incomplete():
            nonlocal selected_completed_index
            if selected_completed_index is not None:
                self.task_manager.mark_task_incomplete(selected_completed_index)
                selected_completed_index = None
                update_completed_list()
                self.update_task_list()
        
        def update_completed_list():
            for widget in completed_task_list.winfo_children():
                widget.destroy()
            
            for index, (task, date, time) in enumerate(self.task_manager.completed_tasks):
                task_label = CTkLabel(
                    master=completed_task_list,
                    text=f"{task} ({date} {time})",
                    fg_color=COLOURS['DARK_GREY'] if index != selected_completed_index else COLOURS['PURPLE'],
                    text_color=COLOURS['WHITE'],
                    font=SMALL,
                    corner_radius=8,
                    anchor="center",
                    justify="center"
                )
                task_label.pack(fill="x", padx=5, pady=2)
                task_label.bind("<Button-1>", lambda event, idx=index: select_completed_task(idx))
        
        def select_completed_task(index):
            nonlocal selected_completed_index
            selected_completed_index = index
            update_completed_list()
        
        selected_completed_index = None
        completed_window = CTkToplevel(self.app)
        completed_window.title("Completed Tasks")
        completed_window.geometry("400x350")
        completed_window.resizable(True, False)
        completed_window.lift()        # Bring window to front
        completed_window.focus_force()
        
        CTkLabel(
            master=completed_window,
            text="Completed Tasks",
            text_color=COLOURS['LIGHT_PURPLE'],
            font=MEDIUM_BOLD
        ).pack(pady=(10, 10))
        
        completed_task_list = CTkScrollableFrame(master=completed_window, fg_color=COLOURS['GREY'], width=350, height=150)
        completed_task_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        update_completed_list()
        
        CTkButton(
            master=completed_window,
            text="Mark Incomplete",
            fg_color=COLOURS['PURPLE'],
            hover_color=COLOURS['PINK'],
            font=SMALL_BOLD,
            text_color=COLOURS['WHITE'],
            command=mark_incomplete
        ).pack(pady=10)

    def no_tasks(self):
        colour = sample(sorted(COLOURS.keys()), 1)[0]
        CTkLabel(
            master=self.task_list,
            text="🎊 No tasks to complete! 🎊",
            text_color=COLOURS[colour],
            font=MEDIUM_BOLD,
            corner_radius=8,
            anchor="center",
            justify="center"
        ).pack(fill="x", padx=5, pady=55)
        return
    
    def run(self):
        self.app.mainloop()

