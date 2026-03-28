# AI Employee System

**An Advanced AI-Powered Digital Employee for Automated Task Management**

A sophisticated AI employee system that monitors external sources, processes tasks autonomously, and executes actions with human oversight for safety. Built around a filesystem-based workflow that enables persistent, auditable operations across multiple domains.

## Overview

The AI Employee System is designed to:

- Monitor Gmail, WhatsApp, and other communication channels
- Detect leads, tasks, and opportunities automatically
- Convert detected items into structured markdown tasks
- Generate detailed action plans using AI reasoning
- Request human approval for sensitive operations
- Execute actions using secure MCP tools
- Maintain comprehensive logs for auditing and compliance

## Architecture

The system follows a state-based workflow architecture:

```
Watchers → Needs_Action → Plans → Pending_Approval → Approved → Execution → Done
```

### Core Workflow Folders:

- **Needs_Action/** - Incoming tasks detected by watchers
- **Plans/** - AI-generated action plans with tool selections
- **Pending_Approval/** - Plans awaiting human authorization
- **Approved/** - Verified plans ready for execution
- **Rejected/** - Plans declined by human operator
- **Drafts/** - Prepared content awaiting final approval
- **Done/** - Successfully completed tasks
- **Logs/** - Comprehensive system activity logs
- **Reports/** - Weekly audit and analytics reports

### System Modules:

- **watchers/** - Source monitoring (Gmail, WhatsApp, etc.)
- **ai/** - AI reasoning and plan generation modules
- **core/** - Main orchestration and workflow management
- **mcp_servers/** - Secure action execution tools
- **security/** - Cryptographic verification and access controls
- **auditor/** - Reporting and compliance auditing
- **dashboard/** - System monitoring interface
- **config/** - Environment configuration and credentials
- **agents/** - AI agent implementations
- **integrations/** - External service connectors
- **utils/** - Utility functions and helpers

## Key Features

### 🤖 Autonomous Operation

- Automatic detection of tasks and leads from multiple sources
- AI-powered plan generation with appropriate tool selection
- Persistent operation with state management
- Intelligent retry and error handling

### 🔐 Safety & Control

- Mandatory human approval for sensitive operations
- Cryptographic plan signing and verification
- Comprehensive logging of all activities
- Strict safety boundaries preventing unauthorized actions

### 📊 Auditing & Compliance

- Complete audit trails for all operations
- Weekly business reports and system health analysis
- Timestamped logs of all inputs, outputs, and decisions
- Chain of custody tracking for all processed items

### 🌐 Multi-Domain Integration

- Cross-platform monitoring (Gmail, WhatsApp, LinkedIn)
- Multi-channel communication capabilities
- Integration with external services via MCP tools
- Coordinated multi-step operations

## Safety Framework

The system implements robust safety measures:

1. **Approval Requirements** - All sensitive operations require explicit human authorization
2. **Immutable Logging** - Every action is recorded in the Logs/ directory
3. **Credential Security** - Sensitive credentials stored only in environment variables
4. **Plan Verification** - All action plans are cryptographically signed and verified
5. **Error Isolation** - Failed tasks move to quarantine for review and prevent infinite loops

## Getting Started

### Prerequisites

- Python 3.7+
- Access to external service APIs (Gmail, WhatsApp, etc.)
- MCP server configurations for action execution
- Environment variables for API keys and credentials

### Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env` file
4. Set up MCP server connections
5. Start the system: `python run_ai_employee.py`

### Running the System

```bash
# Start the main orchestrator
python core/orchestrator.py

# Monitor the dashboard
tail -f dashboard/status.md

# Check logs
tail -f Logs/system_$(date +%Y%m%d).log
```

## Project Structure

```
AI_Employee_Vault/
├── Needs_Action/          # Incoming detected tasks
├── Plans/                 # AI-generated action plans
├── Pending_Approval/      # Plans awaiting human approval
├── Approved/              # Authorized plans for execution
├── Rejected/              # Declined plans
├── Drafts/                # Prepared content awaiting approval
├── Done/                  # Successfully completed tasks
├── Logs/                  # System activity logs
├── Reports/               # Audit and analytics reports
├── Inbox/                 # Incoming communication monitoring
├── watchers/              # External source monitoring
├── ai/                    # AI reasoning modules
├── core/                  # Main orchestration logic
├── mcp_servers/           # Secure action execution tools
├── security/              # Cryptographic and access controls
├── auditor/               # Reporting and compliance tools
├── dashboard/             # Monitoring interface
├── config/                # System configuration
├── agents/                # AI agent implementations
├── integrations/          # External service connectors
└── utils/                 # Utility functions
```

## Development

### Adding New Watchers

Create new watcher modules in the `watchers/` directory to monitor additional sources. Each watcher should:

- Detect relevant events or communications
- Create structured task files in the `Needs_Action/` directory
- Handle authentication and API integration for the source

### Extending MCP Servers

Add new MCP server implementations in `mcp_servers/` to enable new types of actions. Each server should:

- Implement secure interfaces to external systems
- Include rate limiting and safety constraints
- Handle authentication and session management

### AI Plan Generation

The AI module in `ai/` generates executable action sequences by:

- Parsing incoming task requirements
- Selecting appropriate tools and parameters
- Creating detailed step-by-step execution plans
- Ensuring all safety requirements are met

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is part of a hackathon submission and intended for demonstration purposes.

## Contact

For questions about the AI Employee System, please open an issue in the repository.
