# File System Watcher for AI Employee

This script monitors the Inbox folder for new files and creates corresponding task files in the Needs_Action folder.

## Functionality

The file system watcher performs the following operations:

1. Continuously monitors the `/Inbox/` directory for new files
2. When a new file is detected, reads its content
3. Creates a structured task file in `/Needs_Action/` with processing instructions
4. Logs the detection event in `/Logs/`
5. Updates the dashboard with the new task

## Implementation

This watcher is designed to be simple and reliable, focusing on file detection and task creation without complex processing. All heavy processing is deferred to the Skills layer.

## Configuration

- Watch Interval: 5 seconds (adjustable)
- Source Directory: `/Inbox/`
- Target Directory: `/Needs_Action/`
- Log File: `/Logs/watcher.log`

## Safety Features

- No processing of file contents - only detection and notification
- Rate limiting to prevent system overload
- Error handling for file access issues
- Graceful degradation when target directories are unavailable