# File Mover Skill

## Purpose
Moves processed task files between folders (Needs_Action → Done) and manages file lifecycle.

## Inputs
- `source_path`: Path to the source file to move
- `destination_folder`: Destination folder (e.g., "Done", "Archive")
- `reason`: Reason for the move (for logging)

## Outputs
- `success`: Boolean indicating successful move
- `new_path`: Path of the moved file
- `log_message`: Description of the action taken

## Functionality
1. Validates source file exists
2. Creates destination folder if needed
3. Moves the file to the destination
4. Updates logs with the move operation
5. Returns confirmation of the operation

## Safety Constraints
- Only moves files between authorized folders
- Preserves file integrity during move
- Logs all operations for audit trail
- Validates destination paths before moving
- Maintains original filename for traceability