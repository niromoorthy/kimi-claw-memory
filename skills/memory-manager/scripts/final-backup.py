#!/usr/bin/env python3
"""
Final backup script for memory-manager skill.
Runs at 3:55 AM before daily reset.
Creates final checkpoint and end-of-day summary.
"""

import json
from datetime import datetime
from pathlib import Path

def get_memory_dir():
    return Path("/root/.openclaw/workspace/memory")

def main():
    """Create final backup before reset."""
    memory_dir = get_memory_dir()
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M")
    
    # Create final checkpoint
    data = {
        "timestamp": time_str,
        "date": date_str,
        "type": "final-backup",
        "summary": "End of day - pre-reset backup",
        "key_facts": [],
        "open_tasks": [],
        "note": "Session will reset at 4:00 AM"
    }
    
    # Save final checkpoint
    checkpoint_file = memory_dir / "checkpoints" / f"{date_str}-{time_str}-final.json"
    with open(checkpoint_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Update recovery file
    recovery_file = memory_dir / "recovery" / "last-session.json"
    with open(recovery_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Log the backup
    recovery_log = memory_dir / "recovery" / "recovery-log.md"
    with open(recovery_log, 'a') as f:
        f.write(f"\n## Final Backup {date_str} {time_str}\n")
        f.write("Pre-reset checkpoint created.\n")
    
    print(f"Final backup created: {date_str} {time_str}")

if __name__ == "__main__":
    main()
