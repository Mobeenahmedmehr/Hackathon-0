# AGENTS.md - AI Employee System Agents

This document defines all AI agents inside the AI Employee system.

## OrchestratorAgent

### Role
Coordinates the entire AI employee system.

### Responsibilities
- Monitor task queues across all workflow stages
- Route tasks to specialized agents based on content and requirements
- Manage execution flow between different system components
- Handle error recovery and system state management
- Coordinate approval workflows and human interventions
- Ensure system health and operational continuity

## EmailAgent

### Role
Handles all Gmail related tasks.

### Responsibilities
- Analyze incoming emails and identify tasks or leads
- Draft appropriate replies based on email content and context
- Send approved responses through Gmail API
- Manage email threading and conversation continuity
- Extract relevant information from email threads
- Handle email attachments and embedded links

### Tools Used
- gmail_mcp (for email operations)

## WhatsAppAgent

### Role
Handles client communication via WhatsApp.

### Responsibilities
- Analyze incoming WhatsApp messages for leads or tasks
- Detect potential business opportunities in conversations
- Create response drafts for customer inquiries
- Manage WhatsApp conversation threads
- Identify priority messages requiring immediate attention
- Maintain contact lists and conversation history

### Tools Used
- browser_mcp or whatsapp automation (for messaging operations)

## LinkedInAgent

### Role
Handles LinkedIn outreach and posting.

### Responsibilities
- Generate engaging LinkedIn posts based on business goals
- Respond to comments and engagement on posts
- Send connection requests to potential prospects
- Monitor LinkedIn for business opportunities
- Track engagement metrics and post performance
- Manage LinkedIn profile updates and networking

### Tools Used
- linkedin_mcp (for LinkedIn operations)

## SalesAgent

### Role
Handles business leads.

### Responsibilities
- Qualify incoming leads based on business criteria
- Prepare personalized follow-up emails for qualified leads
- Schedule meetings and coordinate calendar availability
- Track lead progression through sales funnel
- Maintain CRM-style records of lead interactions
- Generate sales reports and performance metrics

## AutomationAgent

### Role
Handles browser automation tasks.

### Responsibilities
- Fill out online forms and applications
- Submit web-based requests and applications
- Automate repetitive browser-based workflows
- Navigate websites and extract relevant information
- Handle CAPTCHA and anti-bot measures appropriately
- Perform data entry and website interaction tasks

### Tools Used
- browser_mcp (for browser automation)

## AuditorAgent

### Role
Responsible for monitoring system performance.

### Responsibilities
- Generate weekly reports on system performance and activity
- Detect system failures and operational anomalies
- Analyze success metrics and identify improvement areas
- Create compliance reports for auditing purposes
- Monitor resource usage and system efficiency
- Track approval rates and human intervention frequency

Each agent operates within the safety constraints defined in the system architecture, ensuring all actions are properly logged, approved when necessary, and aligned with business objectives.