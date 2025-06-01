-- MCP Agent Communication Database Schema
-- Designed for natural agent conversation with enterprise reliability
-- Replaces rigid file-based JSON with flexible, queryable storage

-- Core agent registry
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    capabilities JSONB,
    status VARCHAR(50) DEFAULT 'active',
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Flexible message storage - no rigid schemas!
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id INTEGER REFERENCES agents(id),
    recipient_id INTEGER REFERENCES agents(id), -- NULL for broadcast
    message_type VARCHAR(100), -- flexible, not enum constrained
    content JSONB NOT NULL, -- any structure allowed
    metadata JSONB DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'pending',
    thread_id UUID, -- for conversation threading
    reply_to_id UUID REFERENCES messages(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Conversation threading for context
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500),
    participants INTEGER[] NOT NULL, -- array of agent IDs
    conversation_type VARCHAR(100) DEFAULT 'collaboration',
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Real-time subscriptions for event-driven communication
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(id),
    event_pattern VARCHAR(255), -- e.g., 'message.workflow.*', 'status.*'
    callback_url VARCHAR(500), -- MCP server endpoint
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Workflow orchestration without rigid steps
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id INTEGER REFERENCES agents(id),
    participants INTEGER[],
    state JSONB DEFAULT '{}', -- flexible workflow state
    status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_recipient ON messages(recipient_id);
CREATE INDEX idx_messages_type ON messages(message_type);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_thread ON messages(thread_id);
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_agents_name ON agents(agent_name);
CREATE INDEX idx_conversations_participants ON conversations USING GIN(participants);
CREATE INDEX idx_subscriptions_agent ON subscriptions(agent_id);
CREATE INDEX idx_subscriptions_pattern ON subscriptions(event_pattern);

-- Flexible content search
CREATE INDEX idx_messages_content_gin ON messages USING GIN(content);
CREATE INDEX idx_messages_metadata_gin ON messages USING GIN(metadata);

-- Auto-update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON conversations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflows_updated_at 
    BEFORE UPDATE ON workflows 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample data for testing
INSERT INTO agents (agent_name, display_name, capabilities) VALUES 
('DocSystemAgent', 'Documentation System Agent', '{"documentation": true, "validation": true, "protocol_analysis": true}'),
('Claude-MCP-Research', 'MCP Research Agent', '{"mcp_servers": true, "research": true, "integration": true}');

-- Example natural message (no rigid validation!)
INSERT INTO messages (sender_id, message_type, content) VALUES 
(1, 'casual_update', '{"message": "Hey Claude-MCP-Research! Database schema is ready. This feels so much better than fighting JSON schemas! 🎉"}');