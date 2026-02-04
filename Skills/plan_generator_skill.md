# Plan Generator Skill

## Purpose
Generates structured markdown plans based on input requirements and constraints.

## Inputs
- `requirements`: List of requirements for the plan
- `constraints`: Constraints and limitations for the plan
- `resources`: Available resources for plan execution
- `timeline`: Timeline expectations if applicable

## Outputs
- `plan_content`: Generated plan in markdown format
- `plan_path`: Path where the plan was saved
- `success`: Boolean indicating successful generation

## Functionality
1. Analyzes input requirements and constraints
2. Creates a structured plan with objectives and steps
3. Formats the plan in markdown with proper headings
4. Saves the plan to the Plans folder
5. Updates dashboard with new plan information

## Safety Constraints
- Only generates plans based on provided inputs
- Does not execute plan steps automatically
- Maintains proper markdown formatting
- Validates input parameters before processing
- Logs plan generation for audit trail