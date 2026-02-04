# Task Processor Skill

## Purpose
Processes structured task files by interpreting instructions and executing appropriate actions.

## Inputs
- `task_file_path`: Path to the task file to process
- `task_data`: Parsed task data from the reader skill

## Outputs
- `result`: Result of the task processing
- `actions_taken`: List of actions performed
- `next_steps`: Recommended next steps
- `success`: Boolean indicating successful processing

## Functionality
1. Interprets the task instructions
2. Determines appropriate actions based on task type
3. Calls other skills as needed (file mover, dashboard updater, etc.)
4. Records the outcome of processing
5. Prepares for task completion and file movement

## Safety Constraints
- Only executes actions consistent with task instructions
- Does not perform unauthorized operations
- Maintains audit trail of all actions
- Validates task structure before processing
- Respects company handbook constraints