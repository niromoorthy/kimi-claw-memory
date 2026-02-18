---
name: memory-manager
description: Robust memory management system for OpenClaw that survives daily resets. Automatically saves session state, creates checkpoints, and recovers context after 4 AM reset. Use when session starts to restore context, during conversations to save state, or when recovering from unexpected interruptions.
---

# Memory Manager

## Overview

This skill provides automatic memory persistence across OpenClaw's daily 4 AM reset. It saves conversation state every 5 minutes, creates pre-reset backups, and automatically restores context when a new session starts.

## Architecture

```
memory/
├── MEMORY.md                    # Critical long-term facts (always loaded)
├── daily/
│   └── 2026-02-17.md           # Conversation logs by day
├── checkpoints/
│   └── 2026-02-17-04-00.json   # Machine-readable state snapshots
├── recovery/
│   └── last-session.json       # Emergency recovery file
└── archive/
    └── 2026-week-07.md         # Weekly summaries (auto-generated)
```

## When to Use

### At Session Start (Automatic)
The skill auto-triggers when OpenClaw starts. It will:
1. Check if this is a post-reset session
2. Load MEMORY.md
3. Find and load latest checkpoint
4. Generate recovery summary

### During Active Sessions
Auto-saves every 5 minutes via cron. No manual action needed.

### Manual Save
If you want to force a checkpoint:
```bash
python3 /root/.openclaw/workspace/skills/memory-manager/scripts/auto-save.py --force
```

## Scripts

### auto-save.py
Runs every 5 minutes. Saves:
- Conversation summary
- Key facts learned
- Open tasks
- User preferences

### session-recovery.py
Runs at session start. Restores:
- Last known conversation context
- Pending tasks
- Critical user facts

### final-backup.py
Runs at 3:55 AM (before reset). Creates:
- Final checkpoint of day
- Session end summary
- Recovery metadata

### weekly-archive.py
Runs Sundays at midnight. Archives:
- Old daily files to weekly summary
- Updates MEMORY.md with persistent facts
- Cleans up checkpoints older than 30 days

## Recovery Report Format

When recovering from reset, you'll see:

> *"Session recovered from 4:00 AM reset. Last conversation was at 3:47 AM. You asked me to [summary]. You mentioned [key facts]. Pending: [open tasks]."*

## Redundancy

- **Dual storage**: Every save writes to both Markdown and JSON
- **Time-based backups**: Checkpoints every 5 min + final 3:55 AM backup
- **Cross-validation**: Recovery compares multiple sources
- **Emergency recovery**: Last-resort file if all else fails

## Cron Jobs

```bash
# Auto-save every 5 minutes
*/5 * * * * /root/.openclaw/workspace/skills/memory-manager/scripts/auto-save.py

# Final backup before reset
55 3 * * * /root/.openclaw/workspace/skills/memory-manager/scripts/final-backup.py

# Post-reset recovery
5 4 * * * /root/.openclaw/workspace/skills/memory-manager/scripts/session-recovery.py

# Weekly archive (Sundays at midnight)
0 0 * * 0 /root/.openclaw/workspace/skills/memory-manager/scripts/weekly-archive.py
```
