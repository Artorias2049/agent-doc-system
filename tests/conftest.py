"""
Pytest configuration and fixtures for agent communication testing.
"""

import json
import pytest
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock
import uuid

# Import models for testing
import sys
sys.path.append(str(Path(__file__).parent.parent / "framework" / "agent_communication" / "core"))

from models import (
    AgentMessage, MessageFile, MessageType, MessageStatus,
    TestRequestContent, TestResultContent, StatusUpdateContent,
    WorkflowRequestContent, ValidationRequestContent, DocumentationUpdateContent,
    TestParameters, Environment, TestType, AgentState, ValidationLevel
)
from enhanced_protocol import EnhancedAgentProtocol


@pytest.fixture
def temp_root_dir():
    """Create a temporary directory structure for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root_path = Path(temp_dir)
        
        # Create directory structure
        (root_path / ".claude" / "config").mkdir(parents=True)
        (root_path / "framework" / "agent_communication" / "history").mkdir(parents=True)
        (root_path / "framework" / "schemas").mkdir(parents=True)
        
        # Create minimal config files
        config_data = {
            "agent_communication": {
                "cleanup_policy": {"default_retention_days": 7},
                "validation": {"strict_mode": True, "auto_validate_on_send": True}
            }
        }
        
        with open(root_path / ".claude" / "config" / "agent_settings.json", "w") as f:
            json.dump(config_data, f)
        
        yield root_path


@pytest.fixture
def sample_agent_protocol(temp_root_dir):
    """Create an EnhancedAgentProtocol instance for testing."""
    return EnhancedAgentProtocol(
        agent_id="test_agent_001",
        root_dir=str(temp_root_dir),
        environment="development"
    )


@pytest.fixture
def sample_test_request_content():
    """Sample test request content."""
    return TestRequestContent(
        test_type=TestType.UNIT,
        test_file="tests/test_example.py",
        parameters=TestParameters(
            environment=Environment.DEVELOPMENT,
            verbose=True,
            timeout_seconds=300,
            coverage=True
        )
    )


@pytest.fixture
def sample_test_result_content():
    """Sample test result content."""
    return TestResultContent(
        test_id=uuid.uuid4(),
        status="passed",
        logs=["Test started", "All tests passed"],
        artifacts=[],
        execution_time_seconds=15.5,
        coverage_percentage=85.0
    )


@pytest.fixture
def sample_workflow_content():
    """Sample workflow request content."""
    from models import WorkflowStep
    
    return WorkflowRequestContent(
        workflow_name="validate_and_test",
        steps=[
            WorkflowStep(
                name="validate_schemas",
                action="validate",
                parameters={"target": "schemas/*.yml"},
                timeout_seconds=60
            ),
            WorkflowStep(
                name="run_tests",
                action="test",
                parameters={"coverage": True},
                depends_on=["validate_schemas"]
            )
        ],
        parameters={"environment": "development"},
        parallel_execution=False
    )


@pytest.fixture
def sample_validation_content():
    """Sample validation request content."""
    return ValidationRequestContent(
        validation_type="schema",
        target_files=["framework/schemas/*.yml"],
        validation_level=ValidationLevel.ENHANCED,
        auto_fix=False,
        generate_report=True
    )


@pytest.fixture
def sample_status_update_content():
    """Sample status update content."""
    return StatusUpdateContent(
        agent_id="test_agent_001",
        state=AgentState.BUSY,
        progress=75.0,
        current_task="Running tests",
        estimated_completion=datetime.utcnow() + timedelta(minutes=5)
    )


@pytest.fixture
def sample_messages_data():
    """Sample message data for testing."""
    return [
        {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow(),
            "sender": "test_agent_001",
            "type": MessageType.TEST_REQUEST,
            "content": {
                "test_type": "unit",
                "test_file": "tests/test_example.py",
                "parameters": {
                    "environment": "development",
                    "verbose": True
                }
            },
            "status": MessageStatus.PENDING
        },
        {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow() - timedelta(hours=1),
            "sender": "test_agent_002",
            "type": MessageType.STATUS_UPDATE,
            "content": {
                "agent_id": "test_agent_002",
                "state": "idle",
                "progress": 100.0
            },
            "status": MessageStatus.PROCESSED
        }
    ]


@pytest.fixture
def mock_message_file(sample_messages_data):
    """Mock message file data."""
    messages = [AgentMessage(**msg_data) for msg_data in sample_messages_data]
    return MessageFile(
        messages=messages,
        version="1.1.0",
        metadata={"test": True}
    )


@pytest.fixture
def old_message():
    """Create an old processed message for cleanup testing."""
    return AgentMessage(
        id=uuid.uuid4(),
        timestamp=datetime.utcnow() - timedelta(days=10),
        sender="old_agent",
        type=MessageType.STATUS_UPDATE,
        content=StatusUpdateContent(
            agent_id="old_agent",
            state=AgentState.IDLE,
            progress=100.0
        ),
        status=MessageStatus.PROCESSED
    )


@pytest.fixture
def recent_message():
    """Create a recent message that should not be cleaned up."""
    return AgentMessage(
        id=uuid.uuid4(),
        timestamp=datetime.utcnow() - timedelta(hours=1),
        sender="recent_agent",
        type=MessageType.STATUS_UPDATE,
        content=StatusUpdateContent(
            agent_id="recent_agent",
            state=AgentState.BUSY,
            progress=50.0
        ),
        status=MessageStatus.PENDING
    )


@pytest.fixture
def invalid_message_data():
    """Invalid message data for validation testing."""
    return {
        "id": "invalid-uuid",  # Invalid UUID
        "timestamp": "invalid-timestamp",  # Invalid timestamp
        "sender": "",  # Empty sender
        "type": "invalid_type",  # Invalid message type
        "content": {},  # Empty content
        "status": "invalid_status"  # Invalid status
    }


class MockDatetime:
    """Mock datetime for consistent testing."""
    
    @staticmethod
    def utcnow():
        return datetime(2024, 12, 29, 12, 0, 0)


@pytest.fixture
def freeze_time(monkeypatch):
    """Freeze time for consistent testing."""
    monkeypatch.setattr("framework.agent_communication.core.models.datetime", MockDatetime)
    monkeypatch.setattr("framework.agent_communication.core.enhanced_protocol.datetime", MockDatetime)


# Helper functions for tests

def create_test_message(message_type: MessageType, content_data: Dict[str, Any]) -> AgentMessage:
    """Helper to create test messages."""
    return AgentMessage(
        sender="test_agent",
        type=message_type,
        content=content_data,
        status=MessageStatus.PENDING
    )


def assert_message_valid(message: AgentMessage):
    """Helper to assert message is valid."""
    assert message.id is not None
    assert message.timestamp is not None
    assert message.sender is not None
    assert message.type is not None
    assert message.content is not None
    assert message.status is not None


def create_temp_message_file(temp_dir: Path, messages: List[AgentMessage]) -> Path:
    """Helper to create temporary message files."""
    message_file = MessageFile(messages=messages)
    file_path = temp_dir / "test_messages.json"
    
    with open(file_path, "w") as f:
        json.dump(message_file.dict(by_alias=True), f, indent=2, default=str)
    
    return file_path