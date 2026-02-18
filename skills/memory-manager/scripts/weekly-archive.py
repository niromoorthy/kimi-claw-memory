#!/usr/bin/env python3
"""
Weekly archive script for memory-manager skill.
Runs Sundays at midnight.
Archives old daily files and updates MEMORY.md.
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

def get_memory_dir():
    return Path("/root/.openclaw/workspace/memory")

def get_week_number(date_str):
    """Get ISO week number from date string."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.isocalendar()[1]

def archive_daily_files():
    """Archive daily files older than 7 days into weekly summary."""
    memory_dir = get_memory_dir()
    daily_dir = memory_dir / "daily"
    archive_dir = memory_dir / "archive"
    archive_dir.mkdir(exist_ok=True)
    
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    # Group old files by week
    weekly_data = {}
    
    for daily_file in daily_dir.glob("*.md"):
        # Extract date from filename
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', daily_file.name)
        if not date_match:
            continue
        
        date_str = date_match.group(1)
        file_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Skip if less than 7 days old
        if file_date > week_ago:
            continue
        
        # Get week number
        week_num = get_week_number(date_str)
        year = file_date.year
        week_key = f"{year}-week-{week_num:02d}"
        
        if week_key not in weekly_data:
            weekly_data[week_key] = []
        
        # Read and add to weekly summary
        try:
            content = daily_file.read_text()
            weekly_data[week_key].append({
                'date': date_str,
                'content': content
            })
        except Exception:
            pass
    
    # Create weekly archive files
    for week_key, days in weekly_data.items():
        archive_file = archive_dir / f"{week_key}.md"
        
        with open(archive_file, 'w') as f:
            f.write(f"# Weekly Archive: {week_key}\n\n")
            
            for day in sorted(days, key=lambda x: x['date']):
                f.write(f"\n## {day['date']}\n")
                # Extract just the summary, not full content
                lines = day['content'].split('\n')
                for line in lines[:20]:  # First 20 lines
                    f.write(line + '\n')
                f.write('\n...\n')

def cleanup_old_checkpoints():
    """Remove checkpoint files older than 30 days."""
    memory_dir = get_memory_dir()
    checkpoints_dir = memory_dir / "checkpoints"
    
    if not checkpoints_dir.exists():
        return
    
    now = datetime.now()
    thirty_days_ago = now - timedelta(days=30)
    
    for checkpoint in checkpoints_dir.glob("*.json"):
        # Extract date from filename (format: YYYY-MM-DD-HH-MM.json)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', checkpoint.name)
        if not date_match:
            continue
        
        date_str = date_match.group(1)
        file_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        if file_date < thirty_days_ago:
            checkpoint.unlink()
            print(f"Removed old checkpoint: {checkpoint.name}")

def main():
    """Main archive function."""
    print("Starting weekly archive...")
    
    archive_daily_files()
    cleanup_old_checkpoints()
    
    print("Weekly archive complete.")

if __name__ == "__main__":
    main()
