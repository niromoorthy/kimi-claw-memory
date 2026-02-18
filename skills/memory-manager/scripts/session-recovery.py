#!/usr/bin/env python3
"""
Session recovery script for memory-manager skill.
Runs at session start to restore context after reset.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def get_memory_dir():
    """Get the memory directory path."""
    return Path("/root/.openclaw/workspace/memory")

def read_memory_md():
    """Read critical facts from MEMORY.md."""
    memory_file = get_memory_dir() / "MEMORY.md"
    if not memory_file.exists():
        return "No MEMORY.md found"
    
    try:
        return memory_file.read_text()
    except Exception as e:
        return f"Error reading MEMORY.md: {e}"

def find_latest_checkpoint():
    """Find the most recent checkpoint file."""
    checkpoints_dir = get_memory_dir() / "checkpoints"
    if not checkpoints_dir.exists():
        return None
    
    checkpoints = list(checkpoints_dir.glob("*.json"))
    if not checkpoints:
        return None
    
    return max(checkpoints, key=lambda p: p.stat().st_mtime)

def read_recovery_file():
    """Read emergency recovery file."""
    recovery_file = get_memory_dir() / "recovery" / "last-session.json"
    if not recovery_file.exists():
        return None
    
    try:
        with open(recovery_file, 'r') as f:
            return json.load(f)
    except Exception:
        return None

def generate_recovery_report(memory_md, checkpoint_data):
    """Generate human-readable recovery report."""
    report = []
    
    # Check if this is a post-reset recovery
    now = datetime.now()
    if now.hour == 4 and now.minute < 10:
        report.append("Session recovered from 4:00 AM reset.")
    else:
        report.append("Session started. Loading memory...")
    
    # Add checkpoint info
    if checkpoint_data:
        last_time = checkpoint_data.get('timestamp', 'unknown')
        report.append(f"Last checkpoint: {last_time}")
        
        if checkpoint_data.get('summary'):
            report.append(f"Previous context: {checkpoint_data['summary']}")
        
        if checkpoint_data.get('key_facts'):
            facts = ', '.join(checkpoint_data['key_facts'])
            report.append(f"Key facts: {facts}")
        
        if checkpoint_data.get('open_tasks'):
            tasks = ', '.join(checkpoint_data['open_tasks'])
            report.append(f"Pending tasks: {tasks}")
    else:
        report.append("No previous checkpoint found.")
    
    return '\n'.join(report)

def main():
    """Main recovery function."""
    memory_dir = get_memory_dir()
    
    # Ensure directories exist
    for subdir in ["daily", "checkpoints", "recovery", "archive"]:
        (memory_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # Read sources
    memory_md = read_memory_md()
    
    # Try checkpoint first, then recovery file
    checkpoint_file = find_latest_checkpoint()
    checkpoint_data = None
    
    if checkpoint_file:
        try:
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
        except Exception:
            pass
    
    if not checkpoint_data:
        checkpoint_data = read_recovery_file()
    
    # Generate report
    report = generate_recovery_report(memory_md, checkpoint_data)
    
    # Output for OpenClaw to read
    print("=== MEMORY RECOVERY REPORT ===")
    print(report)
    print("=== END REPORT ===")
    
    # Also save to recovery log
    recovery_log = memory_dir / "recovery" / "recovery-log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(recovery_log, 'a') as f:
        f.write(f"\n## Recovery {now}\n")
        f.write(report)
        f.write("\n\n")

if __name__ == "__main__":
    main()
