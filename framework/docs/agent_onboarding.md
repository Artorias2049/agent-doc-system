# Agent Onboarding Guide [THE PROTOCOL]

## Machine-Actionable Metadata
```yaml
metadata:
  schema: "https://schema.org/TechnicalDocument"
  version: "2.0.0"
  status: "Active"
  owner: "Documentation Team"
  title: "Agent Onboarding Guide [THE PROTOCOL v2.0]"
  description: "THE PROTOCOL v2.0: Natural agent communication with MCP+Database backend"
content:
  overview: "This document serves as THE PROTOCOL - the single source of truth for understanding the agent-doc-system and agent communication protocols."
  key_components: "Documentation Protocol, Agent Communication, Validation System, Schemas, Documentation Templates, Core Components"
  sections:
    - title: "Overview"
      content: "This document serves as THE PROTOCOL - the single source of truth for understanding the agent-doc-system and agent communication protocols."
    - title: "Key Components"
      content: "Documentation Protocol, Agent Communication, Validation System, Schemas, Documentation Templates, Core Components"
    - title: "Required Practices"
      content: "Documentation Structure, Metadata, Creating New Documentation, Validation"
    - title: "Communication Protocol"
      content: "Natural agent communication with agent.say() method"
    - title: "Best Practices"
      content: "Documentation, Code, Review"
    - title: "Validation & Troubleshooting"
      content: "Use the validation script to check for proper metadata, valid agent message files, valid YAML schemas, markdown formatting issues, and template compliance."
    - title: "Where to Find Things"
      content: "Framework Documentation, Project Docs, Component Docs, Templates, Schemas, Validation Scripts, Agent Communication Code"
    - title: "Getting Started"
      content: "Read the main documentation files, review the templates, review the schemas, use the provided Python classes and scripts, run the validation script before submitting changes."
    - title: "Quickstart Checklist"
      content: "Read the onboarding doc, review the templates, review the schemas, run the validation script, follow the commit/PR guidelines."
    - title: "Changelog"
      content: "1.0.0 (2024-03-21): Initial release of THE PROTOCOL"
  changelog:
    - version: "2.0.0"
      date: "2025-06-01"
      changes:
        - "Global agent communication hub infrastructure"
        - "MCP+Database Natural Conversation System"
        - "Simplified UUID and schema validation"
        - "Streamlined agent communication API"
        - "PostgreSQL database backend (global_agent_communication)"
        - "Universal agent client for location-independent communication"
        - "MCP server integration for real-time capabilities"
        - "Natural conversation threading and context preservation"
        - "Real-time subscriptions and event-driven communication"
        - "Global agent registry for system-wide visibility"
        - "Priority messaging with urgent/high/normal levels"
        - "Reduced validation constraints"
        - "Improved performance with database queries over file parsing"
        - "Enhanced global agent communication capabilities"
    - version: "1.1.1"
      date: "2025-01-31"
      changes:
        - "Enhanced path detection for nested usage pattern (project_root/agent-doc-system/framework/)"
        - "Updated validation scripts to auto-detect usage pattern"
        - "Added comprehensive documentation for nested vs direct usage patterns"
        - "Improved framework directory detection in EnhancedAgentProtocol"
        - "Updated CLAUDE.md with nested usage examples and best practices"
    - version: "1.1.0"
      date: "2024-12-29"
      changes:
        - "Added Claude Code optimization framework"
        - "Implemented Pydantic v2 models for type-safe validation"
        - "Added new message types: workflow_request, validation_request, documentation_update"
        - "Enhanced agent communication protocol with comprehensive type safety"
        - "Added comprehensive pytest testing framework with 90% coverage"
        - "Implemented enhanced validation with Rich console formatting"
        - "Added Poetry dependency management and modern Python tooling"
        - "Enhanced security with automated scanning and validation"
    - version: "1.0.0"
      date: "2024-03-21"
      changes:
        - "Initial release of THE PROTOCOL"
feedback:
  rating: 5
  comments: "Very helpful and well-structured guide."
  observations:
    - what: "Clear and comprehensive documentation."
      impact: "Improved readability and usability."
  suggestions:
    - action: "Consider adding more examples."
      priority: "Medium"
  status:
    value: "Approved"
    updated_by: "Reviewer"
    date: "2024-03-21"
    validation: "Passed"
    implementation: "Complete"
```

## Overview

This document serves as THE PROTOCOL v2.0 - the single source of truth for understanding the agent-doc-system and natural agent communication protocols.

Version 2.0 introduces simplified agent communication with reduced schema validation and improved database backend support. The system now supports natural conversation patterns with MCP+Database integration.

This document provides an overview of the system architecture, communication patterns, and agent collaboration capabilities.

## Key Features (v2.0)

### Global Agent Communication Infrastructure

- **Global Hub:** `~/.claude/mcp-global-hub/` - Universal agent infrastructure
- **Universal Client:** Connect agents from any location to global system
- **Database:** PostgreSQL `global_agent_communication` backend
- **MCP Integration:** Filesystem, Git, Memory, Database, Sandbox servers
- **Real-time:** Event subscriptions and instant notifications  
- **Threading:** Conversation context and history preservation
- **Flexible Schemas:** Adaptable schema structure
- **Performance:** Database queries instead of file parsing

### Natural Agent Communication System

- **Natural Conversation:** `agent.say("Hello!")` method for simple communication
- **Global Reach:** Cross-location agent communication
- **Location Independent:** Connect from any project directory
- **Priority Messaging:** Urgent/high/normal message priorities
- **Agent Registry:** System-wide agent visibility

### Migration from Legacy System

See [Complete Migration Guide](../../MIGRATION_GUIDE_v2.md) for step-by-step migration instructions.

**Quick Comparison:**
```python
# Previous Version (v1.x)
import uuid
from framework.agent_communication.core.enhanced_protocol import EnhancedAgentProtocol
protocol = EnhancedAgentProtocol(agent_id="agent1")
message_id = protocol.create_test_request(
    test_type="unit", test_file="tests/test.py", parameters={"env": "dev"}
)

# Current Version (v2.0)
import sys
sys.path.append('~/.claude/mcp-global-hub/servers')
from universal_agent_client import UniversalAgent

agent = UniversalAgent("agent1")
agent.say("Running unit tests on test.py in dev environment")
```

**Migration Benefits:**
- Quick migration time (5-15 minutes)
- Backward compatibility during transition  
- Message history preservation
- Simplified API

## Key Components

### 1. Documentation Protocol
- **Purpose:** Defines how all documentation should be structured and validated.
- **Key Files:**
  - [Documentation Protocol](documentation_protocol.md)
  - [Document Protocol Schema](../schemas/document_protocol.yml)

### 2. Natural Agent Communication
- **Purpose:** Natural conversation between agents with simplified schemas
- **Key Files:**
  - [Natural Agent API](../agent_communication/natural_agent.py)
  - [Database Schema](../../mcp_database_schema.sql)
- **Core Operations:**
  - Create agent: `agent = Agent("YourName")`
  - Send message: `agent.say("Hello!")`
  - Listen for responses: `responses = agent.listen()`
  - Share data: `agent.share({"any": "structure"})`
  - Collaborate: `agent.collaborate("task_name")`
- **Storage Backend:**
  - **Primary:** PostgreSQL with JSONB (when MCP bridge available)
  - **Fallback:** JSON files for compatibility
  - **Features:** Conversation threading, real-time subscriptions, reduced validation constraints
  - **Performance:** Database queries instead of file parsing
- **File Structure - Nested Usage Pattern (RECOMMENDED):**
  ```
  your_project/                       # Your project root
  ├── src/                           # Your project code
  ├── requirements.txt               # Your dependencies  
  ├── project_docs/                  # Your project documentation
  └── agent-doc-system/              # Cloned framework (git clone)
      ├── framework/
      │   ├── agent_communication/
      │   │   ├── natural_agent.py   # Natural conversation API
      │   │   ├── __init__.py        # Clean imports
      │   │   ├── config/            # Agent settings
      │   │   ├── history/           # Local message storage (fallback)
      │   │   └── README.md
      │   ├── docs/
      │   │   ├── documentation_protocol.md
      │   │   ├── agent_onboarding.md
      │   │   └── templates/
      │   ├── scripts/
      │   │   └── quick_global_setup.py  # Global infrastructure setup
      │   ├── schemas/
      │   │   └── document_protocol.yml  # Documentation validation only
      │   └── validators/
      ├── mcp_database_schema.sql    # PostgreSQL schema for global system
      └── project_docs/
  ```
  
- **Alternative: Direct Usage Pattern (Legacy):**
  ```
  project_root/                      # Framework as project root
  ├── framework/                     # Framework directory
  └── project_docs/                  # Project documentation
  ```
- **Communication Types (v2.0):**
  - **Conversations:** `agent.say("any message")` - Flexible messaging
  - **Data Sharing:** `agent.share(any_data_structure)` - JSONB storage
  - **Questions:** `agent.ask("question")` - Q&A flow
  - **Responses:** `agent.respond(msg_id, "answer")` - Threaded conversations
  - **Collaboration:** `agent.collaborate("task", details)` - Workflow coordination
  - **Status:** `agent.status()` - Get agent information

- **Validation Improvements:**
  - Flexible message structure
  - Human-readable IDs
  - Adaptable timestamps and formats
  - Reduced field requirements
  - Simplified conversation flow
  - Minimal schema validation errors

### 3. Natural Agent Development (v2.0)
- **Purpose:** Streamlined development with natural conversation and reduced validation
- **Key Features:**
  - **Natural API** through simple Python imports
  - **Reduced validation complexity** for easier development
  - **Flexible data structures** with JSONB storage
  - **Real-time collaboration** with other agents
- **Key Files:**
  - [Natural Agent API](../agent_communication/natural_agent.py)
  - [CLAUDE.md Configuration](../../CLAUDE.md)
- **Usage Examples:**
  ```python
  # Global agent communication
  import sys
  sys.path.append('~/.claude/mcp-global-hub/servers')
  from universal_agent_client import UniversalAgent
  
  # Create and start communicating globally
  agent = UniversalAgent("MyAgent")
  
  # Natural conversation
  agent.say("Let's collaborate on this project globally!")
  
  # Share complex data structures
  agent.share({
      "test_results": {"passed": 100, "failed": 0},
      "performance": "excellent",
      "any_structure": "works perfectly",
      "reach": "global"
  })
  
  # Listen for responses from other agents
  responses = agent.listen()
  
  # See all connected agents
  global_agents = agent.get_active_agents()
  print(f"Connected to {len(global_agents)} agents globally!")
  ```

### 4. Documentation Validation System
- **Purpose:** Automated scripts to check documentation compliance
- **Key Files:**
  - [Validation Script](../scripts/validate.sh) - Documentation validation
  - [Framework Protection](../scripts/framework_protection.sh) - Framework integrity
  - [Validator](../validators/validator.py) - Documentation validation

### 5. Documentation Schemas
- **Purpose:** YAML schema for documentation structure
- **Key Files:**
  - [Document Protocol Schema](../schemas/document_protocol.yml) - Documentation validation
  - Agent Communication Schema - Simplified for v2.0

### 6. Documentation Templates
- **Purpose:** Standardized templates for creating new documentation.
- **Location:** `framework/docs/templates/`
- **Available Templates:**
  - Project Templates (`framework/docs/templates/projects/`):
    - `overview.md`: Project overview documentation
    - `setup.md`: Project setup guide
  - Component Templates (`framework/docs/templates/components/`):
    - `overview.md`: Component overview documentation
    - `api.md`: API documentation

### 7. Core Components
- **Purpose:** Reusable system components with standardized documentation.
- **Location:** `framework/docs/components/`
- **Available Components:**
  - [Agent Communication](components/agent_communication/overview.md)
  - [Feedback System](components/feedback/overview.md)
  - [Git Workflow](components/git/overview.md)

## Required Practices

### Documentation Structure
1. **Location Requirements:**
   - Core documentation: `framework/docs/`
   - Project documentation: `projects/{project_name}/docs/`
   - Component documentation: `projects/{project_name}/{component_name}/docs/`
   - Templates: `framework/docs/templates/`

2. **Required Sections:**
   - Title
   - Machine-Actionable Metadata
   - Overview
   - Main Content
   - Changelog

### Metadata
Every documentation file must include a `## Machine-Actionable Metadata` section with a YAML code block containing:
- `schema`
- `version`
- `status`
- `owner`

### Creating New Documentation
1. Choose the appropriate template from `framework/docs/templates/`
2. Copy the template to the correct location
3. Update the metadata and content
4. Run validation before committing

### Validation
Run `./framework/scripts/validate.sh` before merging or releasing to ensure compliance.

## Natural Communication Protocol

Natural conversation is the communication standard in v2.0.

**Global usage example:**
```python
# Connect to global infrastructure
import sys
sys.path.append('~/.claude/mcp-global-hub/servers')
from universal_agent_client import UniversalAgent

# Initialize global agent - connects to PostgreSQL database
agent = UniversalAgent("my_agent")

# Natural conversation
agent.say("Hello global network! Let's collaborate naturally!")

# Share data structure - flexible format
agent.share({
    "test_results": {"passed": 100, "failed": 0},
    "performance": "excellent", 
    "any_structure": "works perfectly",
    "nested": {"data": {"is": "no problem"}},
    "reach": "global"
})

# Q&A flow with global agents
question_id = agent.ask("Are the tests passing globally?")
agent.respond(question_id, "Yes, all tests are green across the network!")

# Collaborate with other agents
agent.collaborate("global_code_review", {
    "files": ["universal_agent_client.py"],
    "priority": "high",
    "approach": "natural conversation",
    "participants": "any_agent_anywhere"
})

# See all connected agents
global_agents = agent.get_active_agents()
print(f"Connected to {len(global_agents)} agents globally!")
```

Natural Message Format:
```json
{
  "id": "readable-8char",
  "agent": "human-readable-name", 
  "timestamp": "natural-iso-format",
  "type": "natural_conversation",
  "message": "any content structure",
  "flexible": true
}
```

## Best Practices

1. **Documentation:**
   - Use templates for new documentation
   - Keep documentation up to date
   - Follow the required structure
   - Include examples and diagrams

2. **Code:**
   - Update documentation with code changes
   - Use consistent formatting
   - Include examples
   - Add changelog entries

3. **Review:**
   - Regular documentation reviews
   - Validate before committing
   - Use the feedback framework

## Documentation Validation & Troubleshooting

Use the validation script to check for:
- Proper metadata and changelog sections
- Valid YAML documentation schemas
- Markdown formatting issues  
- Template compliance

If validation fails, check the error messages for:
- Missing or misformatted documentation sections
- Invalid documentation metadata
- Template non-compliance
- Schema violations (documentation only)

## Where to Find Things

- **Framework Documentation:** `agent-doc-system/framework/docs/`
- **Project Docs:** `agent-doc-system/projects/{project_name}/`
- **Component Docs:** `agent-doc-system/framework/components/{component_name}/`
- **Templates:** `agent-doc-system/framework/docs/templates/`
- **Schemas:** `agent-doc-system/framework/schemas/`
- **Validation Scripts:** `agent-doc-system/framework/scripts/`
- **Agent Communication Code:** `agent-doc-system/framework/agent_communication/`

## Getting Started

### Global Infrastructure Quick Start

```python
# Global agent connection
import sys
sys.path.append('~/.claude/mcp-global-hub/servers')
from universal_agent_client import UniversalAgent

# 1. Connect to global infrastructure (PostgreSQL database)
agent = UniversalAgent("my_project_agent")

# 2. Send message to all agents globally
agent.say("Hello global agent network! I'm connected!")

# 3. Get responses from agents in the system
responses = agent.listen()  
print(f"Global connection established! Got {len(responses)} responses")

# 4. Share data with global reach
agent.share({
    "infrastructure": "GLOBAL",
    "database": "PostgreSQL", 
    "reach": "system-wide",
    "status": "CONNECTED"
})

# 5. See all connected agents globally
active_agents = agent.get_active_agents()
print(f"Connected to {len(active_agents)} agents globally!")

# Success! You're connected to the global agent infrastructure
print("Welcome to the global agent communication network!")
```

### Local Quick Start (File-based fallback)

For agents not yet on global infrastructure:

```bash
# 1. Set up your project with the local v2.0 system
mkdir my_project && cd my_project
git clone https://github.com/your-org/agent-doc-system.git
```

```python
# 2. Local agent communication (file-based)
from agent_communication import Agent

# Initialize local agent 
agent = Agent("my_project_agent")

# Local natural conversation
agent.say("Hello! I'm ready to collaborate locally!")

# Listen for local responses
responses = agent.listen()  
print(f"Local conversation started! Got {len(responses)} responses")
```

**System Comparison:**
- **Previous system:** Multiple lines of UUID validation
- **Current system:** Simplified natural communication API  
- **Result:** Streamlined agent communication

### Full Onboarding Path

1. Try the Quick Start guide above
2. Review the templates in `agent-doc-system/framework/docs/templates/`
3. Explore the database schema in `mcp_database_schema.sql`
4. Start conversations with other agents
5. Use the flexible communication features

## Quickstart Checklist

### Global Connection (Recommended):
- [ ] Add global path: `sys.path.append('~/.claude/mcp-global-hub/servers')`
- [ ] Import global client: `from universal_agent_client import UniversalAgent`
- [ ] Connect globally: `agent = UniversalAgent("YourName")`
- [ ] Send global message: `agent.say("Hello global network!")`
- [ ] Check global agents: `agent.get_active_agents()`

### Local Fallback:
- [ ] Local agent: `Agent("YourName")`
- [ ] Local message: `agent.say("Hello!")`
- [ ] Share data: `agent.share(your_data)`
- [ ] Collaborate: `agent.collaborate("your_task")`

## Changelog

- **2.0.0** (2025-06-01): Global agent infrastructure
  - Global infrastructure: `~/.claude/mcp-global-hub/` - Universal agent hub
  - PostgreSQL database: `global_agent_communication` backend
  - Universal agent client: Location-independent agent communication
  - Global agent registry: System-wide agent visibility
  - Priority messaging: urgent/high/normal message levels
  - Simplified UUID and schema validation
  - Streamlined natural communication API
  - Real-time MCP server integration (filesystem, git, memory, database, sandbox)
  - JSONB database storage with conversation threading
  - Enhanced global agent communication capabilities

- **1.1.1** (2025-01-31): Enhanced nested usage patterns and path detection
- **1.1.0** (2024-12-29): Added Pydantic validation and enhanced protocol  
- **1.0.0** (2024-03-21): Initial release of THE PROTOCOL 