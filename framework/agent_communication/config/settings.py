#!/usr/bin/env python3

from pathlib import Path
import os

# Base directory for agent communication
BASE_DIR = Path(__file__).parent.parent.parent

# Communication settings
MESSAGE_RETENTION_DAYS = 7
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB
SUPPORTED_MESSAGE_TYPES = [
    "test_request",
    "test_result",
    "status_update",
    "context_update"
]

# Message status options
MESSAGE_STATUS = {
    "PENDING": "pending",
    "PROCESSED": "processed",
    "FAILED": "failed"
}

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# File paths
HISTORY_DIR = os.path.join(BASE_DIR, "agent_communication", "history")
CONFIG_DIR = os.path.join(BASE_DIR, "agent_communication", "config") 