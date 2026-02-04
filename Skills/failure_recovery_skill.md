# Failure Recovery Skill

## Purpose
Handles failure recovery for tasks that have failed during processing, implementing retry logic, backoff strategies, and quarantine procedures.

## Inputs
- `task_id`: Identifier of the failed task
- `error_type`: Classification of the error (transient, auth, logic, system)
- `error_details`: Specific details about the error that occurred
- `retry_count`: Number of previous retry attempts
- `quarantine_reason`: Reason for potential quarantine if retries exhausted

## Outputs
- `recovery_action`: Action to take (retry, quarantine, escalate, skip)
- `retry_delay`: Delay before next retry attempt (if applicable)
- `quarantined`: Boolean indicating if task was quarantined
- `recovery_notes`: Notes about the recovery process

## Functionality
1. Analyzes the error type and details to determine appropriate recovery strategy
2. Implements exponential backoff for transient errors
3. Quarantines tasks with logic or system errors after max retries
4. Prompts for human intervention for auth errors
5. Updates audit logs with recovery actions taken

## Recovery Strategies
1. **Transient Errors**: Retry with exponential backoff (2^retry_count * base_delay)
2. **Authentication Errors**: Flag for human intervention
3. **Logic Errors**: Quarantine after max retries with error details
4. **System Errors**: Retry with longer delays, quarantine if persistent

## Integration Points
- Works with Gold Task Processor for error handling
- Updates audit logs with recovery actions
- Interacts with quarantine system for failed tasks
- Provides escalation pathways for unresolvable errors

## Safety Constraints
- Respects max retry limits to prevent infinite loops
- Maintains audit trail of all recovery attempts
- Preserves original task data during recovery
- Prevents retry storms with appropriate backoff
- Ensures failed tasks don't block system operations