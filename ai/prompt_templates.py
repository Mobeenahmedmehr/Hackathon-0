TASK_ANALYSIS_PROMPT = """
Analyze the following task and provide a structured assessment:

Task: {task_description}

Please provide your analysis in the following format:
- Goal: [Clear objective of the task]
- Task Type: [email / sales / linkedin / automation / research]
- Complexity: [simple / moderate / complex]
- Estimated Time: [minutes needed to complete]

Keep your analysis concise but thorough.
"""

PLAN_GENERATION_PROMPT = """
You are an AI task planner that creates detailed execution plans. Based on the following task information, create a structured plan:

Task Details:
- Source: {source}
- Sender: {sender}
- Description: {task_description}
- Raw Message: {raw_message}

Create a plan with the following sections:

Goal:
[Clear objective of the task]

Task Type:
[One of: email / sales / linkedin / automation / research]

Steps:
1. [First step]
2. [Second step]
3. [Third step]

Recommended Agent:
[One of: EmailAgent / SalesAgent / LinkedInAgent / AutomationAgent]

Tools Required:
[List the tools needed, e.g., gmail_mcp, linkedin_mcp, browser_mcp, file_tools]

Approval Required:
[yes / no]

Reasoning:
[Explain why this plan is correct and appropriate for the task]

Please provide only the structured plan with the sections above.
"""