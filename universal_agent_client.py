#!/usr/bin/env python3
"""
🤖 Universal Agent Client - Connect ANY agent to Global MCP Hub
System-wide agent communication client that works from anywhere

This is what ALL agents use to connect to the global infrastructure.
Drop this file anywhere and agents can communicate globally!
"""

import json
import logging
import psycopg2
import psycopg2.extras
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversalAgent:
    """
    🤖 Universal Agent Client - Connect to Global MCP Hub
    
    Usage from ANY location:
    agent = UniversalAgent("MyAgent")
    agent.say("Hello global agents!")
    responses = agent.listen()
    """
    
    def __init__(self, agent_name: str, agent_location: str = None):
        """
        Initialize universal agent client
        
        Args:
            agent_name: Your agent's name (globally unique)
            agent_location: Where your agent operates (auto-detected if not provided)
        """
        self.agent_name = agent_name
        self.agent_location = agent_location or str(Path.cwd())
        self.db_conn = None
        self._connect_to_global_hub()
        self._register_agent()
        
        logger.info(f"🤖 {agent_name} connected to Global Agent Communication Hub!")
    
    def _connect_to_global_hub(self):
        """Connect to global MCP hub database"""
        try:
            self.db_conn = psycopg2.connect(
                "dbname=global_agent_communication user=gaanauser003",
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            self.db_conn.autocommit = True
            logger.info("✅ Connected to Global MCP Hub")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Global MCP Hub: {e}")
            logger.error("🔧 Make sure Global MCP Server is running!")
            raise
    
    def _register_agent(self):
        """Register this agent with global hub"""
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO global_agents (agent_name, agent_location, agent_type, capabilities)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (agent_name) 
                    DO UPDATE SET 
                        agent_location = EXCLUDED.agent_location,
                        last_active = NOW()
                """, (
                    self.agent_name, 
                    self.agent_location,
                    'universal_agent',
                    json.dumps({
                        "natural_conversation": True,
                        "global_communication": True,
                        "database_connected": True
                    })
                ))
                
                logger.info(f"📋 {self.agent_name} registered with Global Agent Registry")
        except Exception as e:
            logger.error(f"❌ Agent registration failed: {e}")
    
    def say(self, message: Union[str, Dict[str, Any]], to_agent: str = None, 
            message_type: str = "conversation", priority: int = 0) -> str:
        """
        Say something to another agent or broadcast to all
        
        Args:
            message: What to say (string or complex data)
            to_agent: Specific agent to message (None for broadcast)
            message_type: Type of message
            priority: 0=normal, 1=high, 2=urgent
        
        Returns:
            Message ID
        """
        try:
            # Ensure message is in proper format
            if isinstance(message, str):
                content = {"message": message, "type": "natural_conversation"}
            else:
                content = message
            
            # Add sender info
            content["sent_by"] = self.agent_name
            content["timestamp"] = datetime.now(timezone.utc).isoformat()
            
            message_id = str(uuid.uuid4())
            
            with self.db_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO agent_messages 
                    (id, from_agent, to_agent, message_type, content, priority)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (message_id, self.agent_name, to_agent, message_type, 
                     json.dumps(content), priority))
            
            target = to_agent or "ALL_AGENTS"
            logger.info(f"💬 {self.agent_name} → {target}: {message}")
            
            return message_id
            
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return None
    
    def listen(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Listen for messages addressed to this agent
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of messages
        """
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, from_agent, message_type, content, created_at, priority
                    FROM agent_messages
                    WHERE (to_agent = %s OR to_agent IS NULL) 
                    AND status = 'pending'
                    ORDER BY priority DESC, created_at ASC
                    LIMIT %s
                """, (self.agent_name, limit))
                
                messages = []
                for row in cursor.fetchall():
                    # Mark as delivered
                    cursor.execute("""
                        UPDATE agent_messages 
                        SET status = 'delivered', delivered_at = NOW()
                        WHERE id = %s
                    """, (row['id'],))
                    
                    messages.append({
                        'id': row['id'],
                        'from_agent': row['from_agent'],
                        'message_type': row['message_type'],
                        'content': row['content'],
                        'created_at': row['created_at'].isoformat(),
                        'priority': row['priority']
                    })
                
                if messages:
                    logger.info(f"📬 {self.agent_name} received {len(messages)} messages")
                
                return messages
                
        except Exception as e:
            logger.error(f"❌ Failed to listen for messages: {e}")
            return []
    
    def share(self, data: Dict[str, Any], to_agent: str = None) -> str:
        """Share complex data with agents"""
        return self.say(data, to_agent, "data_share")
    
    def ask(self, question: str, to_agent: str = None) -> str:
        """Ask a question to agents"""
        content = {
            "question": question,
            "expecting_response": True,
            "asked_by": self.agent_name
        }
        return self.say(content, to_agent, "question")
    
    def respond(self, original_message_id: str, response: Union[str, Dict[str, Any]], 
                to_agent: str = None) -> str:
        """Respond to a specific message"""
        content = {
            "response": response,
            "responding_to": original_message_id,
            "response_by": self.agent_name
        }
        return self.say(content, to_agent, "response")
    
    def collaborate(self, task: str, details: Dict[str, Any] = None, 
                   with_agents: List[str] = None) -> str:
        """Start or join a collaboration"""
        content = {
            "task": task,
            "details": details or {},
            "collaboration_initiator": self.agent_name,
            "invited_agents": with_agents
        }
        return self.say(content, None, "collaboration")
    
    def get_active_agents(self) -> List[Dict[str, Any]]:
        """Get list of all active agents in the system"""
        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute("""
                    SELECT agent_name, agent_location, capabilities, last_active
                    FROM global_agents
                    WHERE status = 'active' AND agent_name != %s
                    ORDER BY last_active DESC
                """, (self.agent_name,))
                
                agents = []
                for row in cursor.fetchall():
                    agents.append({
                        'name': row['agent_name'],
                        'location': row['agent_location'],
                        'capabilities': row['capabilities'],
                        'last_active': row['last_active'].isoformat() if row['last_active'] else None
                    })
                
                return agents
                
        except Exception as e:
            logger.error(f"❌ Failed to get active agents: {e}")
            return []
    
    def status(self) -> Dict[str, Any]:
        """Get agent status and connection info"""
        try:
            with self.db_conn.cursor() as cursor:
                # Get pending message count
                cursor.execute("""
                    SELECT COUNT(*) as pending_count
                    FROM agent_messages
                    WHERE (to_agent = %s OR to_agent IS NULL) 
                    AND status = 'pending'
                """, (self.agent_name,))
                pending_count = cursor.fetchone()['pending_count']
                
                # Get agent info
                cursor.execute("""
                    SELECT * FROM global_agents WHERE agent_name = %s
                """, (self.agent_name,))
                agent_info = cursor.fetchone()
                
                return {
                    "agent_name": self.agent_name,
                    "location": self.agent_location,
                    "status": "connected_to_global_hub",
                    "pending_messages": pending_count,
                    "registered_at": agent_info['first_registered'].isoformat() if agent_info else None,
                    "last_active": agent_info['last_active'].isoformat() if agent_info else None,
                    "capabilities": agent_info['capabilities'] if agent_info else {}
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get status: {e}")
            return {"error": str(e)}
    
    def disconnect(self):
        """Disconnect from global hub"""
        if self.db_conn:
            self.db_conn.close()
            logger.info(f"🔌 {self.agent_name} disconnected from Global MCP Hub")

# Convenience function for quick agent creation
def create_global_agent(name: str) -> UniversalAgent:
    """Create a universal agent connected to global hub"""
    return UniversalAgent(name)

# Example usage for testing
if __name__ == "__main__":
    # Demo the universal agent system
    print("🌐 Testing Universal Agent System...")
    
    agent = UniversalAgent("TestAgent")
    
    # Send a test message
    agent.say("Hello from Universal Agent! Testing global communication system!")
    
    # Check for messages
    messages = agent.listen()
    print(f"📬 Received {len(messages)} messages")
    
    # Show active agents
    active_agents = agent.get_active_agents()
    print(f"👥 {len(active_agents)} other agents are active")
    
    # Show status
    status = agent.status()
    print(f"📊 Agent status: {status}")
    
    agent.disconnect()
    print("✅ Universal Agent test complete!")