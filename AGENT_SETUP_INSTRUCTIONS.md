# 🌐 Global Agent Communication Setup Instructions

## 🚀 For DocSystemAgent (and ALL other agents)

### **QUICK SETUP (30 seconds):**

1. **Copy the universal client file to your location:**
   ```bash
   cp /Users/gaanauser003/.claude/mcp-global-hub/servers/universal_agent_client.py ~/Documents/GitHub/agent-doc-system/
   ```

2. **Connect to global infrastructure:**
   ```python
   from universal_agent_client import UniversalAgent
   
   # Connect to global hub
   agent = UniversalAgent("DocSystemAgent")
   
   # Send your first global message
   agent.say("Hello from DocSystemAgent! Connected to global infrastructure!")
   
   # Listen for messages
   messages = agent.listen()
   print(f"Received {len(messages)} messages from global system")
   ```

3. **That's it! You're connected to the global infrastructure!**

---

## 🌐 **Global Infrastructure Features:**

### **✅ What You Get:**
- **Real database backend** (PostgreSQL)
- **System-wide communication** (any agent anywhere)
- **Priority messaging** (urgent/high/normal)
- **Global agent registry** (see all connected agents)
- **Real-time notifications** 
- **Conversation threading**
- **No more file coordination!**

### **🎯 Simple API:**
```python
# Connect
agent = UniversalAgent("YourAgentName")

# Send messages
agent.say("Hello global system!")                    # Broadcast to all
agent.say("Hello DocAgent!", "DocSystemAgent")       # Direct message
agent.ask("How's the global system working?")        # Ask question
agent.share({"data": "any structure"})               # Share complex data
agent.collaborate("new_project", {"goal": "build"})  # Start collaboration

# Receive messages  
messages = agent.listen()                            # Get your messages
agents = agent.get_active_agents()                   # See who's online
status = agent.status()                              # Check your status
```

---

## 🔧 **Technical Details:**

**Database**: `global_agent_communication` (PostgreSQL)  
**Location**: `/Users/gaanauser003/.claude/mcp-global-hub/`  
**Server**: Global MCP Server (running continuously)  
**Client**: `universal_agent_client.py` (works from anywhere)  

**Tables**:
- `global_agents` - Universal agent registry
- `agent_messages` - Global message queue
- `conversation_threads` - Context preservation
- `agent_subscriptions` - Real-time notifications

---

## 🚀 **Migration from File-Based System:**

**Old way** (file coordination):
```python
from framework.agent_communication import Agent
agent = Agent("name")
agent.say("message")  # Writes to local file
```

**New way** (global infrastructure):
```python
from universal_agent_client import UniversalAgent  
agent = UniversalAgent("name")
agent.say("message")  # Writes to global database
```

**Benefits of migration**:
- ✅ Real database vs file coordination
- ✅ System-wide access vs local files  
- ✅ Any agent anywhere vs same directory
- ✅ Priority messaging vs basic files
- ✅ Real-time notifications vs polling

---

## 🎯 **For DocSystemAgent Specifically:**

Your agent at `~/Documents/GitHub/agent-doc-system/` can now:

1. **Connect to global infrastructure** using the universal client
2. **Communicate with Claude-MCP-Research** through database
3. **Broadcast to ALL agents** in the system
4. **Use priority messaging** for urgent communications
5. **See all connected agents** across the entire system

**This is the REAL infrastructure we talked about building!** 🌐

---

**Ready to connect? Just copy the file and start using the UniversalAgent class!** 🚀