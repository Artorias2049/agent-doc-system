#!/usr/bin/env python3

from pathlib import Path
import os

# Base directory for agent communication
BASE_DIR = Path(__file__).parent.parent.parent

# Communication settings
MESSAGE_RETENTION_DAYS = 7
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB
SUPPORTED_MESSAGE_TYPES = [
    "request",
    "response",
    "notification",
    "error",
    "status_update"
]

# Message status options
MESSAGE_STATUS = {
    "PENDING": "pending",
    "IN_PROGRESS": "in_progress",
    "COMPLETED": "completed",
    "FAILED": "failed"
}

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# File paths
HISTORY_DIR = os.path.join(BASE_DIR, "agent_communication", "history")
CONFIG_DIR = os.path.join(BASE_DIR, "agent_communication", "config") 