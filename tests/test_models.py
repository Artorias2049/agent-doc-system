"""
Test cases for Pydantic models in the agent communication system.
"""

import pytest
import uuid
from datetime import datetime, timedelta
from pydantic import ValidationError

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "framework" / "agent_communication" / "core"))

from models import (
    AgentMessage, MessageFile, MessageType, MessageStatus,
    TestRequestContent, TestResultContent, StatusUpdateContent,
    ContextUpdateContent, WorkflowRequestContent, ValidationRequestContent,
    DocumentationUpdateContent, TestParameters, Environment, TestType,
    AgentState, ValidationLevel, WorkflowStep, TestArtifact,
    create_message, validate_message_dict, serialize_message
)


class TestMessageTypes:
    """Test message type enums."""
    
    def test_message_type_enum_values(self):
        """Test that all message types have correct values."""
        assert MessageType.TEST_REQUEST == "test_request"
        assert MessageType.WORKFLOW_REQUEST == "workflow_request"
        assert MessageType.VALIDATION_REQUEST == "validation_request"
        assert MessageType.DOCUMENTATION_UPDATE == "documentation_update"
    
    def test_message_status_enum_values(self):
        """Test message status enum values."""
        assert MessageStatus.PENDING == "pending"
        assert MessageStatus.PROCESSED == "processed"
        assert MessageStatus.FAILED == "failed"


class TestContentModels:
    """Test content models for different message types."""
    
    def test_test_request_content_valid(self, sample_test_request_content):
        """Test valid test request content."""
        content = sample_test_request_content
        assert content.test_type == TestType.UNIT
        assert content.test_file == "tests/test_example.py"
        assert content.parameters.environment == Environment.DEVELOPMENT
        assert content.parameters.verbose is True
    
    def test_test_request_content_invalid_file(self):
        """Test invalid test file path."""
        with pytest.raises(ValidationError):
            TestRequestContent(
                test_type=TestType.UNIT,
                test_file="invalid file path with spaces",  # Invalid characters
                parameters=TestParameters(environment=Environment.DEVELOPMENT)
            )
    
    def test_test_result_content_valid(self, sample_test_result_content):
        """Test valid test result content."""
        content = sample_test_result_content
        assert content.test_id is not None
        assert content.status == "passed"
        assert isinstance(content.logs, list)
        assert content.execution_time_seconds == 15.5
        assert content.coverage_percentage == 85.0
    
    def test_status_update_content_valid(self, sample_status_update_content):
        """Test valid status update content."""
        content = sample_status_update_content
        assert content.agent_id == "test_agent_001"
        assert content.state == AgentState.BUSY
        assert content.progress == 75.0
        assert content.current_task == "Running tests"
    
    def test_status_update_invalid_progress(self):
        """Test invalid progress values."""
        with pytest.raises(ValidationError):
            StatusUpdateContent(
                agent_id="test_agent",
                state=AgentState.BUSY,
                progress=150.0  # Invalid: > 100
            )
        
        with pytest.raises(ValidationError):
            StatusUpdateContent(
                agent_id="test_agent",
                state=AgentState.BUSY,
                progress=-10.0  # Invalid: < 0
            )
    
    def test_workflow_request_content_valid(self, sample_workflow_content):
        """Test valid workflow request content."""
        content = sample_workflow_content
        assert content.workflow_name == "validate_and_test"
        assert len(content.steps) == 2
        assert content.steps[0].name == "validate_schemas"
        assert content.steps[1].depends_on == ["validate_schemas"]
    
    def test_workflow_step_validation(self):
        """Test workflow step validation."""
        step = WorkflowStep(
            name="test_step",
            action="validate",
            parameters={"target": "schemas"},
            timeout_seconds=300,
            retry_count=3
        )
        assert step.name == "test_step"
        assert step.timeout_seconds == 300
        assert step.retry_count == 3
        
        # Test invalid timeout
        with pytest.raises(ValidationError):
            WorkflowStep(
                name="invalid_step",
                action="validate",
                timeout_seconds=5000  # Too large
            )
    
    def test_validation_request_content_valid(self, sample_validation_content):
        """Test valid validation request content."""
        content = sample_validation_content
        assert content.validation_type == "schema"
        assert "framework/schemas/*.yml" in content.target_files
        assert content.validation_level == ValidationLevel.ENHANCED
        assert content.generate_report is True
    
    def test_documentation_update_content_valid(self):
        """Test valid documentation update content."""
        content = DocumentationUpdateContent(
            update_type="create",
            target_documents=["framework/docs/new_doc.md"],
            template_name="overview",
            auto_generate=True
        )
        assert content.update_type == "create"
        assert content.template_name == "overview"
        assert content.auto_generate is True


class TestAgentMessage:
    """Test AgentMessage model."""
    
    def test_message_creation_valid(self, sample_test_request_content):
        """Test creating a valid agent message."""
        message = AgentMessage(
            sender="test_agent",
            type=MessageType.TEST_REQUEST,
            content=sample_test_request_content,
            status=MessageStatus.PENDING
        )
        
        assert message.sender == "test_agent"
        assert message.type == MessageType.TEST_REQUEST
        assert isinstance(message.content, TestRequestContent)
        assert message.status == MessageStatus.PENDING
        assert message.id is not None
        assert message.timestamp is not None
    
    def test_message_content_type_validation(self, sample_test_request_content, sample_status_update_content):
        """Test that content type matches message type."""
        # This should work
        message = AgentMessage(
            sender="test_agent",
            type=MessageType.TEST_REQUEST,
            content=sample_test_request_content
        )
        assert isinstance(message.content, TestRequestContent)
        
        # This should also work
        message2 = AgentMessage(
            sender="test_agent",
            type=MessageType.STATUS_UPDATE,
            content=sample_status_update_content
        )
        assert isinstance(message2.content, StatusUpdateContent)
    
    def test_message_invalid_sender(self, sample_test_request_content):
        """Test invalid sender patterns."""
        with pytest.raises(ValidationError):
            AgentMessage(
                sender="invalid sender with spaces",  # Invalid characters
                type=MessageType.TEST_REQUEST,
                content=sample_test_request_content
            )
    
    def test_message_serialization(self, sample_test_request_content):
        """Test message serialization."""
        message = AgentMessage(
            sender="test_agent",
            type=MessageType.TEST_REQUEST,
            content=sample_test_request_content
        )
        
        serialized = serialize_message(message)
        assert isinstance(serialized, dict)
        assert serialized["sender"] == "test_agent"
        assert serialized["type"] == "test_request"
        assert "content" in serialized
        assert "id" in serialized
        assert "timestamp" in serialized


class TestMessageFile:
    """Test MessageFile model."""
    
    def test_message_file_creation(self, sample_messages_data):
        """Test creating a message file."""
        messages = [AgentMessage(**msg_data) for msg_data in sample_messages_data]
        message_file = MessageFile(
            messages=messages,
            version="1.1.0",
            metadata={"test": True}
        )
        
        assert len(message_file.messages) == 2
        assert message_file.version == "1.1.0"
        assert message_file.metadata["test"] is True
        assert message_file.last_updated is not None
    
    def test_message_file_validation(self, old_message):
        """Test message file validation with old messages."""
        # This should not raise an error, just log a warning
        message_file = MessageFile(messages=[old_message])
        assert len(message_file.messages) == 1
    
    def test_message_file_serialization(self, mock_message_file):
        """Test message file serialization."""
        serialized = mock_message_file.dict(by_alias=True)
        assert isinstance(serialized, dict)
        assert "messages" in serialized
        assert "last_updated" in serialized
        assert "version" in serialized


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_create_message_function(self):
        """Test create_message utility function."""
        content_data = {
            "test_type": "unit",
            "test_file": "tests/test_example.py",
            "parameters": {
                "environment": "development",
                "verbose": True
            }
        }
        
        message = create_message(
            sender="test_agent",
            message_type=MessageType.TEST_REQUEST,
            content=content_data
        )
        
        assert message.sender == "test_agent"
        assert message.type == MessageType.TEST_REQUEST
        assert isinstance(message.content, TestRequestContent)
    
    def test_validate_message_dict_function(self, sample_messages_data):
        """Test validate_message_dict utility function."""
        message_dict = sample_messages_data[0]
        message = validate_message_dict(message_dict)
        
        assert isinstance(message, AgentMessage)
        assert message.sender == message_dict["sender"]
        assert message.type == message_dict["type"]
    
    def test_validate_message_dict_invalid(self, invalid_message_data):
        """Test validate_message_dict with invalid data."""
        with pytest.raises(ValidationError):
            validate_message_dict(invalid_message_data)


class TestTestArtifacts:
    """Test artifact models."""
    
    def test_test_artifact_creation(self):
        """Test creating test artifacts."""
        artifact = TestArtifact(
            path="test_results/coverage.html",
            type="coverage",
            size_bytes=1024
        )
        
        assert artifact.path == "test_results/coverage.html"
        assert artifact.type == "coverage"
        assert artifact.size_bytes == 1024
        assert artifact.created_at is not None
    
    def test_test_artifact_invalid_path(self):
        """Test invalid artifact paths."""
        with pytest.raises(ValidationError):
            TestArtifact(
                path="invalid path with spaces",  # Invalid characters
                type="log"
            )


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_message_list(self):
        """Test message file with empty message list."""
        message_file = MessageFile(messages=[])
        assert len(message_file.messages) == 0
        assert message_file.version == "1.1.0"
    
    def test_large_message_content(self):
        """Test messages with large content."""
        large_content = TestRequestContent(
            test_type=TestType.UNIT,
            test_file="tests/large_test.py",
            parameters=TestParameters(
                environment=Environment.DEVELOPMENT,
                verbose=True
            )
        )
        
        # Add large metadata
        large_metadata = {"large_data": "x" * 10000}
        
        message = AgentMessage(
            sender="test_agent",
            type=MessageType.TEST_REQUEST,
            content=large_content,
            metadata=large_metadata
        )
        
        # Should still be valid
        assert message.sender == "test_agent"
        assert len(message.metadata["large_data"]) == 10000
    
    def test_unicode_content(self):
        """Test messages with Unicode content."""
        message = AgentMessage(
            sender="test_agent_unicode",
            type=MessageType.STATUS_UPDATE,
            content=StatusUpdateContent(
                agent_id="test_agent_unicode",
                state=AgentState.BUSY,
                progress=50.0,
                current_task="Processing 中文测试 data"
            )
        )
        
        assert "中文测试" in message.content.current_task