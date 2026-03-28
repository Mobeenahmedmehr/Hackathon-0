# Component Details

## Watchers (`watchers/`)

### Purpose
The watchers module serves as the system's sensory layer, monitoring various communication channels and converting relevant events into structured tasks.

### Functionality
- Monitors communication platforms (email, Slack, Discord, etc.)
- Identifies relevant events based on predefined criteria
- Converts events into markdown-formatted task items
- Filters noise from relevant communication
- Maintains event logs for audit purposes

### Supported Channels
- Email inboxes
- Team collaboration platforms
- Social media feeds
- RSS feeds and news sources
- Project management tools

### Configuration
Watchers can be configured with:
- Keywords or phrases to trigger attention
- Sender/receiver whitelists
- Time-based filtering rules
- Priority levels for different event types

### Output Format
Events are converted to standardized markdown task formats that can be processed by the AI reasoning engine.

---

## AI Reasoning Engine (`ai/`)

### Purpose
The AI reasoning engine processes incoming tasks and generates appropriate action plans using advanced language models.

### Components
- **Task Analyzer**: Parses incoming tasks and extracts key information
- **Context Builder**: Gathers relevant context for decision making
- **Plan Generator**: Creates detailed action plans using Qwen API
- **Quality Validator**: Ensures plans meet safety and quality standards

### Planning Process
1. Task ingestion and parsing
2. Context gathering and analysis
3. Plan generation using Qwen API
4. Quality and safety validation
5. Plan formatting for approval workflow

### Integration Points
- Interfaces with Qwen API for reasoning capabilities
- Connects to MCP servers for action possibilities
- Links with security module for plan verification

---

## Core Orchestration (`core/`)

### Purpose
Manages the overall autonomous execution loop and coordinates between system components.

### Key Responsibilities
- Controls the autonomous decision-making cycle
- Manages state transitions between components
- Handles error recovery and fallback procedures
- Maintains execution context and history

### Execution Loop
1. Receive new tasks from watchers
2. Pass tasks to AI reasoning engine
3. Submit plans for human approval
4. Execute approved plans via MCP servers
5. Log results and update system state
6. Generate completion reports

### State Management
- Tracks pending, approved, and completed tasks
- Maintains execution history for auditing
- Manages concurrent task processing
- Handles resource allocation

---

## MCP Servers (`mcp_servers/`)

### Purpose
Provides safe, controlled interfaces for the AI to interact with external systems.

### Available Tools
- **Email Client**: Send and manage emails
- **Social Media**: Post on LinkedIn, Twitter, and other platforms
- **Browser Automation**: Interact with web interfaces safely
- **Calendar Integration**: Schedule and manage appointments
- **Document Generation**: Create and modify documents
- **Database Access**: Query and update data stores (read/write)

### Security Measures
- Each tool has defined permission boundaries
- Actions are logged and auditable
- Rate limiting prevents abuse
- Input sanitization prevents injection attacks

### Configuration
- Per-tool permission levels
- Rate limiting parameters
- Connection timeouts and retries
- Error handling and fallbacks

---

## Security Layer (`security/`)

### Purpose
Ensures all actions are properly authenticated, authorized, and verified before execution.

### Components
- **Cryptographic Signing**: Signs all action plans before execution
- **Verification Module**: Validates plan authenticity
- **Access Control**: Manages permissions for different operations
- **Audit Trail**: Maintains records of all security-related events

### Signing Process
1. Action plan is prepared by AI reasoning engine
2. Plan is cryptographically signed using private key
3. Signature is validated before execution
4. Invalid signatures prevent plan execution

### Verification Checks
- Plan integrity verification
- Permission level validation
- Safety constraint checking
- Anomaly detection

---

## Auditor (`auditor/`)

### Purpose
Generates comprehensive reports on system performance, activities, and outcomes.

### Report Types
- **Weekly Business Reports**: Executive summaries of AI activities
- **Performance Metrics**: Efficiency and effectiveness measurements
- **Activity Logs**: Detailed records of all actions taken
- **Compliance Reports**: Adherence to safety and approval protocols

### Data Collection
- Task completion rates
- Approval times and patterns
- Error frequencies and types
- Resource utilization metrics

### Reporting Schedule
- Daily activity summaries
- Weekly comprehensive reports
- Monthly trend analysis
- Ad-hoc reports on demand

---

## Dashboard (`dashboard/`)

### Purpose
Provides real-time visibility into system health, status, and activity.

### Key Metrics
- System uptime and availability
- Task processing queue status
- Recent activity feed
- Performance indicators
- Error rate monitoring

### Features
- Real-time system status indicators
- Historical performance charts
- Alert and notification system
- Drill-down capability for detailed analysis
- Export functionality for reports

### Access Levels
- Executive view: High-level metrics and summaries
- Operations view: Detailed system status and controls
- Audit view: Complete activity logs and compliance data