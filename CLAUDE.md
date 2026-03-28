# CLAUDE.md - AI Employee System Guide

This document explains the entire AI Employee system architecture for Claude Code.

## Project Overview

This system is an AI Employee that can:
- Monitor Gmail and WhatsApp
- Detect leads or tasks
- Convert them into markdown tasks
- Generate action plans using AI
- Request human approval
- Execute actions using MCP tools
- Log everything for auditing

The system is built around a filesystem-based workflow that enables persistent, auditable operations with human oversight for safety.

## Core Architecture

### Filesystem Workflow
```
Watchers → Needs_Action → Plans → Pending_Approval → Approved → Execution → Done
```

### Folder Purposes

#### Needs_Action/
- Incoming tasks detected from watchers
- Tasks that require processing
- New communication or lead notifications

#### Plans/
- AI generated action plans
- Detailed steps for task execution
- Tool selection and parameter definitions

#### Pending_Approval/
- Plans waiting for human approval
- Tasks requiring human oversight
- Sensitive operations needing authorization

#### Approved/
- Plans approved by the human operator
- Ready for execution by the system
- Verified and authorized actions

#### Rejected/
- Plans rejected by the human operator
- Tasks that will not be executed
- Provides feedback for future improvements

#### Drafts/
- Generated drafts such as email replies or posts
- Prepared content awaiting final approval
- Pre-filled forms or documents

#### Done/
- Completed tasks
- Successfully executed operations
- Final state for successful operations

#### Logs/
- System activity logs
- Execution traces and debugging information
- Timestamped records of all operations

#### Reports/
- Weekly audit and analytics reports
- Performance metrics and system health
- Business intelligence summaries

## Core System Modules

### watchers/
- Responsible for monitoring external sources such as Gmail and WhatsApp
- Converts detected events into structured task files
- Implements source-specific connection and polling logic
- Handles authentication and API integration for each platform

### ai/
- Contains reasoning modules that use the Qwen API to generate plans
- Processes incoming tasks and creates executable action sequences
- Implements context understanding and decision-making logic
- Selects appropriate tools and parameters for each task

### core/
- Contains the main orchestrator loop that runs the AI employee
- Manages state transitions between different workflow stages
- Coordinates between different system components
- Handles error recovery and retry logic

### mcp_servers/
- Contains tool servers that allow the AI to perform actions such as sending emails or automating browsers
- Provides secure interfaces to external systems
- Implements rate limiting and safety constraints
- Handles authentication and session management for external services

### security/
- Handles cryptographic plan signing and verification
- Ensures plan integrity and authenticity
- Implements access controls and permission validation
- Manages encryption keys and secure storage

### auditor/
- Generates weekly performance reports
- Tracks system metrics and success rates
- Creates compliance and audit trails
- Analyzes system behavior and identifies trends

### dashboard/
- Provides a monitoring interface for system status
- Displays real-time activity and performance metrics
- Shows system health and error notifications
- Enables human operators to oversee operations

### config/
- Handles environment variables and configuration
- Manages API keys and service credentials
- Stores system-wide settings and parameters
- Implements configuration validation and loading

## Safety Rules

### Critical System Safety Rules

1. **AI must never execute actions without approval unless explicitly allowed**
   - All sensitive operations require explicit human approval
   - Default stance is to require approval for any external action
   - Exception rules must be clearly defined and limited

2. **All actions must be logged**
   - Every operation must be recorded in the Logs/ directory
   - Include timestamps, inputs, outputs, and execution results
   - Maintain immutable audit trails for compliance

3. **Sensitive credentials must only exist in environment variables**
   - No hardcoded credentials in source code
   - Use secure configuration management
   - Implement credential rotation policies

4. **Plans should be signed and verified before execution**
   - Cryptographic verification of all action plans
   - Prevent tampering with execution instructions
   - Maintain plan integrity from creation to execution

5. **Failed tasks must move to an error or quarantine state**
   - Implement proper error handling and recovery
   - Move failed tasks to quarantine for review
   - Prevent infinite retry loops on persistent failures

## AI Responsibilities

The AI system must:

1. **Read tasks** - Parse incoming task files and understand requirements
2. **Generate plans** - Create detailed action sequences using appropriate tools
3. **Select appropriate tools** - Choose the right MCP server for each action
4. **Request approval when needed** - Move plans to Pending_Approval when required
5. **Execute approved plans** - Run verified actions through MCP servers
6. **Log results** - Record all execution outcomes for auditing

The AI operates within the defined safety boundaries while maximizing autonomous operation for routine tasks.