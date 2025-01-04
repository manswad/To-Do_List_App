# Task Manager Documentation

## Overview

Task Manager is a desktop application built with Python that helps users manage their daily tasks with a graphical user interface. It features task tracking, reminders, and system tray integration for seamless desktop usage.

## Installation

### Option 1: Windows Executable

1. Navigate to the Releases tab on GitHub
2. Download the latest `.exe` file
3. Run the executable - no additional installation required

### Option 2: From Source

Prerequisites:
- Python 3.6 or higher
- Required packages:
```bash
pip install plyer pillow pystray
```

To run from source:
1. Clone the repository
2. Navigate to the project directory
3. Run `python main.py`

## Features

### Core Functionality

- **Task Management**
    - Add tasks with title, description, and due date
    - Mark tasks as complete
    - Delete tasks
    - View all tasks in a sortable list

- **Persistent Storage**
    - Tasks automatically saved to `tasks.json`
    - Data persists between application restarts

- **Desktop Integration**
    - System tray functionality
    - Minimize to tray option
    - Desktop notifications for upcoming tasks

### Task Properties

- Title (required)
- Description (optional)
- Due Date (required, format: YYYY-MM-DD)
- Status (Pending/Done)

### Automatic Reminders

- Notifications for tasks due within 24 hours
- Includes task title, due date, and description
- Runs in background while application is open

## Usage Guide

### Adding a Task

1. Enter task title
2. (Optional) Add description
3. Enter due date in YYYY-MM-DD format
4. Click "Add Task"

### Managing Tasks

- **Mark as Done**: Select task and click "Mark as Done"
- **Delete Task**: Select task and click "Delete Task"
- **View Task Status**: Check the "Status" column in the task list

### System Tray Features

1. Click "Minimize to Tray" to hide the main window
2. Access the application from the system tray icon:
    - Click "Open" to restore the window
    - Click "Exit" to close the application

## Technical Details

### Data Storage

- Tasks stored in `tasks.json` in the application directory
- JSON format structure:
```json
[
    {
        "title": "Task Name",
        "description": "Task Description",
        "due_date": "YYYY-MM-DD",
        "done": false
    }
]
```

### Reminder System

- Checks task due dates every 60 seconds
- Triggers notifications for:
    - Tasks due today
    - Tasks due tomorrow
- Only notifies for pending tasks (not marked as done)

### UI Components

- Main window: 600x450 pixels
- Task list with sortable columns:
    - ID
    - Title
    - Due Date
    - Status
- Input fields for task creation
- Action buttons for task management

## Troubleshooting

### Common Issues

1. **Task Not Saving**
    - Check write permissions in application directory
    - Verify `tasks.json` is not read-only

2. **Notifications Not Working**
    - Ensure system notifications are enabled
    - Check if application has notification permissions

3. **Date Format Errors**
    - Ensure dates are in YYYY-MM-DD format
    - Check for proper hyphen usage in dates

### Known Limitations

- Cannot edit existing tasks (must delete and recreate)
- No support for recurring tasks
- Single user/local storage only

## Best Practices

1. Regularly check task list for upcoming deadlines
2. Use clear, descriptive titles for tasks
3. Include relevant details in task descriptions
4. Mark tasks as done promptly to avoid unnecessary reminders

## Security Notes

- Task data is stored locally without encryption
- No network connectivity required
- No authentication mechanism included

## System Requirements

- Windows Operating System
- Minimum 512MB RAM
- 50MB free disk space
- Display resolution: 800x600 or higher

## Support

For issues and feature requests:
- Submit issues via GitHub
- Include system details and error messages in reports

## Additional details:

This is my first project on GitHub.
Thank you for visiting ❤️