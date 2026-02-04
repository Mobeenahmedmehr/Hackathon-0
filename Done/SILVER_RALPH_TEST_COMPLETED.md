---
type: silver_persistence_test
priority: high
status: pending
requires_approval: true
---

OBJECTIVE:
Demonstrate a multi-step Silver Tier workflow with persistence.

REQUIRED STEPS:

1. Generate a Plan.md with at least 3 steps.
2. Create an approval request file.
3. WAIT until human approval is given.
4. After approval, generate a draft action using MCP (draft-only).
5. Create a success marker file.
6. Move this task to /Done.

COMPLETION CONDITIONS (ALL REQUIRED):

- A plan exists in /Plans
- An approval file exists in /Pending_Approval
- Approval file is moved to /Approved
- MCP draft file exists
- Success marker file exists in /Done
