# AI Employee Summary

## What This AI Employee Does

This AI Employee is a local-first digital assistant that automates routine tasks through a file-based workflow system. It operates using a Watcher → Reasoning → Action architecture:

### Core Functions:
- **File Monitoring**: Continuously watches the Inbox folder for new files
- **Task Processing**: Automatically creates and processes structured task files
- **Workflow Management**: Moves tasks through different stages (Needs Action → Done)
- **Status Tracking**: Maintains a dashboard with real-time system status
- **Plan Generation**: Creates strategic plans based on task requirements

### Architecture:
- **Local-First**: All operations occur on your local system with no external dependencies
- **File-Based**: Uses a folder system (Inbox, Needs_Action, Done, Plans, Logs) to manage tasks
- **Autonomous**: Runs continuously to detect and process new tasks automatically
- **Safe**: Enforces strict safety constraints with no external API calls, payments, or messaging

### How It Works:
1. Place files in the Inbox folder
2. The file watcher detects new files and creates structured tasks
3. The task processor handles each task according to its requirements
4. Completed tasks are moved to the Done folder
5. The dashboard updates to reflect current system status

This system provides a secure, autonomous way to automate routine file-based tasks while maintaining complete local control.