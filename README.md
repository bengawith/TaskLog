# TaskLogger

TaskLogger is a personal task logging application with a modern interface built using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter). This application allows you to manage tasks, set due dates and times, and mark tasks as complete or incomplete.

## Features

- **Task Management:** Add, edit, and delete tasks with associated due dates and times.
- **Completion Tracking:** Mark tasks as completed and view a separate list of completed tasks.
- **Intuitive UI:** Visual feedback with dynamic time displays and color-coded task statuses.
- **Automatic Sorting:** Tasks are sorted based on due date and time.
- **Modular Design:** Separated logic into modules (`task_manager.py`, `ui.py`, `main.py`) for maintainability.

## Folder Structure

```
TaskLogger/
├── main.py                # main entry point            
├── ui.py                  # user interface
├── task_manager.py        # task management
├── TaskLogger.spec        # PyInstaller spec file
├── README.md              # This file
├── requirements.txt       # dependencies
└── static/
    ├── images/
    │   ├── TL.ico         # application icon
    │   └── tk_sky.jpg     # background image for the UI
    └── json/
        └── tasks.json     # task data
```

## Installation

### Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/)

### Dependencies

Install the required packages using pip:

```bash
pip install customtkinter pillow        # or pip install -r requirements.txt
```

## Running the Application

To run the TaskLogger application directly from source, navigate to the project directory and execute:

```bash
python main.py
```

## Building an Executable with PyInstaller

You can create a standalone executable using PyInstaller. Follow these steps:

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Build the Executable:**

   Use the provided `TaskLogger.spec` file to bundle your application along with the static assets:

   - **On Windows:**
     ```bash
     pyinstaller TaskLogger.spec
     ```
   - **On Linux/macOS:**
     Make sure to adjust the path separators in the spec file if necessary, then run:
     ```bash
     pyinstaller TaskLogger.spec
     ```

3. **Locate the Executable:**

   After the build process, the executable will be located in the `dist` directory.

## Contact

If you have any questions or feedback, please don't hesitate to reach out to me:
- [GitHub](https://github.com/bengawith)
