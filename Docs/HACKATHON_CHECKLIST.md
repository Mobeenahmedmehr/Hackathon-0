# Hackathon Submission Checklist

## Platinum Tier AI Employee Verification

### Judge Verification Steps

Follow these steps to verify the system meets all requirements:

#### 1. Autonomy Verification
- [ ] Start the system: `python run_platinum_tier.py`
- [ ] Place a simple task in `/Inbox/` (e.g., create a text file with basic instructions)
- [ ] Observe automatic processing without human intervention
- [ ] Confirm task moves through system: Inbox → Cloud → Local → Done

#### 2. Control Verification
- [ ] Place a task requiring email sending in `/Inbox/`
- [ ] Verify system creates approval request in `/Pending_Approval/`
- [ ] Confirm task requires human approval before execution
- [ ] Move file to `/Approved/` to continue processing

#### 3. Recovery Verification
- [ ] Check `/Logs/` for error handling and retry mechanisms
- [ ] Look for files in `/Quarantined/` if any errors occurred
- [ ] Verify system continues operating after errors

#### 4. Audit Verification
- [ ] Examine `/Logs/gold_audit_[date].log` for comprehensive logging
- [ ] Verify each action has timestamp, action type, input, output, approval status
- [ ] Confirm audit trail for the demo scenario

#### 5. Demo Reproduction
- [ ] Follow the steps in `/Demo/END_TO_END_DEMO.md`
- [ ] Verify all file transitions occur as documented
- [ ] Confirm final output matches expectations

### System Status Check

#### Platinum Tier Features:
- [ ] Cloud + Local split architecture functioning
- [ ] Cryptographic plan signing and verification
- [ ] Zero-trust enforcement between components
- [ ] Persistent Platinum Ralph Wiggum loop
- [ ] Human-in-the-Loop approval workflow

#### Backward Compatibility:
- [ ] Gold Tier functionality preserved
- [ ] All previous tiers continue to work
- [ ] No breaking changes to existing components

### Quick Test Commands

```bash
# Start the system
python run_platinum_tier.py

# Create a simple test task
echo "# Test Task

## Instructions
Create a simple summary of system status.

" > Inbox/test_task_$(date +%s).md

# Check dashboard for status updates
cat Dashboard.md
```

### Expected Outcomes

After running the demo:
1. Task should progress through Cloud → Local pipeline
2. Approval required for sensitive operations
3. Audit log should contain complete trail
4. Dashboard should update with task status
5. Final output in `/Done/` folder