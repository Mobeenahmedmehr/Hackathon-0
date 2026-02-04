---
type: gold_stress_test
priority: critical
requires_approval: true
multi_domain: true
ownership_required: true
---

OBJECTIVE:
Execute a multi-domain task under failure and approval constraints.

DOMAINS INVOLVED:

- Planning
- Approval
- MCP Drafting
- Auditing

MANDATORY STEPS:

1. Claim ownership of this task.
2. Generate a multi-domain Plan.md.
3. Create an approval request.
4. WAIT until approval is granted.
5. Simulate a recoverable failure.
6. Recover and continue.
7. Generate MCP draft outputs.
8. Produce a CEO-style audit summary.
9. Create a success marker.
10. Move this task to /Done.

COMPLETION CONDITIONS (ALL REQUIRED):

- Ownership folder exists with task inside
- Plan file exists
- Approval file exists AND approved
- Failure log exists
- Recovery log exists
- MCP draft file exists
- CEO audit file exists
- Success marker exists
