# Status Tracking Skill

## Purpose
Tracks the status of tasks, approvals, and drafts across the Silver Tier system to maintain visibility and accountability.

## Inputs
- `component`: Which system component to track (watchers, approvals, drafts, tasks)
- `status_filter`: Optional filter for specific statuses (pending, approved, rejected, etc.)
- `time_period`: Time period to track (today, week, month)

## Outputs
- `status_report`: Summary of current system status
- `counts`: Counts for each status category
- `recent_activity`: List of recent activities
- `alerts`: Any issues or pending items requiring attention

## Functionality
1. Monitors all system folders for current status
2. Tracks pending tasks in `/Needs_Action`
3. Monitors pending approvals in `/Pending_Approval`
4. Tracks approved and rejected items
5. Monitors draft status in `/Drafts`
6. Updates dashboard with real-time status
7. Generates status reports for system health monitoring

## Tracking Areas
- **Tasks**: Monitor `/Inbox`, `/Needs_Action`, `/Done`
- **Approvals**: Monitor `/Pending_Approval`, `/Approved`, `/Rejected`
- **Drafts**: Monitor `/Drafts` for pending actions
- **Watchers**: Track activity from all watcher types
- **Logs**: Aggregate system health from log files

## Dashboard Integration
- Updates task queue counts
- Shows approval queue status
- Displays draft count and status
- Reports system health indicators
- Highlights any system issues or alerts

## Safety Constraints
- All tracking is read-only to avoid interfering with operations
- Status updates are atomic to prevent race conditions
- Historical data preserved for audit trails
- No system state is modified by tracking activities
- Privacy maintained - only aggregate status information reported

## Reporting Features
- Real-time status updates
- Periodic summary reports
- Alert generation for unusual conditions
- Trend analysis for system optimization