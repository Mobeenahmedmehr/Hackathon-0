# Plan Generation Skill (Enhanced)

## Purpose
Generates detailed, structured plans for multi-step tasks that require approval before execution.

## Inputs
- `objective`: The main goal or objective to achieve
- `steps`: List of required steps to complete the task
- `resources`: Resources needed for the task
- `timeline`: Estimated timeline for completion
- `approval_required`: Boolean indicating if human approval is needed

## Outputs
- `plan_file_path`: Path to the generated plan file
- `requires_approval`: Boolean indicating if the plan needs approval
- `success`: Boolean indicating successful plan generation

## Functionality
1. Creates a structured Plan.md file with:
   - Clear objective statement
   - Step-by-step checklist
   - Approval points (if required)
   - Resource requirements
   - Timeline estimates
   - Success criteria
2. Stores plans in the `/Plans` directory
3. Flags plans requiring human approval
4. Logs plan creation for audit trail

## Safety Constraints
- All plans requiring sensitive actions are flagged for approval
- Plans include safety checkpoints before sensitive operations
- Detailed documentation maintained for all planning activities
- Plans are stored locally and not transmitted externally

## Approval Integration
- Plans that include sensitive actions (sending messages, payments, etc.) are automatically flagged for approval
- Plan files include clear approval request sections
- Plan execution is paused until human approval is received