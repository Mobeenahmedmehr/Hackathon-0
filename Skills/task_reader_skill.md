# Task Reader Skill

## Purpose
Reads and parses task files from the Needs_Action folder to extract instructions and metadata.

## Inputs
- `task_file_path`: Path to the task file to process

## Outputs
- `task_content`: Parsed content of the task
- `instructions`: Specific instructions from the task
- `metadata`: Task metadata including priority and type
- `success`: Boolean indicating successful parsing

## Functionality
1. Reads the markdown task file
2. Parses the content to extract instructions
3. Identifies task metadata (priority, type, etc.)
4. Validates the task structure
5. Returns structured data for further processing

## Safety Constraints
- Only processes files from authorized directories
- Validates file format before processing
- Does not execute arbitrary code from task files
- Logs all processed tasks for audit trail