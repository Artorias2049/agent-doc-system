#!/bin/bash
# Test script for slash commands

echo "🧪 Testing Claude Code slash commands..."

HANDLER="$(dirname "$0")/slash_command_handler.py"

echo ""
echo "1. Testing help command:"
python3 "$HANDLER" "/help"

echo ""
echo "2. Testing agent:read command:"
python3 "$HANDLER" "/agent:read"

echo ""
echo "3. Testing chat:history command:"
python3 "$HANDLER" "/chat:history"

echo ""
echo "✅ Slash command tests completed!"
