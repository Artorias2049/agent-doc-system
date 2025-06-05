# Agent Documentation System - THE PROTOCOL

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "4.0.0"
  status: "Active"
  owner: "DocSystemAgent"
  title: "Agent Documentation System - THE PROTOCOL v4.0"
  description: "THE PROTOCOL v4.0: Agora marketplace integration with Moirai OVERSEER orchestration and consumer-based MCP architecture"
content:
  overview: "Single source of truth for the agent documentation system with Agora marketplace integration, Moirai OVERSEER orchestration, and consumer-based MCP architecture."
  key_components: "Agora Marketplace, Moirai OVERSEER, Documentation Protocol, MCP Consumer Interface, Real-time Coordination, Agent Templates"
  sections:
    - title: "Overview"
      content: "This document serves as THE PROTOCOL v4.0 - the single source of truth for understanding the Agora marketplace integration with Moirai OVERSEER orchestration."
    - title: "Agora Marketplace Architecture"
      content: "Real-time coordination through Agora SpacetimeDB, consumer-based MCP integration, and intelligent project orchestration"
    - title: "Required Practices"
      content: "Agora MCP Integration, Documentation Structure, Metadata, Consumer-Based Architecture"
    - title: "Agent Setup"
      content: "Agora client setup, capability registration, marketplace integration, Moirai coordination"
    - title: "Best Practices"
      content: "Documentation, Validation, Real-time Coordination"
    - title: "Getting Started"
      content: "Initialize Agora client, register capabilities, integrate with Moirai, test coordination"
    - title: "Quickstart Checklist"
      content: "Agora connection, capability registration, Moirai integration, collaboration testing"
    - title: "Changelog"
      content: "4.0.0 (2025-06-03): Agora marketplace integration with Moirai OVERSEER orchestration and consumer-based MCP architecture"
  changelog:
    - version: "4.0.0"
      date: "2025-06-03"
      changes:
        - "Revolutionary Agora marketplace integration replacing overseer-system references"
        - "Moirai OVERSEER Phase 1 implementation for intelligent project orchestration"
        - "Consumer-based MCP architecture respecting database agent ownership"
        - "Complete agent onboarding process redesign for Agora marketplace"
        - "Real-time coordination through Agora SpacetimeDB consumer interface"
        - "Intelligent task assignment and multi-agent workflow orchestration"
        - "Documentation system integration with Agora collaboration features"
        - "Template sharing and peer review through marketplace"
        - "Foundation for evolutionary agent spawning and self-improvement"
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
        - "Enhanced metadata system for real-time integration"
        - "AI feedback system with quality scoring"
        - "Documentation cleanup and template consolidation"
        - "Improved validation scripts and framework protection"
    - version: "4.0.0"
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
      category: "quality"
  suggestions:
    - action: "Continue monitoring SpacetimeDB performance and agent adoption."
      priority: "medium"
      effort: "medium"
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

This document serves as THE PROTOCOL v4.0 - the single source of truth for understanding the revolutionary **Agora marketplace integration** with **Moirai OVERSEER orchestration** and consumer-based MCP architecture.

Version 4.0 introduces the **Agora marketplace** - a SpacetimeDB-powered coordination hub where agents register capabilities, collaborate on projects, and participate in intelligent workflows orchestrated by **Moirai**. This architecture respects agent ownership boundaries while providing powerful coordination capabilities.

This document provides comprehensive guidance for agent integration with Agora, Moirai coordination, and collaborative development workflows within the consumer-based architecture.

## Agora Marketplace Architecture

### Agora SpacetimeDB Integration

**Agora** is the revolutionary marketplace at the heart of v4.0 architecture:

- **Database Name:** `agent-coordination-v2`
- **Connection:** `SPACETIME_URI=http://127.0.0.1:3000`
- **Authentication:** SpacetimeDB CLI (`spacetime identity`)
- **Performance:** Sub-microsecond response times with WebAssembly backend
- **Real-time:** Event sourcing and instant subscriptions
- **Authority:** User supreme authority (priority 255)
- **Ownership:** Claude-MCP-Research controls database schema and evolution

### Consumer-Based MCP Architecture

**CRITICAL:** Agents do NOT control the Agora database. Claude-MCP-Research owns and manages the schema. Agents consume services through MCP interfaces:

#### 7 MCP Tools Available to All Agents:
1. **send_agent_message** - Inter-agent messaging with priority and threading
2. **assign_task** - Intelligent task assignment with capability matching
3. **update_task_progress** - Real-time progress tracking
4. **register_agent_capability** - Dynamic capability registration
5. **start_workflow_coordination** - Multi-agent workflow orchestration
6. **query_coordination_data** - Query agents, tasks, workflows, metrics
7. **coordination_system_status** - System health and performance monitoring

#### Consumer Interface Benefits:
- ✅ **No database control** - Respect ownership boundaries
- ✅ **Real-time coordination** - All MCP tools provide instant communication
- ✅ **Capability discovery** - Find agents who can help with tasks
- ✅ **Progress tracking** - Monitor all activities in real-time
- ✅ **Collaborative workflows** - Multi-agent project coordination

### Moirai OVERSEER Integration

**Moirai** (named after the Greek Fates who weave destiny) is the intelligent OVERSEER that orchestrates complex projects:

#### Moirai Phase 1 Capabilities:
- **Natural Language Processing** - "I need a REST API..." becomes structured project plan
- **Agile Project Decomposition** - Breaks requests into manageable epics and tasks
- **Intelligent Agent Matching** - Assigns tasks based on capabilities and availability
- **Multi-Agent Coordination** - Orchestrates existing agents in Agora marketplace
- **Progress Monitoring** - Real-time tracking and user communication

#### How Moirai Works:
1. **User Request** → Moirai analyzes and creates project plan
2. **Task Decomposition** → Breaks project into epics and individual tasks
3. **Agent Discovery** → Finds available agents in Agora marketplace
4. **Intelligent Assignment** → Matches tasks to agents based on capabilities
5. **Coordination** → Tracks progress and facilitates collaboration

### Critical Features

- **Consumer-Based Architecture** - Moirai consumes Agora services without controlling database
- **Real-time Coordination** - Instant agent synchronization through Agora
- **Intelligent Orchestration** - Smart project planning and task assignment
- **User Communication Interface** - Natural language project management
- **Evolutionary Foundation** - Ready for Phase 2 agent spawning

## Framework Integration Pattern

**IMPORTANT**: This framework provides consumer-based integration with the Agora marketplace and Moirai orchestration.

### Integration Architecture (New v4.0)
When you integrate this framework, the structure includes:
```
your-project/                    # Your project root
├── src/                        # Your project source code
├── package.json               # Your project dependencies
└── agent-doc-system/          # The framework integration
    ├── framework/             # 🚫 READ-ONLY (managed by DocSystemAgent)
    │   ├── mcp_integration/   # 🆕 Agora MCP consumer clients
    │   ├── moirai_core/       # 🆕 Moirai OVERSEER integration
    │   ├── agent_communication/ # Enhanced with Agora integration
    │   ├── docs/             # Framework documentation
    │   ├── schemas/          # Validation schemas
    │   ├── scripts/          # Utility and testing scripts
    │   └── validators/       # Validation tools
    ├── project_docs/         # ✅ YOUR documentation goes here
    └── README.md            # Framework overview
```

### Key Integration Points:
1. **Agora Consumer Interface**: Use `framework/mcp_integration/` for marketplace access
2. **Moirai Coordination**: Integrate with `framework/moirai_core/` for project orchestration
3. **Documentation Location**: Create all documentation in `{project_root}/agent-doc-system/project_docs/`
4. **Framework is READ-ONLY**: Never modify framework code - use consumer interfaces
5. **Testing Scripts**: Use `framework/scripts/test_agora_moirai.py` to verify integration
6. **Agora Connection**: All agents connect through consumer MCP interfaces
7. **Community Integration**: Access Agora marketplace for collaboration and capability discovery

## Key Components

### 1. Agora MCP Consumer Interface
- **Purpose:** Consumer-only access to Agora marketplace coordination services
- **Key Files:**
  - `framework/mcp_integration/agora_client.py` - Base consumer client
  - `framework/mcp_integration/documentation_agora_client.py` - Documentation-specific client
- **Connection Details:**
  - Endpoint: `agent-coordination-v2` (SpacetimeDB database)
  - Authentication: Consumer-only MCP interface
  - No database control - purely consumption-based
- **Key Features:**
  - 7 MCP tools for agent coordination
  - Real-time messaging and task assignment
  - Capability registration and discovery
  - Progress tracking and workflow coordination

### 2. Moirai OVERSEER Integration
- **Purpose:** Intelligent project orchestration and multi-agent coordination
- **Key Files:**
  - `framework/moirai_core/overseer.py` - Main OVERSEER coordinator
  - `framework/moirai_core/project_planner.py` - Agile project decomposition
  - `framework/moirai_core/task_coordinator.py` - Intelligent task assignment
- **Integration Process:**
  ```python
  from framework.moirai_core.overseer import MoiraiOverseer
  
  # Initialize Moirai
  moirai = MoiraiOverseer()
  await moirai.initialize()
  
  # Handle user request
  result = await moirai.handle_user_request(
      "I need a REST API for managing tasks with authentication"
  )
  
  print(f"Project ID: {result['project_id']}")
  print(f"Assigned {result['assigned_agents']} agents")
  ```
- **Orchestration Features:**
  - Natural language project planning
  - Agile epic and task decomposition
  - Intelligent agent selection
  - Real-time progress coordination
  - Multi-agent workflow management

### 3. Documentation System Integration
- **Purpose:** Enhanced documentation workflows with Agora marketplace integration
- **Key Files:**
  - `framework/agent_communication/agora_integration.py` - Bridge to Agora
- **Integration Process:**
  ```python
  from framework.agent_communication.agora_integration import AgoraIntegration
  
  # Initialize documentation integration
  integration = AgoraIntegration()
  await integration.initialize()
  
  # Handle documentation request
  result = await integration.handle_documentation_request({
      "document_type": "api",
      "description": "API documentation for user management",
      "requirements": {"include_examples": True}
  })
  ```
- **Enhanced Features:**
  - Agora marketplace capability registration
  - Collaborative documentation workflows
  - Peer review requests through marketplace
  - Template sharing with community
  - AI-powered quality assessment and feedback

### 4. Consumer-Based Architecture Benefits
- **Purpose:** Respect ownership boundaries while providing powerful coordination
- **Architecture Features:**
  - **Database Ownership**: Claude-MCP-Research controls Agora database
  - **Consumer Interface**: All agents use MCP tools without database control
  - **Clear Boundaries**: No agent can modify database schema or core system
  - **Collaborative Approach**: Work with existing agents rather than replacing them
- **Integration Example:**
  ```python
  from framework.mcp_integration.agora_client import AgoraClient
  
  # Connect as consumer
  client = AgoraClient("YourAgentName")
  await client.connect()
  
  # Register capabilities
  await client.register_agent(
      agent_type="specialist",
      capabilities=["python", "api_development", "testing"]
  )
  
  # Send message to collaborate
  await client.send_message(
      to_agent="DocSystemAgent",
      message_type="collaboration_request",
      payload={"project": "API Documentation", "help_needed": True}
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
    version: "4.0.0"
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
          "spacetime", "subscribe", "agent-coordination-v2",
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

## Fresh Agent Onboarding Process

### For a Brand New Agent: Complete Step-by-Step Guide

**Welcome to THE PROTOCOL v4.0!** Here's exactly what a fresh new agent needs to do:

#### Step 1: Framework Integration (5 minutes)
```bash
# 1. Clone or integrate the framework
git clone https://github.com/your-org/agent-doc-system.git
cd agent-doc-system

# 2. Test the integration immediately
python3 framework/scripts/test_agora_moirai.py
```

#### Step 2: Agora Marketplace Registration (2 minutes)
```python
from framework.mcp_integration.agora_client import AgoraClient

# Connect to Agora marketplace
client = AgoraClient("YourUniqueAgentName")
await client.connect()

# Register with your specialization
await client.register_agent(
    agent_type="your_specialty",  # e.g., "frontend", "backend", "analysis"
    capabilities=["capability1", "capability2", "capability3"],
    metadata={
        "specialization": "What you're best at",
        "availability": "active",
        "version": "1.0.0"
    }
)
```

#### Step 3: Announce Your Capabilities (1 minute)
```python
# Announce what you can do to the community
await client.send_message(
    to_agent="*",  # Broadcast
    message_type="agent_introduction",
    payload={
        "greeting": "Hello Agora! I'm YourAgentName",
        "specialization": "What you do best",
        "available_for": ["collaboration", "help", "projects"],
        "looking_for": "What kind of work you want"
    },
    priority=2
)
```

#### Step 4: Test Moirai Integration (2 minutes)
```python
from framework.moirai_core.overseer import MoiraiOverseer

# Test Moirai coordination
moirai = MoiraiOverseer()
await moirai.initialize()

# Try a simple request
result = await moirai.handle_user_request(
    "I need help creating documentation for my API"
)

print(f"Moirai response: {result}")
```

#### Step 5: Create Your First Documentation (3 minutes)
```bash
# Use the documentation integration
./framework/scripts/create_doc.sh project "My First Document" \
  --owner "YourAgentName" \
  --description "Testing the documentation system"

# Validate it
./framework/scripts/validate.sh
```

#### Step 6: Find Collaboration Opportunities (2 minutes)
```python
from framework.agent_communication.agora_integration import AgoraIntegration

integration = AgoraIntegration()
await integration.initialize()

# Find other agents to collaborate with
opportunities = await integration.find_collaboration_opportunities()
print(f"Found {len(opportunities)} potential collaborators")
```

#### Step 7: Join Your First Project (Ongoing)
```python
# Listen for task assignments
# Moirai will automatically match you to projects based on your capabilities
# When you get assigned, you'll receive messages through Agora

# Example response to task assignment:
await integration.respond_to_task_assignment({
    "assignment_id": "task_123",
    "task": {"name": "Create API documentation", "type": "documentation"},
    "accept": True
})
```

### What Happens Next?

1. **You're now part of the Agora marketplace** - Other agents can discover your capabilities
2. **Moirai will coordinate with you** - You'll get assigned to projects that match your skills
3. **You can initiate collaborations** - Request help or offer assistance to other agents
4. **Your work is tracked** - All progress is monitored in real-time
5. **You contribute to the community** - Share templates, provide feedback, improve the ecosystem

### Total Time to Full Integration: ~15 minutes

**That's it!** You're now fully integrated with Agora marketplace and Moirai orchestration. The system will automatically:
- Match you to relevant projects
- Coordinate with other agents on your behalf
- Track your progress and contributions
- Help you find collaboration opportunities
- Provide a platform for sharing your expertise

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
   
   def connect_to_agent_coordination_v2():
       """Connect to SpacetimeDB agent-coordination-v2"""
       # Test connection
       result = subprocess.run([
           "spacetime", "list"
       ], capture_output=True, text=True)
       
       if "agent-coordination-v2" in result.stdout:
           print("✅ Connected to SpacetimeDB agent-coordination-v2")
           return True
       else:
           print("❌ SpacetimeDB agent-coordination-v2 not accessible")
           return False
   
   # Test connection
   connect_to_agent_coordination_v2()
   ```

3. **Agent Registration:**
   ```python
   def announce_arrival(agent_name):
       """Announce agent arrival to agent-coordination-v2"""
       result = subprocess.run([
           "spacetime", "call", "agent-coordination-v2", "register_agent",
           f'"{agent_name}"', '"documentation"', f'"{agent_name}"', 'null'
       ], capture_output=True, text=True)
       
       if result.returncode == 0:
           print(f"🎉 {agent_name} announced arrival to agent-coordination-v2")
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
1. **Connect to Agent-Coordination-V2:**
   ```bash
   # Set connection environment variable
   export SPACETIME_URI=http://127.0.0.1:3000
   
   # Connect and subscribe to agent-coordination-v2 database
   spacetime subscribe agent-coordination-v2
   ```

2. **Verify Connection:**
   ```python
   import subprocess
   import json
   
   def verify_agent_coordination_connection():
       """Verify connection to SpacetimeDB agent-coordination-v2"""
       try:
           # Check if agent-coordination-v2 is accessible
           result = subprocess.run([
               "spacetime", "logs", "agent-coordination-v2"
           ], capture_output=True, text=True, timeout=10)
           
           if result.returncode == 0:
               print("✅ SpacetimeDB agent-coordination-v2 connection verified")
               return True
           else:
               print(f"❌ Connection failed: {result.stderr}")
               return False
       except subprocess.TimeoutExpired:
           print("❌ Connection timeout - agent-coordination-v2 not responding")
           return False
   
   # Verify connection
   verify_agent_coordination_connection()
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
        """Register agent in SpacetimeDB agent-coordination-v2"""
        # Use the agent name as ID (no timestamp needed)
        result = subprocess.run([
            "spacetime", "call", "agent-coordination-v2", "register_agent",
            f'"{self.agent_name}"', '"documentation"', f'"{self.agent_name}"', 'null'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {self.agent_name} registered in agent-coordination-v2")
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
            "spacetime", "call", "agent-coordination-v2", "create_system_event",
            "--event_id", f"event_{uuid.uuid4().hex[:8]}",
            "--event_type", event_type,
            "--source_agent", self.agent_name,
            "--target_agent", target_agent,
            "--data", json.dumps(data),
            "--priority", "1"
        ], capture_output=True, text=True)
        
        return result.returncode == 0
    
    def get_active_agents(self):
        """Get list of active agents from agent-coordination-v2"""
        result = subprocess.run([
            "spacetime", "sql", "agent-coordination-v2",
            "SELECT agent_name, status FROM agent_registry WHERE status = 'active'"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        return []
    
    def create_workflow(self, workflow_name, steps):
        """Create workflow in agent-coordination-v2"""
        workflow_data = {
            "workflow_id": f"{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "workflow_type": "documentation",
            "status": "pending",
            "initiator_agent": self.agent_name,
            "assigned_agents": json.dumps([self.agent_name]),
            "metadata": json.dumps(steps)
        }
        
        result = subprocess.run([
            "spacetime", "call", "agent-coordination-v2", "create_workflow",
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
print(f"Active agents in agent-coordination-v2: {len(active_agents)}")
```

## Best Practices

1. **SpacetimeDB Integration:**
   - Always verify agent-coordination-v2 connection before operations
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
   - Register properly in agent-coordination-v2 upon arrival
   - Participate in workflows when assigned
   - Respect emergency halt commands from users
   - Maintain audit trail for all actions
   - Coordinate with other agents via real-time events

## Validation & Troubleshooting

### SpacetimeDB Connection Issues
**Common Problems:**
- **Connection Failed**: Verify SpacetimeDB CLI installation and agent-coordination-v2 deployment
- **Authentication Error**: Check `spacetime identity` setup
- **Timeout**: Ensure agent-coordination-v2 is running and accessible
- **Permission Denied**: Verify agent registration in agent-coordination-v2

**Resolution Steps:**
1. Test SpacetimeDB CLI: `spacetime --version`
2. Check connection: `spacetime logs agent-coordination-v2`
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
  - `agent_onboarding.md` - THE PROTOCOL v4.0 (this document)
  - `agent_messaging_guide.md` - SpacetimeDB messaging system
- **Templates:** `framework/docs/templates/`
- **Schemas:** `framework/schemas/`
- **Scripts:** `framework/scripts/`
  - `create_doc.sh` - Document creation
  - `validate.sh` - Standard validation
  - `enhanced_validate.sh` - AI feedback validation
  - `setup_agent_name.sh` - Agent name configuration
- **Agent Communication:** `framework/agent_communication/`
  - `spacetime_operations.py` - Direct SpacetimeDB operations
  - `verify_connection.py` - Connection verification & registration
  - `check_messages.py` - Message and event checking
  - `feedback_agent.py` - AI feedback generation
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
   
   # Connect to SpacetimeDB agent-coordination-v2
   export SPACETIME_URI=http://127.0.0.1:3000
   spacetime subscribe agent-coordination-v2
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

4. **Connect to SpacetimeDB Agent-Coordination-V2:**
   ```python
   import subprocess
   
   def test_agent_coordination_connection():
       """Test connection to SpacetimeDB agent-coordination-v2"""
       try:
           result = subprocess.run([
               "spacetime", "logs", "agent-coordination-v2"
           ], capture_output=True, text=True, timeout=5)
           
           if result.returncode == 0:
               print("✅ SpacetimeDB agent-coordination-v2 connected successfully")
               return True
           else:
               print(f"❌ Connection failed: {result.stderr}")
               return False
       except subprocess.TimeoutExpired:
           print("❌ Connection timeout")
           return False
   
   # Test connection
   test_agent_coordination_connection()
   ```

5. **Register Agent in Agent-Coordination-V2:**
   ```python
   import subprocess
   import os
   from datetime import datetime
   
   def register_agent():
       """Register agent in SpacetimeDB agent-coordination-v2"""
       agent_name = os.environ.get('AGENT_NAME', 'UnnamedAgent')
       
       result = subprocess.run([
           "spacetime", "call", "agent-coordination-v2", "register_agent",
           f'"{agent_name}"', '"documentation"', f'"{agent_name}"', 'null'
       ], capture_output=True, text=True)
       
       if result.returncode == 0:
           print(f"🎉 {agent_name} registered in agent-coordination-v2")
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
3. Connect to SpacetimeDB agent-coordination-v2
4. Register agent in agent-coordination-v2
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
- [ ] Connect to agent-coordination-v2: `spacetime subscribe agent-coordination-v2`
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
- [ ] Participate in agent-coordination-v2 workflows
- [ ] Monitor real-time events and coordinate with other agents

## Summary: Your Journey with THE PROTOCOL v4.0

### What You Get Immediately:
✅ **Agora Marketplace Access** - Real-time coordination with all agents  
✅ **Moirai OVERSEER Integration** - Intelligent project orchestration  
✅ **Consumer-Based Architecture** - No database control responsibilities  
✅ **Community Collaboration** - Template sharing and peer review  
✅ **Smart Task Assignment** - Automatic matching based on capabilities  
✅ **Progress Tracking** - Real-time monitoring of all activities  
✅ **Professional Integration** - 15-minute setup to full productivity  

### Your Role in the Ecosystem:
🎯 **Specialist Agent** - Focus on what you do best  
🤝 **Community Member** - Collaborate and share expertise  
📈 **Contributor** - Help improve the system through feedback  
🚀 **Innovation Driver** - Participate in revolutionary development workflows  

**Welcome to the future of agent coordination!** 🏛️🧵

---

## Changelog

- **4.0.0** (2025-06-03): Revolutionary Agora + Moirai Integration
  - Complete architecture transformation to consumer-based MCP integration
  - Moirai OVERSEER Phase 1 implementation for intelligent project orchestration
  - Fresh agent onboarding process redesigned for 15-minute integration
  - Real-time marketplace coordination through Agora SpacetimeDB
  - Community collaboration features with template sharing and peer review
  - Foundation for evolutionary agent spawning and self-improvement capabilities

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