#!/bin/bash
# Direct execution script for chat export
cd "$(dirname "$0")/../.."
python3 .claude/scripts/slash_command_handler.py "/chat:export"