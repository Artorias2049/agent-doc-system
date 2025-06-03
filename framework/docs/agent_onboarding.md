# Agent Documentation System - THE PROTOCOL

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "3.3.0"
  status: "Active"
  owner: "DocSystemAgent"
  title: "Agent Documentation System - THE PROTOCOL v3.3"
  description: "THE PROTOCOL v3.3: SpacetimeDB-powered multi-agent coordination with database name corrections and verified overseer-system architecture"
content:
  overview: "Single source of truth for the agent documentation system with SpacetimeDB real-time coordination and user supreme authority."
  key_components: "SpacetimeDB Overseer System, Documentation Protocol, Real-time Coordination, User Authority, Agent Management, Documentation Templates"
  sections:
    - title: "Overview"
      content: "This document serves as THE PROTOCOL - the single source of truth for understanding the SpacetimeDB-powered agent-doc-system."
    - title: "SpacetimeDB Architecture"
      content: "Real-time coordination with overseer-system database, user supreme authority, and agent management"
    - title: "Required Practices"
      content: "Documentation Structure, Metadata, SpacetimeDB Connection, Agent Registration"
    - title: "Agent Setup"
      content: "Agent name setup, SpacetimeDB connection, arrival announcement, documentation creation"
    - title: "Best Practices"
      content: "Documentation, Validation, Real-time Coordination"
    - title: "Getting Started"
      content: "Setup agent name, connect to SpacetimeDB, announce arrival, create documentation, validate"
    - title: "Quickstart Checklist"
      content: "Agent name, SpacetimeDB connection, documentation creation, validation"
    - title: "Changelog"
      content: "3.3.0 (2025-06-03): Database name corrections and verified overseer-system integration"
  changelog:
    - version: "3.3.0"
      date: "2025-06-03"
      changes:
        - "Critical database name correction: mcp-agent-system → overseer-system"
        - "Updated all SpacetimeDB command references to use correct database name"
        - "Verified all reducer calls and connection strings"
        - "Fixed documentation inconsistencies identified by Claude-MCP-Research"
        - "Ensured complete alignment with deployed overseer-system architecture"
    - version: "3.2.0"
      date: "2025-06-03"
      changes:
        - "Complete 16-table SpacetimeDB overseer-system architecture"
        - "Updated agent ID format: {type}_{function}_{timestamp}"
        - "Verified connection endpoint: http://127.0.0.1:3000"
        - "Updated PATH export to $HOME/.local/bin:$PATH"
        - "Added agent_registry, agent_hierarchy, workflow_steps, task_queue tables"
        - "Added coordination_locks, health_metrics, system_alerts, session_management tables"
        - "Updated with Claude-MCP-Research verified specifications"
        - "Ready for production migration to SpacetimeDB overseer-system"
    - version: "3.1.0"
      date: "2025-06-03"
      changes:
        - "Updated with deployed SpacetimeDB overseer-system specifications"
        - "Added user_directives and user_audit_log tables (8-table architecture)"
        - "Documented agent registration parameters and ID formats"
        - "Added connection string format and PATH export requirements"
        - "Included reducer function references for agent operations"
        - "Verified deployment specifications from Claude-MCP-Research"
    - version: "3.0.0"
      date: "2025-06-03"
      changes:
        - "SpacetimeDB overseer-system integration for real-time coordination"
        - "User supreme authority (priority 255) implementation"
        - "15 MCP tools with complete input/output schemas"
        - "Real-time subscriptions and event sourcing"
        - "6-table database architecture (users, agents, workflows, user_overrides, system_events, user_notifications)"
        - "Agent registration and communication via SpacetimeDB reducers"
        - "Emergency halt capability and complete audit trail"
        - "Sub-microsecond response time with WebAssembly backend"
        - "Single SpacetimeDB platform for all agent coordination"
        - "SpacetimeDB CLI authentication and connection management"
        - "Documentation system integration with real-time database"
        - "Complete SpacetimeDB architecture implementation"
    - version: "2.5.0"
      date: "2025-06-03"
      changes:
        - "Enhanced metadata system for dashboard integration"
        - "AI feedback system with quality scoring"
        - "Documentation cleanup and template consolidation"
        - "Improved validation scripts and framework protection"
    - version: "1.0.0"
      date: "2024-03-21"
      changes:
        - "Initial release of THE PROTOCOL"
feedback:
  rating: 98
  comments: "Revolutionary SpacetimeDB integration with comprehensive real-time coordination and user supreme authority."
  observations:
    - what: "Complete architectural upgrade to SpacetimeDB with real-time capabilities."
      impact: "Dramatic improvement in agent coordination and user control."
      priority: "high"
      category: "architecture"
  suggestions:
    - action: "Continue monitoring SpacetimeDB performance and agent adoption."
      priority: "medium"
      effort: "ongoing"
      impact: "high"
      assignee: "DocSystemAgent"
  status:
    value: "approved"
    updated_by: "DocSystemAgent"
    date: "2025-06-03"
    validation: "passed"
    implementation: "complete"
```

## Overview

This document serves as THE PROTOCOL v3.3 - the single source of truth for understanding the SpacetimeDB-powered agent documentation system with real-time coordination and user supreme authority.

Version 3.3 provides the complete 16-table architecture for **SpacetimeDB overseer-system** - a revolutionary real-time database with sub-microsecond response times, complete audit trails, and user supreme authority (priority 255). SpacetimeDB is the single coordination platform for all agent operations.

This document provides comprehensive guidance for agent setup, SpacetimeDB connection, documentation creation, and real-time collaboration within the overseer-system architecture.

## SpacetimeDB Architecture

### Overseer-System Database

**SpacetimeDB overseer-system** is the heart of the v3.0 architecture:

- **Database Name:** `overseer-system`
- **Connection:** `SPACETIME_URI=http://127.0.0.1:3000`
- **Authentication:** SpacetimeDB CLI (`spacetime identity`)
- **Performance:** Sub-microsecond response times with WebAssembly backend
- **Real-time:** Event sourcing and instant subscriptions
- **Authority:** User supreme authority (priority 255)

### Database Schema (16 Tables)

1. **users** - `user_id(String), username(String), display_name(String), authority_level(String), created_at(Timestamp), preferences(String)`
2. **user_overrides** - `override_id(String), user_id(String), override_type(String), target_id(String), action(String), reason(String), timestamp(Timestamp), priority(i32)`
3. **user_directives** - `directive_id(String), user_id(String), directive_type(String), target_agents(String), content(String), priority(u8), expires_at(Timestamp), created_at(Timestamp)`
4. **user_audit_log** - `log_id(u64), user_id(String), action_type(String), target_type(String), target_id(String), before_state(String), after_state(String), timestamp(Timestamp)`
5. **agent_registry** - `agent_id(String), agent_name(String), agent_type(String), supervisor_id(String), status(String), registered_at(Timestamp), last_heartbeat(Timestamp), config(String)`
6. **agent_hierarchy** - `hierarchy_id(String), parent_agent(String), child_agent(String), relationship_type(String), created_at(Timestamp), metadata(String)`
7. **system_events** - `event_id(String), event_type(String), source_agent(String), target_agent(String), timestamp(Timestamp), data(String), priority(i32)`
8. **workflows** - `workflow_id(String), workflow_type(String), status(String), initiator_agent(String), assigned_agents(String), created_at(Timestamp), completed_at(Timestamp), metadata(String)`
9. **workflow_steps** - `step_id(String), workflow_id(String), step_name(String), step_order(i32), assigned_agent(String), status(String), input_data(String), output_data(String), started_at(Timestamp), completed_at(Timestamp)`
10. **task_queue** - `task_id(String), agent_id(String), task_type(String), priority(i32), payload(String), status(String), created_at(Timestamp), assigned_at(Timestamp), completed_at(Timestamp)`
11. **coordination_locks** - `lock_id(String), resource_id(String), locked_by(String), lock_type(String), acquired_at(Timestamp), expires_at(Timestamp), metadata(String)`
12. **agent_subscriptions** - `subscription_id(String), agent_id(String), event_pattern(String), callback_url(String), is_active(bool), created_at(Timestamp), last_triggered(Timestamp)`
13. **user_notifications** - `notification_id(String), user_id(String), notification_type(String), severity(String), title(String), message(String), timestamp(Timestamp), read(bool)`
14. **health_metrics** - `metric_id(String), agent_id(String), metric_name(String), metric_value(String), timestamp(Timestamp), status(String)`
15. **system_alerts** - `alert_id(String), alert_type(String), severity(String), source(String), message(String), created_at(Timestamp), resolved_at(Timestamp), status(String)`
16. **session_management** - `session_id(String), agent_id(String), session_type(String), started_at(Timestamp), last_activity(Timestamp), status(String), connection_info(String)`

### MCP Tools Integration

**15 MCP Tools Available:**
- **5 User Authority Tools** (priority 255) - Supreme user control
- **3 Agent Management Tools** - Agent registration and coordination
- **2 Workflow Tools** - Multi-agent workflow orchestration
- **2 Communication Tools** - Real-time messaging and notifications
- **3 Resource Providers** - Data access and management

### Critical Features

- **User Supreme Authority** (priority 255) - Users have ultimate control
- **Real-time Coordination** - Instant agent synchronization
- **Complete Audit Trail** - Every action tracked and logged
- **Emergency Halt Capability** - System-wide emergency stops
- **Event Sourcing** - Complete state reconstruction capability

## Framework Usage Pattern

**IMPORTANT**: This framework is designed to be cloned into your projects as a subdirectory.

### Nested Usage Pattern (Standard)
When you clone this framework into your project, the structure will be:
```
your-project/                    # Your project root
├── src/                        # Your project source code
├── package.json               # Your project dependencies
└── agent-doc-system/          # The cloned framework
    ├── framework/             # 🚫 READ-ONLY (managed by DocSystemAgent)
    │   ├── docs/             # Framework documentation
    │   ├── schemas/          # Validation schemas
    │   ├── scripts/          # Utility scripts
    │   └── validators/       # Validation tools
    ├── project_docs/         # ✅ YOUR documentation goes here
    └── README.md            # Framework overview
```

### Key Points:
1. **Documentation Location**: Create all your documentation in `{project_root}/agent-doc-system/project_docs/`
2. **Framework is READ-ONLY**: The `agent-doc-system/framework/` directory should never be modified
3. **Scripts Usage**: Run scripts from your project root:
   ```bash
   ./agent-doc-system/framework/scripts/create_doc.sh project "My Doc" --owner "YourAgent"
   ```
4. **SpacetimeDB Connection**: All agents connect to the same overseer-system database
5. **Search-Friendly**: All documentation system files are under `agent-doc-system/` for easy discovery

## Key Components

### 1. SpacetimeDB Connection System
- **Purpose:** Real-time database connectivity with user supreme authority
- **Connection Details:**
  - Endpoint: `http://127.0.0.1:3000`
  - Authentication: `spacetime identity` CLI authentication
  - Client: SpacetimeDB CLI + Python subprocess calls via MCP
- **Key Features:**
  - Sub-microsecond response times
  - Real-time subscriptions and event sourcing
  - Complete audit trail with user authority (priority 255)
  - Emergency halt and rollback capabilities

### 2. Agent Registration and Management
- **Purpose:** Centralized agent coordination via SpacetimeDB overseer-system
- **Registration Process:**
  ```python
  import subprocess
  import json
  import uuid
  from datetime import datetime
  
  def register_agent(agent_name, agent_type="documentation", supervisor_id=""):
      """Register agent in SpacetimeDB overseer-system"""
      # Agent ID format: {type}_{function}_{number}
      agent_id = f"{agent_type}_{agent_name.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
      
      # Register using register_agent reducer
      result = subprocess.run([
          "spacetime", "call", "overseer-system", "register_agent",
          "--agent_id", agent_id,
          "--agent_name", agent_name,
          "--agent_type", agent_type,
          "--supervisor_id", supervisor_id,
          "--status", "active"
      ], capture_output=True, text=True)
      
      if result.returncode == 0:
          print(f"✅ {agent_name} registered with ID: {agent_id}")
          return agent_id
      else:
          print(f"❌ Registration failed: {result.stderr}")
          return None
  
  # Register your agent
  agent_id = register_agent("YourAgentName", "documentation", "")
  ```
- **Agent Management Features:**
  - Real-time status monitoring
  - Heartbeat tracking
  - Supervisor assignment
  - Configuration management
  - Activity logging

### 3. Workflow Coordination
- **Purpose:** Multi-agent workflow orchestration via SpacetimeDB
- **Workflow Management:**
  ```python
  def create_workflow(workflow_name, steps, assigned_agents):
      """Create workflow in SpacetimeDB overseer-system"""
      result = subprocess.run([
          "spacetime", "call", "overseer-system", "create_workflow",
          "--workflow_name", workflow_name, "--steps", json.dumps(steps), "--assigned_agents", json.dumps(assigned_agents)
      ], capture_output=True, text=True)
      
      return result.returncode == 0
  
  # Example: Documentation workflow
  create_workflow(
      "documentation_review",
      [{"step": "validate", "agent": "DocSystemAgent"},
       {"step": "review", "agent": "ReviewAgent"}],
      ["DocSystemAgent", "ReviewAgent"]
  )
  ```
- **Workflow Features:**
  - Real-time status tracking
  - Agent assignment and coordination
  - Step-by-step execution monitoring
  - Completion timestamps and metadata
  - Workflow chaining and dependencies

### 4. User Authority System
- **Purpose:** User supreme authority (priority 255) with override capabilities
- **Authority Features:**
  - **Priority 255**: Highest priority level in the system
  - **Override Capability**: Users can override any agent action
  - **Emergency Halt**: System-wide emergency stop functionality
  - **Audit Trail**: Complete logging of all authority actions
- **User Override Example:**
  ```python
  def user_override(user_id, target_id, action, reason):
      """Execute user override with supreme authority"""
      result = subprocess.run([
          "spacetime", "call", "overseer-system", "user_override",
          "--user_id", user_id, "--target_id", target_id, "--action", action, "--reason", reason, "--priority", "255"
      ], capture_output=True, text=True)
      
      return result.returncode == 0
  
  # Example: Emergency halt
  user_override(
      "admin_user", 
      "system_wide", 
      "emergency_halt", 
      "Critical security issue detected"
  )
  ```

### 5. Documentation Protocol
- **Purpose:** Structured documentation with comprehensive metadata validation
- **Key Files:**
  - [Document Protocol Schema](../schemas/document_protocol.yml)
  - [Enhanced Feedback Schema](../schemas/enhanced_feedback_schema.yml)
- **Required Document Structure:**
  ```markdown
  # Document Title
  
  ## Machine-Actionable Metadata
  ```yaml
  metadata:
    schema: "https://schema.org/TechnicalDocument"
    version: "1.0.0"
    status: "Active"
    owner: "YourAgentName"
    title: "Document Title"
    description: "Brief description"
  feedback:
    rating: 85
    comments: "Quality assessment"
    status:
      value: "approved"
      validation: "passed"
  ```
  
  ## Content sections...
  ```

### 6. Real-time Event System
- **Purpose:** Event sourcing and real-time notifications via SpacetimeDB
- **Event Types:**
  - Agent registration/deregistration
  - Workflow creation/completion
  - User overrides and authority actions
  - System events and notifications
  - Documentation updates and validation
- **Event Subscription:**
  ```python
  def subscribe_to_events(event_types):
      """Subscribe to real-time events from SpacetimeDB"""
      result = subprocess.run([
          "spacetime", "subscribe", "overseer-system",
          "system_events", json.dumps(event_types)
      ], capture_output=True, text=True)
      
      return result.returncode == 0
  
  # Subscribe to agent events
  subscribe_to_events(["agent_registration", "workflow_completion"])
  ```

### 7. Documentation Templates
- **Purpose:** Standardized templates for consistent documentation creation
- **Location:** `framework/docs/templates/`
- **Available Templates:**
  - Project Templates: `project_template.md`, `project_setup_template.md`
  - Component Templates: `component_template.md`, `api_template.md`
- **Template Usage:**
  ```bash
  # Create documentation using templates
  ./agent-doc-system/framework/scripts/create_doc.sh project "My Documentation" \
    --owner "YourAgentName" \
    --description "Project documentation"
  ```

### 8. Enhanced Validation Framework
- **Purpose:** Comprehensive validation with AI feedback integration
- **Key Files:**
  - [Enhanced Validation Script](../scripts/enhanced_validate.sh)
  - [Standard Validation Script](../scripts/validate.sh)
  - [Python Validator](../validators/validator.py)
- **Validation Commands:**
  ```bash
  # Standard validation
  ./agent-doc-system/framework/scripts/validate.sh
  
  # Enhanced validation with AI feedback
  ./agent-doc-system/framework/scripts/enhanced_validate.sh --feedback
  ```

## Required Practices

### Agent Setup and Registration
1. **Agent Name Setup:**
   ```bash
   # Check current agent name
   ./agent-doc-system/framework/scripts/setup_agent_name.sh check
   
   # Set agent name (one-time only)
   ./agent-doc-system/framework/scripts/setup_agent_name.sh setup YourAgentName
   
   # Activate agent environment
   ./agent-doc-system/framework/scripts/setup_agent_name.sh activate
   ```

2. **SpacetimeDB Connection:**
   ```python
   import subprocess
   
   def connect_to_overseer_system():
       """Connect to SpacetimeDB overseer-system"""
       # Test connection
       result = subprocess.run([
           "spacetime", "list"
       ], capture_output=True, text=True)
       
       if "overseer-system" in result.stdout:
           print("✅ Connected to SpacetimeDB overseer-system")
           return True
       else:
           print("❌ SpacetimeDB overseer-system not accessible")
           return False
   
   # Test connection
   connect_to_overseer_system()
   ```

3. **Agent Registration:**
   ```python
   def announce_arrival(agent_name):
       """Announce agent arrival to overseer-system"""
       result = subprocess.run([
           "spacetime", "call", "overseer-system", "register_agent",
           "--agent_name", agent_name, "--agent_type", "documentation", "--status", "active"
       ], capture_output=True, text=True)
       
       if result.returncode == 0:
           print(f"🎉 {agent_name} announced arrival to overseer-system")
       return result.returncode == 0
   
   # Announce your arrival
   announce_arrival("YourAgentName")
   ```

### Documentation Structure and Permissions
1. **Location Requirements (CRITICAL):**
   - **DocSystemAgent ONLY**: Can create in `framework/docs/`, `framework/docs/api/`, `framework/docs/components/`
   - **ALL OTHER AGENTS**: MUST create documentation ONLY in `agent-doc-system/project_docs/` directory
   - **Templates**: Available to read from `framework/docs/templates/`
   - **Framework Directory**: READ-ONLY for all agents except DocSystemAgent

2. **Required Sections:**
   - Title
   - Machine-Actionable Metadata (with complete feedback section)
   - Overview
   - Main Content
   - Changelog

### Creating New Documentation
1. **Use the automated creator (Recommended)**:
   ```bash
   ./agent-doc-system/framework/scripts/create_doc.sh <type> "<title>" --owner "<name>" --description "<desc>"
   ```
2. **Alternative: Manual template copy**:
   - Choose template from `agent-doc-system/framework/docs/templates/`
   - Copy to correct location (`agent-doc-system/project_docs/`)
   - Update metadata and content
3. Run validation before committing

### Validation
Run validation scripts before committing changes:
- `./agent-doc-system/framework/scripts/validate.sh` - Standard validation
- `./agent-doc-system/framework/scripts/enhanced_validate.sh --feedback` - Enhanced validation with AI feedback

## SpacetimeDB Connection Guide

### Prerequisites
1. **SpacetimeDB CLI Installation:**
   ```bash
   # Install SpacetimeDB CLI
   curl -sSL https://spacetime.com/install | bash
   
   # Add to PATH (required for CLI access)
   export PATH="$HOME/.local/bin:$PATH"
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
   
   # Verify installation
   spacetime --version
   ```

2. **Authentication Setup:**
   ```bash
   # Create SpacetimeDB identity
   spacetime identity new
   
   # List available identities
   spacetime identity list
   ```

### Connection Process
1. **Connect to Overseer-System:**
   ```bash
   # Set connection environment variable
   export SPACETIME_URI=http://127.0.0.1:3000
   
   # Connect and subscribe to overseer-system database
   spacetime subscribe overseer-system
   ```

2. **Verify Connection:**
   ```python
   import subprocess
   import json
   
   def verify_overseer_connection():
       """Verify connection to SpacetimeDB overseer-system"""
       try:
           # Check if overseer-system is accessible
           result = subprocess.run([
               "spacetime", "logs", "overseer-system"
           ], capture_output=True, text=True, timeout=10)
           
           if result.returncode == 0:
               print("✅ SpacetimeDB overseer-system connection verified")
               return True
           else:
               print(f"❌ Connection failed: {result.stderr}")
               return False
       except subprocess.TimeoutExpired:
           print("❌ Connection timeout - overseer-system not responding")
           return False
   
   # Verify connection
   verify_overseer_connection()
   ```

### Agent Operations via SpacetimeDB

**Complete Agent Integration Example:**
```python
import subprocess
import json
import uuid
from datetime import datetime

class SpacetimeDBAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.register()
    
    def register(self):
        """Register agent in SpacetimeDB overseer-system"""
        agent_id = f"documentation_{self.agent_name.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        result = subprocess.run([
            "spacetime", "call", "overseer-system", "register_agent",
            "--agent_id", agent_id,
            "--agent_name", self.agent_name,
            "--agent_type", "documentation",
            "--supervisor_id", "",
            "--status", "active"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {self.agent_name} registered in overseer-system")
        else:
            print(f"❌ Registration failed: {result.stderr}")
    
    def send_event(self, event_type, target_agent, data):
        """Send system event via SpacetimeDB"""
        event_data = {
            "event_type": event_type,
            "source_agent": self.agent_name,
            "target_agent": target_agent,
            "timestamp": datetime.now().isoformat(),
            "data": json.dumps(data),
            "priority": 1
        }
        
        result = subprocess.run([
            "spacetime", "call", "overseer-system", "create_system_event",
            "--event_id", f"event_{uuid.uuid4().hex[:8]}",
            "--event_type", event_type,
            "--source_agent", self.agent_name,
            "--target_agent", target_agent,
            "--data", json.dumps(data),
            "--priority", "1"
        ], capture_output=True, text=True)
        
        return result.returncode == 0
    
    def get_active_agents(self):
        """Get list of active agents from overseer-system"""
        result = subprocess.run([
            "spacetime", "sql", "overseer-system",
            "SELECT agent_name, status FROM agent_registry WHERE status = 'active'"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        return []
    
    def create_workflow(self, workflow_name, steps):
        """Create workflow in overseer-system"""
        workflow_data = {
            "workflow_id": f"{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "workflow_type": "documentation",
            "status": "pending",
            "initiator_agent": self.agent_name,
            "assigned_agents": json.dumps([self.agent_name]),
            "metadata": json.dumps(steps)
        }
        
        result = subprocess.run([
            "spacetime", "call", "overseer-system", "create_workflow",
            "--workflow_id", workflow_data["workflow_id"],
            "--workflow_type", workflow_data["workflow_type"],
            "--initiator_agent", workflow_data["initiator_agent"],
            "--assigned_agents", workflow_data["assigned_agents"],
            "--metadata", workflow_data["metadata"]
        ], capture_output=True, text=True)
        
        return result.returncode == 0

# Usage example
agent = SpacetimeDBAgent("YourAgentName")

# Send documentation event
agent.send_event(
    "documentation_created",
    "DocSystemAgent",
    {"file": "my_documentation.md", "status": "draft"}
)

# Create documentation workflow
agent.create_workflow(
    "doc_review",
    [{"step": "validate", "agent": "DocSystemAgent"},
     {"step": "approve", "agent": "ReviewAgent"}]
)

# Get active agents
active_agents = agent.get_active_agents()
print(f"Active agents in overseer-system: {len(active_agents)}")
```

## Best Practices

1. **SpacetimeDB Integration:**
   - Always verify overseer-system connection before operations
   - Use proper error handling for SpacetimeDB calls
   - Monitor real-time events and subscriptions
   - Respect user authority (priority 255) at all times
   - Implement proper agent registration and heartbeat

2. **Documentation:**
   - Use templates for new documentation
   - Include comprehensive metadata with feedback section
   - Follow the required structure consistently
   - Run validation before committing changes
   - Track improvements with AI feedback system

3. **Agent Coordination:**
   - Register properly in overseer-system upon arrival
   - Participate in workflows when assigned
   - Respect emergency halt commands from users
   - Maintain audit trail for all actions
   - Coordinate with other agents via real-time events

## Validation & Troubleshooting

### SpacetimeDB Connection Issues
**Common Problems:**
- **Connection Failed**: Verify SpacetimeDB CLI installation and overseer-system deployment
- **Authentication Error**: Check `spacetime identity` setup
- **Timeout**: Ensure overseer-system is running and accessible
- **Permission Denied**: Verify agent registration in overseer-system

**Resolution Steps:**
1. Test SpacetimeDB CLI: `spacetime --version`
2. Check connection: `spacetime logs overseer-system`
3. Verify identity: `spacetime identity list`
4. Re-register agent if needed

### Documentation Validation
**Validation Checks:**
- Metadata structure and required fields
- YAML schema compliance
- Markdown formatting
- Template adherence
- Feedback section completeness

**Common Issues:**
- Missing required metadata fields
- Invalid YAML syntax
- Incomplete feedback sections
- Non-compliant template usage

**Resolution:**
1. Check validation error messages
2. Use templates from `framework/docs/templates/`
3. Run AI feedback for improvement suggestions
4. Track improvements with self-improvement tracker

## Directory Reference

- **Framework Documentation:** `framework/docs/`
- **Templates:** `framework/docs/templates/`
- **Schemas:** `framework/schemas/`
- **Scripts:** `framework/scripts/`
- **Agent Communication:** `framework/agent_communication/`
- **Validators:** `framework/validators/`
- **Tests:** `tests/`
- **Project Documentation:** `project_docs/` (your documentation goes here)

## Getting Started

### Quick Start

1. **Install Dependencies:**
   ```bash
   # Using Poetry (recommended)
   poetry install
   
   # Or using pip
   pip install pyyaml rich click pytest mypy black ruff
   
   # Install SpacetimeDB CLI
   curl -sSL https://spacetime.com/install | bash
   ```

2. **Setup SpacetimeDB Identity:**
   ```bash
   # Create SpacetimeDB identity
   spacetime identity new
   
   # Connect to SpacetimeDB overseer-system
   export SPACETIME_URI=http://127.0.0.1:3000
   spacetime subscribe overseer-system
   ```

3. **Check Agent Name:**
   ```bash
   # Check if agent has a name set
   ./agent-doc-system/framework/scripts/setup_agent_name.sh check
   
   # If no name is set, create one
   ./agent-doc-system/framework/scripts/setup_agent_name.sh setup YourAgentName
   
   # Activate agent environment
   ./agent-doc-system/framework/scripts/setup_agent_name.sh activate
   ```

4. **Connect to SpacetimeDB Overseer-System:**
   ```python
   import subprocess
   
   def test_overseer_connection():
       """Test connection to SpacetimeDB overseer-system"""
       try:
           result = subprocess.run([
               "spacetime", "logs", "overseer-system"
           ], capture_output=True, text=True, timeout=5)
           
           if result.returncode == 0:
               print("✅ SpacetimeDB overseer-system connected successfully")
               return True
           else:
               print(f"❌ Connection failed: {result.stderr}")
               return False
       except subprocess.TimeoutExpired:
           print("❌ Connection timeout")
           return False
   
   # Test connection
   test_overseer_connection()
   ```

5. **Register Agent in Overseer-System:**
   ```python
   import subprocess
   import os
   from datetime import datetime
   
   def register_agent():
       """Register agent in SpacetimeDB overseer-system"""
       agent_name = os.environ.get('AGENT_NAME', 'UnnamedAgent')
       
       result = subprocess.run([
           "spacetime", "call", "overseer-system", "register_agent",
           "--agent_name", agent_name, "--agent_type", "documentation", "--status", "active"
       ], capture_output=True, text=True)
       
       if result.returncode == 0:
           print(f"🎉 {agent_name} registered in overseer-system")
           return True
       else:
           print(f"❌ Registration failed: {result.stderr}")
           return False
   
   # Register agent
   register_agent()
   ```

6. **Create Documentation:**
   ```bash
   # For ALL AGENTS - Creates in agent-doc-system/project_docs/
   ./agent-doc-system/framework/scripts/create_doc.sh project "My Project Documentation" \
     --owner "YourAgentName" \
     --description "Brief description of the project documentation"
   ```

7. **Validate and Track:**
   ```bash
   # Standard validation
   ./agent-doc-system/framework/scripts/validate.sh
   
   # Enhanced validation with AI feedback
   ./agent-doc-system/framework/scripts/enhanced_validate.sh --feedback
   ```

### Complete Workflow

1. Install SpacetimeDB CLI and create identity
2. Check agent name setup using `./agent-doc-system/framework/scripts/setup_agent_name.sh check`
3. Connect to SpacetimeDB overseer-system
4. Register agent in overseer-system
5. Review templates in `agent-doc-system/framework/docs/templates/`
6. Create documentation with proper metadata in `agent-doc-system/project_docs/`
7. Run validation and AI feedback
8. Participate in workflows and coordinate with other agents

## Quickstart Checklist

### Setup:
- [ ] Install dependencies: `poetry install` or `pip install pyyaml rich click`
- [ ] Install SpacetimeDB CLI: `curl -sSL https://spacetime.com/install | bash`
- [ ] Create SpacetimeDB identity: `spacetime identity new`
- [ ] Check agent name: `./agent-doc-system/framework/scripts/setup_agent_name.sh check`
- [ ] Set agent name if needed: `./agent-doc-system/framework/scripts/setup_agent_name.sh setup YourAgentName`
- [ ] Activate agent environment: `./agent-doc-system/framework/scripts/setup_agent_name.sh activate`
- [ ] Set connection: `export SPACETIME_URI=http://127.0.0.1:3000`
- [ ] Connect to overseer-system: `spacetime subscribe overseer-system`
- [ ] Test connection and register agent in SpacetimeDB
- [ ] Choose template from `agent-doc-system/framework/docs/templates/`
- [ ] Create documentation with proper YAML metadata in `agent-doc-system/project_docs/`
- [ ] Include required sections: title, metadata, overview, changelog
- [ ] Add feedback section for AI assessment

### Validation and Coordination:
- [ ] Run standard validation: `./agent-doc-system/framework/scripts/validate.sh`
- [ ] Generate AI feedback: `./agent-doc-system/framework/scripts/enhanced_validate.sh --feedback`
- [ ] Implement improvement suggestions
- [ ] Track improvement cycles
- [ ] Participate in overseer-system workflows
- [ ] Monitor real-time events and coordinate with other agents

## Changelog

- **3.3.0** (2025-06-03): Database Name Corrections and Verified Integration
  - Critical database name correction: `mcp-agent-system` → `overseer-system`
  - Updated all SpacetimeDB command references to use correct database name
  - Verified all reducer calls and connection strings
  - Fixed documentation inconsistencies identified by Claude-MCP-Research
  - Ensured complete alignment with deployed overseer-system architecture

- **3.2.0** (2025-06-03): Complete 16-Table SpacetimeDB Architecture
  - Complete 16-table SpacetimeDB overseer-system architecture implementation
  - Updated agent ID format: `{type}_{function}_{timestamp}` (e.g., supervisor_coordination_001)
  - Verified connection endpoint: `http://127.0.0.1:3000` (simplified from database-specific URL)
  - Updated PATH export to `$HOME/.local/bin:$PATH` per Claude-MCP-Research specifications
  - Added agent_registry, agent_hierarchy, workflow_steps, task_queue tables
  - Added coordination_locks, agent_subscriptions, health_metrics, system_alerts tables
  - Added session_management table for agent session tracking
  - Updated reducer functions: register_agent, user_override, user_directive, agent_heartbeat
  - Ready for production migration to SpacetimeDB overseer-system

- **3.1.0** (2025-06-03): Deployed SpacetimeDB Specifications Update
  - Updated with verified deployed SpacetimeDB overseer-system specifications
  - Added user_directives and user_audit_log tables (8-table architecture total)
  - Documented proper agent registration with RegisterAgent reducer and ID formats
  - Added SPACETIME_URI connection string: `http://127.0.0.1:3000/database/overseer-system`
  - Included PATH export requirements for spacetime CLI: `$HOME/.spacetime/bin:$PATH`
  - Updated all reducer function calls: RegisterAgent, CreateSystemEvent, CreateWorkflow
  - Clarified agent registration parameters: agent_id, agent_name, agent_type, capabilities
  - Verified deployment specifications from Claude-MCP-Research integration

- **3.0.0** (2025-06-03): SpacetimeDB Overseer-System Integration
  - SpacetimeDB overseer-system with real-time coordination and user supreme authority
  - 6-table database architecture: users, agents, workflows, user_overrides, system_events, user_notifications
  - 15 MCP tools with complete input/output schemas and user authority (priority 255)
  - Sub-microsecond response times with WebAssembly backend
  - Real-time subscriptions, event sourcing, and complete audit trail
  - Emergency halt capability and rollback mechanisms
  - Agent registration and communication via SpacetimeDB reducers
  - Single system approach completely replacing SQLite
  - SpacetimeDB CLI authentication and connection management
  - Workflow orchestration and multi-agent coordination
  - Documentation system integration with real-time database
  - Migration guide from SQLite to SpacetimeDB architecture

- **2.5.0** (2025-06-03): Enhanced metadata system and AI feedback integration
- **1.0.0** (2024-03-21): Initial release of THE PROTOCOL