#!/usr/bin/env python3
"""
Pydantic models for agent communication with type safety and validation.
Replaces JSON schema validation with faster, more comprehensive Python-native validation.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator


class MessageStatus(str, Enum):
    """Message processing status."""
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"


class MessageType(str, Enum):
    """Supported message types."""
    TEST_REQUEST = "test_request"
    TEST_RESULT = "test_result"
    STATUS_UPDATE = "status_update"
    CONTEXT_UPDATE = "context_update"
    WORKFLOW_REQUEST = "workflow_request"
    VALIDATION_REQUEST = "validation_request"
    DOCUMENTATION_UPDATE = "documentation_update"


class TestType(str, Enum):
    """Test execution types."""
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"


class Environment(str, Enum):
    """Execution environments."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class TestResult(str, Enum):
    """Test execution results."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


class AgentState(str, Enum):
    """Agent operational states."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class ContextUpdateType(str, Enum):
    """Context modification types."""
    ADD = "add"
    UPDATE = "update"
    REMOVE = "remove"


class ValidationLevel(str, Enum):
    """Validation strictness levels."""
    BASIC = "basic"
    ENHANCED = "enhanced"
    STRICT = "strict"


class ArtifactType(str, Enum):
    """Test artifact types."""
    LOG = "log"
    REPORT = "report"
    COVERAGE = "coverage"
    SCREENSHOT = "screenshot"


# Content Models for Different Message Types

class TestParameters(BaseModel):
    """Parameters for test execution."""
    environment: Environment
    verbose: bool = False
    timeout_seconds: Optional[int] = Field(None, ge=1, le=3600)
    parallel: bool = False
    coverage: bool = False


class TestRequestContent(BaseModel):
    """Content for test_request messages."""
    test_type: TestType
    test_file: str = Field(..., pattern=r"^[a-zA-Z0-9/._-]+$")
    parameters: TestParameters
    
    @field_validator('test_file')
    @classmethod
    def validate_test_file_extension(cls, v):
        """Ensure test file has appropriate extension."""
        if not v.endswith(('.py', '.js', '.ts', '.java', '.go')):
            raise ValueError('Test file must have a valid test file extension')
        return v


class TestArtifact(BaseModel):
    """Test execution artifact."""
    path: str = Field(..., pattern=r"^[a-zA-Z0-9/._-]+$")
    type: ArtifactType
    size_bytes: Optional[int] = Field(None, ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TestResultContent(BaseModel):
    """Content for test_result messages."""
    test_id: UUID
    status: TestResult
    logs: List[str] = Field(default_factory=list)
    artifacts: List[TestArtifact] = Field(default_factory=list)
    execution_time_seconds: Optional[float] = Field(None, ge=0)
    coverage_percentage: Optional[float] = Field(None, ge=0, le=100)


class StatusUpdateContent(BaseModel):
    """Content for status_update messages."""
    agent_id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    state: AgentState
    progress: float = Field(..., ge=0, le=100)
    current_task: Optional[str] = None
    estimated_completion: Optional[datetime] = None


class ContextUpdateContent(BaseModel):
    """Content for context_update messages."""
    context_id: UUID
    type: ContextUpdateType
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class WorkflowStep(BaseModel):
    """Individual workflow step definition."""
    name: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = Field(300, ge=1, le=3600)
    retry_count: int = Field(0, ge=0, le=5)
    depends_on: List[str] = Field(default_factory=list)


class WorkflowRequestContent(BaseModel):
    """Content for workflow_request messages."""
    workflow_name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    steps: List[WorkflowStep]
    parameters: Dict[str, Any] = Field(default_factory=dict)
    parallel_execution: bool = False
    failure_strategy: str = Field("abort", pattern=r"^(abort|continue|retry)$")


class ValidationRequestContent(BaseModel):
    """Content for validation_request messages."""
    validation_type: str = Field(..., pattern=r"^(schema|documentation|messages|project)$")
    target_files: List[str] = Field(..., min_items=1)
    validation_level: ValidationLevel = ValidationLevel.ENHANCED
    auto_fix: bool = False
    generate_report: bool = True


class DocumentationUpdateContent(BaseModel):
    """Content for documentation_update messages."""
    update_type: str = Field(..., pattern=r"^(create|update|delete|sync)$")
    target_documents: List[str] = Field(..., min_items=1)
    template_name: Optional[str] = None
    metadata_updates: Optional[Dict[str, Any]] = None
    auto_generate: bool = False


# Main Message Model

class AgentMessage(BaseModel):
    """Main agent message model with comprehensive validation."""
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0))
    sender: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    type: MessageType
    content: Union[
        TestRequestContent,
        TestResultContent,
        StatusUpdateContent,
        ContextUpdateContent,
        WorkflowRequestContent,
        ValidationRequestContent,
        DocumentationUpdateContent
    ]
    status: MessageStatus = MessageStatus.PENDING
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @model_validator(mode='before')
    @classmethod
    def validate_content_type(cls, values):
        """Ensure content matches message type and convert dicts to proper models."""
        msg_type = values.get('type')
        content = values.get('content')
        
        type_mapping = {
            MessageType.TEST_REQUEST: TestRequestContent,
            MessageType.TEST_RESULT: TestResultContent,
            MessageType.STATUS_UPDATE: StatusUpdateContent,
            MessageType.CONTEXT_UPDATE: ContextUpdateContent,
            MessageType.WORKFLOW_REQUEST: WorkflowRequestContent,
            MessageType.VALIDATION_REQUEST: ValidationRequestContent,
            MessageType.DOCUMENTATION_UPDATE: DocumentationUpdateContent,
        }
        
        if msg_type and content:
            expected_type = type_mapping.get(msg_type)
            if expected_type:
                # If content is a dict, convert it to the proper model
                if isinstance(content, dict):
                    values['content'] = expected_type(**content)
                elif not isinstance(content, expected_type):
                    raise ValueError(f"Content type mismatch: expected {expected_type.__name__} for {msg_type}")
        
        return values
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True
        extra = "forbid"


class MessageFile(BaseModel):
    """Message file container model."""
    messages: List[AgentMessage] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0))
    version: str = Field("1.1.0", pattern=r"^\d+\.\d+\.\d+$")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    @field_validator('messages')
    @classmethod
    def validate_message_retention(cls, v):
        """Validate message retention policy."""
        current_time = datetime.now(timezone.utc)
        old_messages = []
        
        for msg in v:
            age_days = (current_time - msg.timestamp).days
            if age_days > 7 and msg.status == MessageStatus.PROCESSED:
                old_messages.append(msg.id)
        
        if old_messages:
            # This is a warning, not an error - cleanup should be handled separately
            pass
        
        return v
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "allow"


# Utility Functions

def create_message(
    sender: str,
    message_type: MessageType,
    content: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> AgentMessage:
    """Create a validated agent message."""
    # Map message type to content model
    content_models = {
        MessageType.TEST_REQUEST: TestRequestContent,
        MessageType.TEST_RESULT: TestResultContent,
        MessageType.STATUS_UPDATE: StatusUpdateContent,
        MessageType.CONTEXT_UPDATE: ContextUpdateContent,
        MessageType.WORKFLOW_REQUEST: WorkflowRequestContent,
        MessageType.VALIDATION_REQUEST: ValidationRequestContent,
        MessageType.DOCUMENTATION_UPDATE: DocumentationUpdateContent,
    }
    
    content_model = content_models[message_type]
    validated_content = content_model(**content)
    
    return AgentMessage(
        sender=sender,
        type=message_type,
        content=validated_content,
        metadata=metadata or {}
    )


def validate_message_dict(message_dict: Dict[str, Any]) -> AgentMessage:
    """Validate a message dictionary and return validated model."""
    return AgentMessage(**message_dict)


def serialize_message(message: AgentMessage) -> Dict[str, Any]:
    """Serialize message to dictionary for JSON storage."""
    from uuid import UUID
    
    data = message.dict(by_alias=True, exclude_none=True)
    
    # Convert UUID to string
    if isinstance(data.get('id'), UUID):
        data['id'] = str(data['id'])
    
    # Convert timestamp to schema-compliant format (YYYY-MM-DDTHH:MM:SSZ)
    if isinstance(data.get('timestamp'), datetime):
        data['timestamp'] = data['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')
    elif isinstance(data.get('timestamp'), str):
        # If already string, ensure Z format
        try:
            dt = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            data['timestamp'] = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            pass  # Leave as-is if parsing fails
    return data


def serialize_message_file(message_file: MessageFile) -> Dict[str, Any]:
    """Serialize message file to dictionary for JSON storage."""
    import json
    from uuid import UUID
    
    # Use Pydantic's JSON serialization with custom datetime handling
    data = json.loads(message_file.json(by_alias=True, exclude_none=True))
    
    # Fix timestamp formats to match schema (YYYY-MM-DDTHH:MM:SSZ)
    def fix_timestamp(ts_str):
        if isinstance(ts_str, str):
            try:
                # Parse various timestamp formats and convert to Z format
                if '+00:00' in ts_str:
                    dt = datetime.fromisoformat(ts_str)
                elif 'Z' in ts_str:
                    dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                else:
                    dt = datetime.fromisoformat(ts_str)
                return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                pass
        return ts_str
    
    # Fix message timestamps
    if 'messages' in data:
        for msg in data['messages']:
            if 'timestamp' in msg:
                msg['timestamp'] = fix_timestamp(msg['timestamp'])
    
    # Fix last_updated timestamp  
    if 'last_updated' in data:
        data['last_updated'] = fix_timestamp(data['last_updated'])
    
    return data