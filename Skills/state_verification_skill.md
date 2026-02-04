# State Verification Skill

## Purpose
Verifies the completion state of tasks using file-state-based verification rather than relying on text claims, ensuring true completion in the Gold Tier AI Employee system.

## Inputs
- `task_id`: Identifier of the task to verify
- `expected_outputs`: List of expected output files or artifacts
- `verification_criteria`: Specific criteria for verifying completion
- `completion_markers`: File-based markers indicating completion
- `state_dependencies`: Other states this task depends on
- `verification_timeout`: Maximum time to wait for state verification

## Outputs
- `verification_result`: Whether the task is truly completed
- `verified_outputs`: List of actually verified outputs
- `missing_artifacts`: Any expected outputs that are missing
- `state_consistency`: Assessment of state consistency
- `completion_confidence`: Confidence level in completion verification
- `verification_log`: Detailed log of verification process

## Functionality
1. Checks for presence of expected output files
2. Validates file integrity and content correctness
3. Verifies completion markers in designated directories
4. Confirms absence of error indicators
5. Validates state dependencies are satisfied
6. Performs consistency checks across related files
7. Generates confidence score for completion verification
8. Maintains verification audit trail

## Verification Process
1. Locates all expected output artifacts based on task definition
2. Checks file existence, size, and basic integrity
3. Validates file content against expected patterns
4. Verifies completion markers in appropriate directories
5. Confirms no error or failure indicators are present
6. Checks related files for consistency
7. Validates state dependencies are properly resolved
8. Generates completion confidence assessment

## File-State Verification Methods
1. **Existence Check**: Verifies expected files are present
2. **Size Validation**: Confirms files are not empty or truncated
3. **Pattern Matching**: Validates file content structure
4. **Marker Verification**: Checks for completion indicators
5. **Dependency Validation**: Ensures prerequisite states are met
6. **Consistency Check**: Verifies related files align properly

## Domain-Specific Verification
### Communication Domain
- Verifies draft files were properly created
- Confirms approval workflow completion
- Validates recipient lists and content

### Operations Domain
- Checks that files were properly processed
- Verifies directory structures are correct
- Confirms data integrity after operations

### Accounting/Tracking Domain
- Validates log entries were created
- Confirms audit trails are complete
- Verifies metrics were properly recorded

## Integration Points
- Connects with task processor for verification triggers
- Integrates with all domain-specific verifiers
- Coordinates with audit system for verification logging
- Links to dashboard for completion status updates
- Communicates with quarantine system for failed verifications

## Safety Constraints
- Uses read-only operations during verification
- Maintains verification independence from creation process
- Preserves original state during verification
- Prevents verification from altering system state
- Ensures verification accuracy regardless of timing
- Maintains audit trail of all verification activities