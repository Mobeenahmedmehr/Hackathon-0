# Platinum Tier AI Employee - End-to-End Demo

## Hero Scenario: Personal Operations Assistant

### Input Task
Create a task file in the Inbox to schedule a team meeting and send invitations.

**File:** `/Inbox/demo_team_meeting_task.md`
```markdown
# Team Meeting Scheduler

## Instructions
Schedule a team meeting for next Tuesday at 2 PM EST with all team members.
Send calendar invites to: alice@company.com, bob@company.com, charlie@company.com
Include agenda: project status, upcoming deadlines, resource allocation.

## Priority
High - please schedule within 24 hours
```

### File Transitions

#### Step 1: Inbox Detection
- **From:** `/Inbox/demo_team_meeting_task.md`
- **Action:** File watcher detects new task
- **To:** Moved to `/Cloud/Incoming_Tasks/cloud_task_[timestamp]_demo_team_meeting_task.md`

#### Step 2: Cloud Planning
- **From:** `/Cloud/Incoming_Tasks/cloud_task_[timestamp]_demo_team_meeting_task.md`
- **Action:** Cloud Planner Agent generates multi-domain plan and signs it
- **To:** `/Cloud/Signed_Plans/signed_plan_[timestamp]_demo_team_meeting_task.md`

**Sample Plan Content:**
```markdown
# Multi-Domain Plan: Team Meeting Scheduler

Generated on: 2026-02-05T14:30:00

## Objective
Schedule the requested team meeting and send invitations.

## Domains Involved
- Communication
- Operations

## Plan Steps
1. Analyze the requirements
2. Identify necessary resources across domains
3. Execute the planned actions in sequence
4. Verify completion of each step
5. Document results and outcomes

[... rest of plan ...]

<!-- PLATINUM_SIGNATURE_START -->
<!-- Content Hash: a1b2c3d4e5f6... -->
<!-- HMAC Signature: x7y8z9... -->
<!-- Signed At: 2026-02-05T14:30:01 -->
<!-- Signer: Platinum_Cloud_Agent -->
<!-- Algorithm: SHA256-HMAC -->
<!-- Source: CloudPlannerAgent -->
<!-- Tier: Platinum -->
<!-- PLATINUM_SIGNATURE_END -->
```

#### Step 3: Local Execution (Approval Required)
- **From:** `/Cloud/Signed_Plans/signed_plan_[timestamp]_demo_team_meeting_task.md`
- **Action:** Local Executor detects plan requires human approval due to email sending
- **To:** `/Pending_Approval/platinum_approval_request_[timestamp]_demo_team_meeting_task.md`

#### Step 4: Human Approval
- **From:** `/Pending_Approval/platinum_approval_request_[timestamp]_demo_team_meeting_task.md`
- **Action:** Human reviewer approves by moving file
- **To:** Move to `/Approved/approved_[timestamp]_platinum_approval_request_[timestamp]_demo_team_meeting_task.md`

#### Step 5: Final Execution
- **From:** Approved status triggers Local Executor
- **Action:** Execute plan in draft-only mode (creates calendar invite draft)
- **To:** `/Local/Executed_Actions/executed_[timestamp]_demo_team_meeting_task.md` and `/Done/done_[timestamp]_demo_team_meeting_task.md`

### Final Output
- Calendar invitation draft created in `/Drafts/`
- Audit log entry in `/Logs/gold_audit_20260205.log`
- Dashboard updated showing task completion
- Confirmation in `/Done/` folder

### Verification Points
1. Check `/Logs/gold_audit_20260205.log` for complete audit trail
2. Verify signature in the signed plan file
3. Confirm approval workflow was triggered
4. Verify final task appears in `/Done/` folder
5. Check dashboard status update