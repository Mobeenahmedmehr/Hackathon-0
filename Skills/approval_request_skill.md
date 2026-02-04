# Approval Request Skill

## Purpose
Creates approval request files for sensitive actions that require human oversight before execution.

## Inputs
- `action_details`: Description of the action requiring approval
- `sensitivity_level`: Level of sensitivity (Low, Medium, High)
- `required_approver`: Role or person who should approve
- `deadline`: Deadline for approval decision
- `justification`: Reason why approval is needed

## Outputs
- `approval_request_file`: Path to the created approval request file
- `status`: Status of the approval request creation
- `success`: Boolean indicating successful creation

## Functionality
1. Creates a structured approval request in the `/Pending_Approval` folder
2. Includes all relevant action details for informed decision-making
3. Specifies required actions (approve/reject) with clear instructions
4. Logs the approval request for audit trail
5. Updates dashboard with pending approval status

## Approval Workflow
1. Creates approval request file with detailed action information
2. Places file in `/Pending_Approval` directory
3. Waits for human to move file to either `/Approved` or `/Rejected`
4. Processes approved actions or cancels rejected actions

## Safety Constraints
- Only sensitive actions trigger approval requests
- Approval requests include all necessary context for informed decisions
- No actions are executed without proper approval
- All approval requests are logged for audit trail
- Clear instructions provided for approval/rejection process

## Integration Points
- Integrates with task processor to intercept sensitive actions
- Updates dashboard with pending approval count
- Works with approval monitor to process decisions