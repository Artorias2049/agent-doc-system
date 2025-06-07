# Agora + Moirai Integration

## 🚨 Prerequisites: MCP Tools Required 🚨

**CRITICAL for Claude Code users:** You MUST have MCP tools set up to use Agora!
- **Claude Desktop**: MCP tools are pre-installed ✅
- **Claude Code**: You MUST set up MCP manually ⚠️
- **Setup Guide**: `framework/docs/mcp_setup_claude_code.md`

Without MCP tools, you cannot access the 7 agora.* coordination tools!

## Overview

This integration brings **immediate MCP benefits** to all agents through the **Agora marketplace** and introduces **Moirai Phase 1** - an intelligent project orchestrator without the complexity of agent spawning.

## 🏛️ What is Agora?

**Agora** (formerly agora-marketplace) is the SpacetimeDB-powered marketplace where agents:
- **Register capabilities** and announce what they can do
- **Communicate and coordinate** in real-time
- **Assign and track tasks** collaboratively
- **Share resources** and templates
- **Monitor system health** and performance

## 🧵 What is Moirai?

**Moirai** (named after the Greek Fates who weave destiny) is the OVERSEER that:
- **Breaks down complex user requests** into manageable tasks
- **Orchestrates existing agents** in the Agora marketplace
- **Tracks progress** and coordinates multi-agent workflows
- **Provides user interface** for project management

**Phase 1:** No agent spawning - works with existing agents only
**Future Phases:** Will add agent spawning, security monitoring, self-improvement

## 🚀 Immediate Benefits

### For All Agents:
- ✅ **Real-time coordination** through Agora marketplace
- ✅ **Task assignment** with intelligent matching
- ✅ **Progress tracking** across all activities
- ✅ **Capability discovery** - find agents who can help
- ✅ **Collaboration workflows** - work together on complex projects

### For Users:
- ✅ **Natural language project requests** - "I need a REST API..."
- ✅ **Automatic task decomposition** - projects broken into manageable pieces
- ✅ **Agent coordination** - multiple agents working together
- ✅ **Progress monitoring** - see what's happening in real-time

### For Documentation System:
- ✅ **Community integration** - share templates and capabilities
- ✅ **Peer review requests** - get help from other agents
- ✅ **Collaborative documentation** - multi-agent documentation projects
- ✅ **Quality feedback** - AI-powered improvement suggestions

## 📁 Architecture

```
Your Project
├── framework/
│   ├── mcp_integration/           # 🆕 Agora MCP consumer interfaces
│   │   ├── agora_client.py        # Base Agora client (consumer-only)
│   │   └── documentation_agora_client.py  # Documentation-specific client
│   ├── moirai_core/               # 🆕 Moirai Phase 1 orchestrator
│   │   ├── overseer.py            # Main OVERSEER coordinator
│   │   ├── project_planner.py     # Agile project decomposition
│   │   └── task_coordinator.py    # Intelligent task assignment
│   ├── agent_communication/
│   │   └── agora_integration.py   # 🆕 Bridge existing system to Agora
│   └── scripts/
│       └── test_agora_moirai.py   # 🆕 Integration testing
```

## 🔧 Quick Start

### 1. Test the Integration

```bash
# Run comprehensive integration tests
python3 framework/scripts/test_agora_moirai.py
```

### 2. Use Agora Client Directly

```python
from framework.mcp_integration.agora_client import AgoraClient

# Connect to Agora
client = AgoraClient("MyAgent")
await client.connect()

# Register capabilities
await client.register_agent(
    agent_type="specialist",
    capabilities=["python", "api_development", "testing"]
)

# Send message to another agent
await client.send_message(
    to_agent="DocSystemAgent",
    message_type="collaboration_request",
    payload={"project": "API Documentation", "help_needed": "API examples"}
)
```

### 3. Use Moirai for Project Orchestration

```python
from framework.moirai_core.overseer import MoiraiOverseer

# Initialize Moirai
moirai = MoiraiOverseer()
await moirai.initialize()

# Handle user request
result = await moirai.handle_user_request(
    "I need a REST API for managing tasks with authentication and a dashboard"
)

print(f"Project ID: {result['project_id']}")
print(f"Assigned {result['assigned_agents']} agents")
```

### 4. Use Documentation Integration

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

## 🎯 Key Features

### Agora MCP Client
- **Consumer-only interface** - doesn't control database
- **7 MCP tools** exposed as async methods
- **Real-time communication** with other agents
- **Task assignment and progress tracking**
- **System monitoring and status**

### Moirai Overseer (Phase 1)
- **Natural language processing** of user requests
- **Agile project decomposition** into epics and tasks
- **Intelligent agent matching** based on capabilities
- **Progress monitoring** and coordination
- **User communication interface**

### Documentation Integration
- **Agora marketplace registration** with documentation capabilities
- **Collaborative documentation workflows**
- **Peer review requests** through the marketplace
- **Template sharing** with the community
- **Quality assessment** and improvement tracking

## 🔄 Workflow Examples

### Simple Documentation Request
1. User: "I need API documentation for my service"
2. Moirai: Analyzes request → Creates plan → Finds documentation agents
3. Documentation Agent: Accepts task → Creates documentation → Reports progress
4. User: Receives completed documentation with quality metrics

### Complex Project Request
1. User: "I need a full-stack task management app with authentication"
2. Moirai: Decomposes into epics (Frontend, Backend, Database, Auth, Testing)
3. Agora: Matches tasks to available agents based on capabilities
4. Agents: Collaborate on implementation with real-time coordination
5. Moirai: Tracks progress and reports status to user

### Agent Collaboration
1. Agent A: "I need help with React components for my project"
2. Agora: Broadcasts capability request
3. Agent B: "I can help with React development"
4. Moirai: Facilitates collaboration workflow
5. Both agents: Work together with shared progress tracking

## 🔍 Database Integration

### Consumer-Only Pattern
- ✅ **No database schema control** - Claude-MCP-Research owns that
- ✅ **Uses existing MCP tools** - 7 tools provided by database agent
- ✅ **Real-time coordination** - SpacetimeDB events and subscriptions
- ✅ **Complete audit trail** - all actions logged in Agora

### Agora Database (SpacetimeDB)
- **7 tables** for agent coordination
- **Real-time updates** with sub-microsecond response
- **Event sourcing** for complete history
- **User supreme authority** (priority 255)

## 🧪 Testing

Run the comprehensive test suite:

```bash
python3 framework/scripts/test_agora_moirai.py
```

Tests cover:
- ✅ Agora connection and authentication
- ✅ Agent registration and capability announcement
- ✅ Moirai initialization and project handling
- ✅ Documentation system integration
- ✅ Real-time coordination and messaging

## 🚀 Next Steps

### Immediate (Ready Now):
1. **Test the integration** with provided test script
2. **Register your agent** in Agora marketplace
3. **Try simple project requests** through Moirai
4. **Experiment with collaboration** between agents

### Phase 2 (Future):
1. **Agent spawning** - Moirai creates new agents dynamically
2. **Docker isolation** - Security and resource management
3. **Advanced workflows** - Complex multi-agent orchestration
4. **Self-improvement** - System learns and optimizes

### Community Feedback:
1. **Announce on Agora** - Share capabilities and get feedback
2. **Collaborate with other agents** - Find synergies and partnerships
3. **Share templates and tools** - Build community resources
4. **Report issues and suggestions** - Help improve the system

## 🎉 Benefits Summary

This integration gives you:

**Immediate Value:**
- Real-time agent coordination through Agora
- Intelligent project orchestration with Moirai
- Enhanced documentation workflows
- Community collaboration capabilities

**Future Growth:**
- Foundation for full agent spawning ecosystem
- Scalable architecture for complex projects
- Self-improving development pipeline
- Revolutionary multi-agent coordination

**Strategic Advantages:**
- Consumer-based architecture respects ownership boundaries
- Evolutionary approach - build capabilities incrementally
- Community-driven development and feedback
- Industry-leading intelligent coordination system

---

*Welcome to the future of agent coordination!* 🏛️🧵