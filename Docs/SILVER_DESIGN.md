# Silver Tier Design Document

## Overview

The Silver Tier of the AI Employee system enhances the Bronze Tier with advanced features including multiple watchers, human-in-the-loop approval workflows, MCP server integration, and scheduling capabilities.

## Architecture

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Watchers      │    │   MCP Server     │    │  Approval        │
│                 │    │                  │    │  Monitor         │
│ • File System   │────│ • Draft Emails   │────│ • Pending        │
│ • Gmail         │    │ • Draft Messages │    │ • Approved       │
│ • Future...     │    │ • Draft Status   │    │ • Rejected       │
└─────────────────┘    └──────────────────┘    └──────────────────┘
         │                       │                        │
         ▼                       ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Task Processor  │    │ Skills Layer     │    │  Status Tracker  │
│                 │    │                  │    │                  │
│ • Processes     │    │ • Planning       │    │ • Dashboard      │
│   Needs_Action  │    │ • Approval Req.  │    │ • Monitoring     │
│ • Flags for     │    │ • MCP Draft      │    │ • Reporting      │
│   Approval      │    │ • Status Tracking│    │                  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Scheduling     │    │  Storage Folders │    │    Dashboard     │
│  System         │    │                  │    │                  │
│ • Daily         │    │ • Inbox          │    │ • Real-time      │
│   Summaries     │    │ • Needs_Action   │    │   Updates        │
│ • Weekly        │    │ • Pending_Approval│   │ • Status Indicators│
│   Reviews       │    │ • Approved/Reject│   │ • Activity Logs  │
└─────────────────┘    │ • Drafts         │    └──────────────────┘
                       │ • Done           │
                       │ • Plans          │
                       │ • Logs           │
                       └──────────────────┘
```

## Key Features

### 1. Multiple Watchers
- **File System Watcher**: Monitors the Inbox folder for new files
- **Gmail Watcher**: Simulates monitoring for new emails
- **Isolated Operation**: Each watcher operates independently
- **Structured Output**: Creates standardized task files in Needs_Action

### 2. Planning & Reasoning
- **Plan.md Generation**: Creates structured plans for multi-step tasks
- **Step-by-Step Checklists**: Includes detailed execution steps
- **Approval Points**: Identifies points requiring human approval
- **Storage in /Plans**: Organized plan management

### 3. MCP Server Integration
- **Draft Creation**: Handles email/message drafts via MCP
- **Safe Execution**: All sensitive actions drafted but not sent
- **Approval Requirement**: Drafts require manual approval to execute
- **Status Tracking**: Monitors draft status and progress

### 4. Human-in-the-Loop (HITL)
- **Pending_Approval**: Tasks requiring human review
- **Approved**: Human-approved tasks for execution
- **Rejected**: Human-rejected tasks
- **Manual Movement**: Humans move files between folders

### 5. Agent Skills
- **Modular Design**: Each capability as separate skill
- **Reusable Components**: Skills can be combined flexibly
- **Standard Interface**: Consistent input/output patterns
- **Safety Integration**: Built-in safety checks

### 6. Scheduling
- **Automated Reports**: Daily summaries and weekly reviews
- **Timestamp Checks**: Simulation-based scheduling
- **Recurring Tasks**: Regular maintenance activities
- **Configurable Intervals**: Adjustable timing for tasks

## Safety & Autonomy Boundaries

### What is Automated
- File system monitoring
- Basic task processing
- Plan generation
- Status updates
- Draft creation
- Schedule management

### What Requires Approval
- Sending emails/messages
- Financial transactions
- Deletion of important files
- Sharing confidential information
- Any irreversible actions

### What is Prohibited
- Auto-sending of any messages
- Payment processing
- Permanent deletion without approval
- Access to sensitive credentials
- Direct external API calls

## File Flow

```
Inbox → File_Watcher → Needs_Action → Task_Processor → Approval_Check →
  ↓                                    ↓                                  ↓
Draft_Creation ← Sensitive_Actions ← Pending_Approval ← Approval_Monitor
  ↓                                    ↓                                  ↓
Done ← Approved_Task_Processing ← Approved/Rejected ← Human_Move_File
```

## Implementation Details

### Watchers
Each watcher is implemented as a separate module that:
1. Monitors its source continuously
2. Creates structured task files when changes occur
3. Writes to Needs_Action folder in standardized format
4. Maintains logs for audit trail

### Approval System
The approval system works by:
1. Flagging sensitive tasks that require approval
2. Moving them to Pending_Approval folder
3. Waiting for human intervention (manual file movement)
4. Processing approved tasks, ignoring rejected ones

### MCP Integration
The MCP server provides:
1. Secure draft creation endpoints
2. Status checking capabilities
3. Safe storage of draft content
4. Integration points with approval system

### Scheduling
The scheduler handles:
1. Daily summary requests (every 24 hours)
2. Weekly review requests (every 7 days)
3. Configurable timing intervals
4. Persistent scheduling state