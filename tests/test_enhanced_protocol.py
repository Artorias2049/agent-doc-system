"""
Test cases for the enhanced agent communication protocol.
"""

import json
import pytest
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, mock_open
from pydantic import ValidationError

import sys
sys.path.append(str(Path(__file__).parent.parent / "framework" / "agent_communication" / "core"))

from models import (
    AgentMessage, MessageFile, MessageType, MessageStatus,
    TestRequestContent, StatusUpdateContent, TestParameters, Environment, TestType
)
from enhanced_protocol import EnhancedAgentProtocol


class TestEnhancedAgentProtocol:
    """Test cases for EnhancedAgentProtocol."""
    
    def test_protocol_initialization(self, temp_root_dir):
        """Test protocol initialization."""
        protocol = EnhancedAgentProtocol(
            agent_id="test_agent",
            root_dir=str(temp_root_dir),
            environment="development"
        )
        
        assert protocol.agent_id == "test_agent"
        assert protocol.environment == "development"
        assert protocol.root_dir == temp_root_dir
        assert protocol.message_file.name == "dev_messages.json"
        assert protocol.message_file.exists()
    
    def test_protocol_initialization_different_environments(self, temp_root_dir):
        """Test protocol initialization with different environments."""
        # Development
        dev_protocol = EnhancedAgentProtocol(
            agent_id="test_agent",
            root_dir=str(temp_root_dir),
            environment="development"
        )
        assert dev_protocol.message_file.name == "dev_messages.json"
        
        # Staging
        staging_protocol = EnhancedAgentProtocol(
            agent_id="test_agent",
            root_dir=str(temp_root_dir),
            environment="staging"
        )
        assert staging_protocol.message_file.name == "staging_messages.json"
        
        # Production
        prod_protocol = EnhancedAgentProtocol(
            agent_id="test_agent",
            root_dir=str(temp_root_dir),
            environment="production"
        )
        assert prod_protocol.message_file.name == "agent_messages.json"
    
    def test_auto_detect_root_dir(self):
        """Test automatic root directory detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create framework directory to simulate project root
            (temp_path / "framework").mkdir()
            
            # Change to subdirectory
            sub_dir = temp_path / "subdir"
            sub_dir.mkdir()
            
            with patch('pathlib.Path.cwd', return_value=sub_dir):
                protocol = EnhancedAgentProtocol(agent_id="test_agent")
                assert protocol.root_dir == temp_path
    
    def test_send_message_valid(self, sample_agent_protocol):
        """Test sending a valid message."""
        content_data = {
            "test_type": "unit",
            "test_file": "tests/test_example.py",
            "parameters": {
                "environment": "development",
                "verbose": True
            }
        }
        
        message_id = sample_agent_protocol.send_message(
            message_type=MessageType.TEST_REQUEST,
            content=content_data
        )
        
        assert message_id is not None
        
        # Verify message was stored
        messages = sample_agent_protocol.get_messages()
        assert len(messages) == 1
        assert str(messages[0].id) == message_id
        assert messages[0].type == MessageType.TEST_REQUEST
    
    def test_send_message_invalid_content(self, sample_agent_protocol):
        """Test sending a message with invalid content."""
        invalid_content = {
            "test_type": "invalid_type",  # Invalid enum value
            "test_file": "tests/test_example.py",
            "parameters": {
                "environment": "development"
            }
        }
        
        with pytest.raises(ValueError):
            sample_agent_protocol.send_message(
                message_type=MessageType.TEST_REQUEST,
                content=invalid_content
            )
    
    def test_send_message_string_type(self, sample_agent_protocol):
        """Test sending a message with string message type."""
        content_data = {
            "test_type": "unit",
            "test_file": "tests/test_example.py", 
            "parameters": {
                "environment": "development",
                "verbose": True
            }
        }
        
        message_id = sample_agent_protocol.send_message(
            message_type="test_request",  # String instead of enum
            content=content_data
        )
        
        assert message_id is not None
        messages = sample_agent_protocol.get_messages()
        assert len(messages) == 1
        assert messages[0].type == MessageType.TEST_REQUEST
    
    def test_send_message_invalid_type_string(self, sample_agent_protocol):
        """Test sending a message with invalid string type."""
        content_data = {"test": "data"}
        
        with pytest.raises(ValueError):
            sample_agent_protocol.send_message(
                message_type="invalid_message_type",
                content=content_data
            )
    
    def test_get_messages_no_filters(self, sample_agent_protocol, sample_messages_data):
        """Test getting all messages without filters."""
        # Add some test messages
        for msg_data in sample_messages_data:
            sample_agent_protocol.send_message(
                message_type=msg_data["type"],
                content=msg_data["content"]
            )
        
        messages = sample_agent_protocol.get_messages()
        assert len(messages) == len(sample_messages_data)
    
    def test_get_messages_with_status_filter(self, sample_agent_protocol):
        """Test getting messages filtered by status."""
        # Send a message
        sample_agent_protocol.send_message(
            message_type=MessageType.TEST_REQUEST,
            content={
                "test_type": "unit",
                "test_file": "tests/test.py",
                "parameters": {"environment": "development"}
            }
        )
        
        # Get pending messages
        pending_messages = sample_agent_protocol.get_messages(status=MessageStatus.PENDING)
        assert len(pending_messages) == 1
        assert pending_messages[0].status == MessageStatus.PENDING
        
        # Get processed messages (should be empty)
        processed_messages = sample_agent_protocol.get_messages(status=MessageStatus.PROCESSED)
        assert len(processed_messages) == 0
    
    def test_get_messages_with_type_filter(self, sample_agent_protocol):
        """Test getting messages filtered by type."""
        # Send different types of messages
        sample_agent_protocol.send_message(
            message_type=MessageType.TEST_REQUEST,
            content={
                "test_type": "unit",
                "test_file": "tests/test.py",
                "parameters": {"environment": "development"}
            }
        )
        
        sample_agent_protocol.send_message(
            message_type=MessageType.STATUS_UPDATE,
            content={
                "agent_id": "test_agent",
                "state": "busy",
                "progress": 50.0
            }
        )
        
        # Filter by test_request
        test_messages = sample_agent_protocol.get_messages(message_type=MessageType.TEST_REQUEST)
        assert len(test_messages) == 1
        assert test_messages[0].type == MessageType.TEST_REQUEST
        
        # Filter by status_update
        status_messages = sample_agent_protocol.get_messages(message_type=MessageType.STATUS_UPDATE)
        assert len(status_messages) == 1
        assert status_messages[0].type == MessageType.STATUS_UPDATE
    
    def test_get_messages_with_limit(self, sample_agent_protocol):
        """Test getting messages with limit."""
        # Send multiple messages
        for i in range(5):
            sample_agent_protocol.send_message(
                message_type=MessageType.STATUS_UPDATE,
                content={
                    "agent_id": f"agent_{i}",
                    "state": "idle",
                    "progress": 100.0
                }
            )
        
        # Get limited messages
        limited_messages = sample_agent_protocol.get_messages(limit=3)
        assert len(limited_messages) == 3
    
    def test_update_message_status(self, sample_agent_protocol):
        """Test updating message status."""
        # Send a message
        message_id = sample_agent_protocol.send_message(
            message_type=MessageType.TEST_REQUEST,
            content={
                "test_type": "unit",
                "test_file": "tests/test.py",
                "parameters": {"environment": "development"}
            }
        )
        
        # Update status
        success = sample_agent_protocol.update_message_status(
            message_id=message_id,
            status=MessageStatus.PROCESSED,
            metadata_update={"processed_at": "2024-12-29T12:00:00Z"}
        )
        
        assert success is True
        
        # Verify status was updated
        messages = sample_agent_protocol.get_messages()
        updated_message = next(msg for msg in messages if str(msg.id) == message_id)
        assert updated_message.status == MessageStatus.PROCESSED
        assert updated_message.metadata["processed_at"] == "2024-12-29T12:00:00Z"
    
    def test_update_message_status_not_found(self, sample_agent_protocol):
        """Test updating status of non-existent message."""
        success = sample_agent_protocol.update_message_status(
            message_id="non-existent-id",
            status=MessageStatus.PROCESSED
        )
        
        assert success is False
    
    def test_cleanup_old_messages(self, sample_agent_protocol):
        """Test cleaning up old messages."""
        # Manually add old and new messages
        message_file = sample_agent_protocol._read_message_file()
        
        # Add old processed message
        old_message = AgentMessage(
            sender="old_agent",
            type=MessageType.STATUS_UPDATE,
            content={
                "agent_id": "old_agent",
                "state": "idle",
                "progress": 100.0
            },
            status=MessageStatus.PROCESSED
        )
        old_message.timestamp = datetime.utcnow() - timedelta(days=10)
        
        # Add recent message
        recent_message = AgentMessage(
            sender="recent_agent",
            type=MessageType.STATUS_UPDATE,
            content={
                "agent_id": "recent_agent",
                "state": "busy",
                "progress": 50.0
            },
            status=MessageStatus.PENDING
        )
        
        message_file.messages = [old_message, recent_message]
        sample_agent_protocol._write_message_file(message_file)
        
        # Cleanup with 7 days retention
        cleaned_count = sample_agent_protocol.cleanup_old_messages(days=7, archive=False)
        
        assert cleaned_count == 1
        
        # Verify only recent message remains
        remaining_messages = sample_agent_protocol.get_messages()
        assert len(remaining_messages) == 1
        assert remaining_messages[0].sender == "recent_agent"
    
    def test_cleanup_with_archiving(self, sample_agent_protocol):
        """Test cleanup with archiving enabled."""
        # Add old processed message
        message_file = sample_agent_protocol._read_message_file()
        old_message = AgentMessage(
            sender="old_agent",
            type=MessageType.STATUS_UPDATE,
            content={
                "agent_id": "old_agent",
                "state": "idle",
                "progress": 100.0
            },
            status=MessageStatus.PROCESSED
        )
        old_message.timestamp = datetime.utcnow() - timedelta(days=10)
        message_file.messages = [old_message]
        sample_agent_protocol._write_message_file(message_file)
        
        # Cleanup with archiving
        cleaned_count = sample_agent_protocol.cleanup_old_messages(days=7, archive=True)
        
        assert cleaned_count == 1
        
        # Check that archive file was created
        archive_files = list(sample_agent_protocol.message_dir.glob("archive_*.json"))
        assert len(archive_files) == 1
        
        # Verify archive content
        with open(archive_files[0]) as f:
            archive_data = json.load(f)
        assert len(archive_data["messages"]) == 1
        assert archive_data["messages"][0]["sender"] == "old_agent"
    
    def test_validate_all_messages(self, sample_agent_protocol):
        """Test validating all messages."""
        # Add valid messages
        sample_agent_protocol.send_message(
            message_type=MessageType.TEST_REQUEST,
            content={
                "test_type": "unit",
                "test_file": "tests/test.py",
                "parameters": {"environment": "development"}
            }
        )
        
        # Run validation
        report = sample_agent_protocol.validate_all_messages()
        
        assert report["total_messages"] == 1
        assert report["valid_messages"] == 1
        assert report["invalid_messages"] == 0
        assert len(report["errors"]) == 0
    
    def test_corrupted_message_file_recovery(self, temp_root_dir):
        """Test recovery from corrupted message file."""
        # Create corrupted message file
        message_dir = temp_root_dir / "framework" / "agent_communication" / "history"
        message_file = message_dir / "dev_messages.json"
        
        with open(message_file, "w") as f:
            f.write("invalid json content")
        
        # Initialize protocol - should handle corruption gracefully
        protocol = EnhancedAgentProtocol(
            agent_id="test_agent",
            root_dir=str(temp_root_dir),
            environment="development"
        )
        
        # Should create backup and new file
        backup_file = message_dir / "dev_messages.backup.json"
        assert backup_file.exists()
        assert message_file.exists()
        
        # New file should be valid
        message_file_obj = protocol._read_message_file()
        assert isinstance(message_file_obj, MessageFile)
        assert len(message_file_obj.messages) == 0
    
    def test_config_loading(self, temp_root_dir):
        """Test configuration loading."""
        # Create custom config
        config_data = {
            "agent_communication": {
                "cleanup_policy": {"default_retention_days": 14},
                "validation": {"strict_mode": False}
            }
        }
        
        config_file = temp_root_dir / ".claude" / "config" / "agent_settings.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)
        
        protocol = EnhancedAgentProtocol(
            agent_id="test_agent",
            root_dir=str(temp_root_dir)
        )
        
        assert protocol.config["agent_communication"]["cleanup_policy"]["default_retention_days"] == 14
        assert protocol.config["agent_communication"]["validation"]["strict_mode"] is False
    
    def test_config_defaults(self, temp_root_dir):
        """Test default configuration when no config file exists."""
        # Remove config file if it exists
        config_file = temp_root_dir / ".claude" / "config" / "agent_settings.json"
        if config_file.exists():
            config_file.unlink()
        
        protocol = EnhancedAgentProtocol(
            agent_id="test_agent",
            root_dir=str(temp_root_dir)
        )
        
        # Should use defaults
        assert "agent_communication" in protocol.config
        assert protocol.config["agent_communication"]["cleanup_policy"]["default_retention_days"] == 7


class TestProtocolEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_send_message_with_metadata(self, sample_agent_protocol):
        """Test sending message with custom metadata."""
        content_data = {
            "test_type": "unit",
            "test_file": "tests/test.py",
            "parameters": {"environment": "development"}
        }
        
        metadata = {"priority": "high", "tags": ["critical"]}
        
        message_id = sample_agent_protocol.send_message(
            message_type=MessageType.TEST_REQUEST,
            content=content_data,
            metadata=metadata
        )
        
        messages = sample_agent_protocol.get_messages()
        message = next(msg for msg in messages if str(msg.id) == message_id)
        assert message.metadata["priority"] == "high"
        assert message.metadata["tags"] == ["critical"]
    
    def test_multiple_filters_get_messages(self, sample_agent_protocol):
        """Test getting messages with multiple filters."""
        # Send different messages
        sample_agent_protocol.send_message(
            message_type=MessageType.TEST_REQUEST,
            content={
                "test_type": "unit",
                "test_file": "tests/test.py",
                "parameters": {"environment": "development"}
            }
        )
        
        sample_agent_protocol.send_message(
            message_type=MessageType.STATUS_UPDATE,
            content={
                "agent_id": "test_agent",
                "state": "busy",
                "progress": 50.0
            }
        )
        
        # Get with multiple filters
        filtered_messages = sample_agent_protocol.get_messages(
            status=MessageStatus.PENDING,
            message_type=MessageType.TEST_REQUEST,
            sender="test_agent_001"
        )
        
        assert len(filtered_messages) == 1
        assert filtered_messages[0].type == MessageType.TEST_REQUEST
        assert filtered_messages[0].status == MessageStatus.PENDING
    
    def test_large_message_handling(self, sample_agent_protocol):
        """Test handling of large messages."""
        # Create large content
        large_logs = ["Log line " + str(i) for i in range(1000)]
        
        content_data = {
            "agent_id": "test_agent",
            "state": "busy",
            "progress": 50.0,
            "current_task": "Processing large dataset",
            "large_data": large_logs  # This will be in metadata
        }
        
        message_id = sample_agent_protocol.send_message(
            message_type=MessageType.STATUS_UPDATE,
            content={
                "agent_id": "test_agent",
                "state": "busy", 
                "progress": 50.0
            },
            metadata={"large_data": large_logs}
        )
        
        assert message_id is not None
        
        # Verify large message was stored and can be retrieved
        messages = sample_agent_protocol.get_messages()
        large_message = next(msg for msg in messages if str(msg.id) == message_id)
        assert len(large_message.metadata["large_data"]) == 1000