# AI Employee System Architecture

## Bronze Tier Overview

The AI Employee Bronze Tier implements a local-first, file-based automation system that follows the Watcher → Reasoning → Action pattern.

## Component Architecture

### 1. File System Watcher (`Watchers/file_watcher.py`)
- **Purpose**: Monitors the Inbox folder for new files
- **Function**: Detects file creation/modification events
- **Output**: Creates structured task files in Needs_Action folder
- **Technology**: Python with pathlib for cross-platform compatibility

### 2. Task Processor (`Watchers/task_processor.py`)
- **Purpose**: Processes structured task files from Needs_Action folder
- **Function**: Interprets task instructions and executes appropriate actions
- **Output**: Moves processed tasks to Done folder, updates systems
- **Technology**: Python with structured parsing logic

### 3. Claude Agent Skills (`Skills/`)
- **Purpose**: Modular functions for specific tasks
- **Current Skills**:
  - Task Reader: Parses task files
  - File Mover: Handles file operations
  - Dashboard Updater: Maintains system status
  - Plan Generator: Creates strategic plans
  - Task Processor: Orchestrates task execution

### 4. File Organization System
- **Inbox/**: Entry point for new tasks
- **Needs_Action/**: Active tasks awaiting processing
- **Done/**: Completed tasks
- **Plans/**: Generated strategic documents
- **Logs/**: System audit trail
- **Skills/**: Skill definitions and documentation
- **Watchers/**: Monitoring components
- **Docs/**: Documentation and guides

### 5. Dashboard System (`Dashboard.md`)
- **Purpose**: Provides high-level system status
- **Updates**: Real-time statistics on task processing
- **Metrics**: Pending tasks, completed tasks, system health

### 6. Company Handbook (`Company_Handbook.md`)
- **Purpose**: Defines system behavior and constraints
- **Rules**: Safety protocols and operational guidelines
- **Constraints**: Prohibited and permitted actions

## Data Flow

```
[External Input] → [Inbox/] → [File Watcher] → [Needs_Action/] → [Task Processor] → [Done/]
                                    ↓                           ↓                   ↓
                              [Logs/] ←—————— [Dashboard.md] ←———— [Logs/]
                                    ↓
                             [Plans/] (when needed)
```

## Safety Architecture

### 1. Isolation
- All operations confined to local file system
- No network connectivity required
- No external API calls
- No internet access needed

### 2. Validation
- Input validation on all task files
- Permission checks before file operations
- Format verification for structured tasks
- Boundary checks for all file operations

### 3. Logging
- Comprehensive audit trail in Logs folder
- Timestamped event recording
- Error tracking and recovery
- System health monitoring

### 4. Constraints
- Follows Company Handbook behavioral rules
- Limited to authorized folder operations
- No destructive operations without safeguards
- All actions reversible when possible

## Execution Flow

1. **Detection Phase**: File watcher monitors Inbox for new files
2. **Task Creation Phase**: Structured task files created in Needs_Action
3. **Processing Phase**: Task processor interprets and executes instructions
4. **Action Phase**: Appropriate skills are invoked to complete tasks
5. **Completion Phase**: Task moved to Done, dashboard updated, logs recorded

## Technology Stack

- **Language**: Python 3.x
- **Architecture**: File-based, local-first
- **Components**: Modular, decoupled services
- **Interface**: Markdown-based task definitions
- **Storage**: Local file system with structured folders
- **Logging**: Text-based audit trails

## Scalability Considerations

- Thread-safe file operations
- Configurable processing intervals
- Modular skill system for extensibility
- Asynchronous processing capability
- Error isolation between tasks

## Security Model

- Zero trust for external inputs
- Principle of least privilege for file operations
- Immutable logs for audit trail
- Isolated execution environment
- Behavioral constraints enforcement