# Audit Generation Skill

## Purpose
Generates comprehensive audit reports and maintains audit trails for all system activities in the Gold Tier AI Employee system.

## Inputs
- `audit_period`: Time period for the audit (daily, weekly, monthly)
- `event_types`: Types of events to include in the audit
- `domains`: Specific domains to audit (communication, operations, accounting)
- `error_threshold`: Threshold for flagging problematic activities
- `compliance_checklist`: Checklist of compliance requirements to verify

## Outputs
- `audit_report`: Comprehensive audit report in markdown format
- `compliance_status`: Overall compliance status with requirements
- `flagged_activities`: List of activities that require attention
- `recommendations`: Actionable recommendations for system improvement
- `health_metrics`: Quantitative metrics about system health

## Functionality
1. Collects audit events from all system components
2. Aggregates data from multiple sources (logs, task completion, approvals)
3. Analyzes patterns and identifies anomalies
4. Generates CEO-style briefing reports
5. Flags non-compliant activities
6. Calculates system health metrics
7. Provides actionable recommendations

## Audit Collection Process
1. Gathers events from all component logs
2. Correlates events across different system components
3. Validates audit trail completeness
4. Checks for missing or inconsistent entries
5. Verifies timestamp accuracy and ordering
6. Ensures all required fields are populated

## Report Generation
1. Creates executive summary with key metrics
2. Analyzes task performance by category
3. Reviews error patterns and recovery effectiveness
4. Evaluates approval workflow efficiency
5. Assesses cross-domain coordination
6. Provides health indicators and recommendations

## Integration Points
- Reads from all component audit logs
- Integrates with Gold Auditor for weekly reports
- Connects with dashboard for real-time metrics
- Links to quarantine system for failed task analysis
- Coordinates with MCP servers for action tracking

## Safety Constraints
- Maintains immutable audit records
- Preserves privacy of sensitive information
- Ensures audit data integrity
- Prevents audit log tampering
- Maintains comprehensive coverage of all activities