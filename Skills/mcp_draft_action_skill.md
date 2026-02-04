# MCP Draft Action Skill

## Purpose
Integrates with the MCP server to create draft actions (emails, messages) that require human approval before sending.

## Inputs
- `action_type`: Type of draft action (email, message, etc.)
- `recipients`: List of recipients for the action
- `content`: Content of the draft
- `subject`: Subject/title of the draft
- `platform`: Platform for the action (email, Slack, etc.)

## Outputs
- `draft_id`: Unique identifier for the created draft
- `draft_path`: Path to the draft file
- `status`: Status of draft creation
- `success`: Boolean indicating successful draft creation

## Functionality
1. Connects to the MCP server to create draft actions
2. Creates draft files in the `/Drafts` directory
3. Ensures all drafts are in "DRAFT" status and not sent automatically
4. Adds clear warnings that drafts require approval before sending
5. Logs draft creation for audit trail

## Draft Creation Process
1. Calls MCP server with action details
2. Creates draft file with clear "DRAFT" status indicator
3. Includes prominent warnings that action has not been sent
4. Provides instructions for moving to approval process
5. Updates dashboard with draft count

## Safety Constraints
- No actions are sent automatically - all remain as drafts
- Draft files clearly marked as "DRAFT (Not Sent)"
- Explicit instructions for approval process included
- All draft creations are logged
- Prevents accidental sending of sensitive communications

## Integration Points
- Works with MCP server for draft creation
- Places drafts in `/Drafts` directory for review
- Integrates with approval workflow for sending after approval
- Updates dashboard with draft status