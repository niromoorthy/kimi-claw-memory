#!/usr/bin/env python3
"""
Auto-save script for memory-manager skill.
Runs every 5 minutes during active sessions.
Saves conversation state to daily file and checkpoint JSON.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

def get_memory_dir():
    """Get the memory directory path."""
    return Path("/root/.openclaw/workspace/memory")

def ensure_directories():
    """Create memory subdirectories if they don't exist."""
    memory_dir = get_memory_dir()
    for subdir in ["daily", "checkpoints", "recovery", "archive"]:
        (memory_dir / subdir).mkdir(parents=True, exist_ok=True)

def get_session_file():
    """Get current session transcript path."""
    # Look for most recent session file
    workspace = Path("/root/.openclaw/workspace")
    sessions = list(workspace.glob("*.jsonl"))
    if not sessions:
        return None
    # Get most recently modified
    return max(sessions, key=lambda p: p.stat().st_mtime)

def extract_conversation_summary(session_file):
    """Extract last few messages from session for summary."""
    if not session_file or not session_file.exists():
        return "No active session found"
    
    try:
        with open(session_file, 'r') as f:
            lines = f.readlines()
        
        # Get last 10 lines for context
        recent = lines[-10:] if len(lines) > 10 else lines
        return f"Session has {len(lines)} messages"
    except Exception as e:
        return f"Error reading session: {e}"

def save_daily_file(date_str, data):
    """Append to daily markdown file."""
    memory_dir = get_memory_dir()
    daily_file = memory_dir / "daily" / f"{date_str}.md"
    
    # Create header if new file
    if not daily_file.exists():
        daily_file.write_text(f"# {date_str}\n\n## Session Log\n\n")
    
    # Append checkpoint entry
    timestamp = data['timestamp']
    with open(daily_file, 'a') as f:
        f.write(f"\n### Checkpoint {timestamp}\n")
        f.write(f"- Summary: {data['summary']}\n")
        f.write(f"- Key facts: {', '.join(data['key_facts'])}\n")
        f.write(f"- Open tasks: {', '.join(data['open_tasks'])}\n")

def save_checkpoint_json(date_str, data):
    """Save machine-readable checkpoint."""
    memory_dir = get_memory_dir()
    checkpoint_file = memory_dir / "checkpoints" / f"{date_str}-{data['timestamp']}.json"
    
    with open(checkpoint_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Also save as "latest" for quick recovery
    latest_file = memory_dir / "recovery" / "last-session.json"
    with open(latest_file, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    """Main auto-save function."""
    ensure_directories()
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M")
    
    # Get session info
    session_file = get_session_file()
    summary = extract_conversation_summary(session_file)
    
    # Build checkpoint data
    # TODO: In real implementation, this would parse actual conversation
    data = {
        "timestamp": time_str,
        "date": date_str,
        "summary": summary,
        "key_facts": [],  # Would extract from conversation
        "open_tasks": [],  # Would track pending items
        "session_file": str(session_file) if session_file else None
    }
    
    # Save to both formats
    save_daily_file(date_str, data)
    save_checkpoint_json(date_str, data)
    
    print(f"Checkpoint saved: {date_str} {time_str}")

if __name__ == "__main__":
    main()
