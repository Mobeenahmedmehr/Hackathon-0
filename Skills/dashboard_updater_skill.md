# Dashboard Updater Skill

## Purpose
Updates the Dashboard.md file with current status, task counts, and system health information.

## Inputs
- `status_updates`: Dictionary of status updates to apply
- `task_counts`: Information about pending/completed tasks
- `system_health`: Current system health indicators

## Outputs
- `success`: Boolean indicating successful update
- `updated_sections`: List of sections that were updated
- `dashboard_path`: Path to the updated dashboard file

## Functionality
1. Reads the current dashboard file
2. Updates task counts and status indicators
3. Refreshes system health information
4. Updates timestamp information
5. Writes the updated dashboard file

## Safety Constraints
- Only updates predefined sections of the dashboard
- Preserves existing dashboard structure
- Validates all updates before applying
- Maintains markdown formatting integrity
- Logs dashboard updates for audit trail