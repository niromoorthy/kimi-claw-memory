# Robust Memory System Design

## Problem Statement
OpenClaw resets daily at 4:00 AM, wiping session context. Need a system that:
1. Survives resets without losing critical context
2. Automatically restores state at session start
3. Tracks conversation continuity
4. Backs up important data

## Proposed Architecture

### Option 1: Enhanced File-Based System (Recommended)
Build on existing memory files with automation:

```
memory/
├── MEMORY.md              # Curated long-term facts (manual)
├── 2026-02-17.md          # Daily conversation log (auto)
├── session-state.json     # Current session tracking (auto)
├── checkpoints/           # Periodic snapshots (auto)
│   ├── 2026-02-17-04-00.json
│   └── 2026-02-17-12-00.json
└── recovery/
    ├── last-known-state.json
    └── pending-tasks.json
```

**Components:**

1. **Session State Tracker** (script)
   - Runs every 5 minutes during active sessions
   - Saves: conversation summary, open tasks, key facts learned
   - Timestamped checkpoints

2. **Auto-Recovery Skill** 
   - Triggers at session start
   - Reads MEMORY.md + last checkpoint
   - Restores context automatically
   - Reports: "Recovered from 4:00 AM reset. Last conversation about X."

3. **Cron Backup Job**
   - Runs at 3:55 AM (before reset)
   - Creates final checkpoint
   - Logs session end reason

### Option 2: Supabase Integration
External database for redundancy:

**Pros:**
- Survives any local file corruption
- Queryable history
- Multi-device sync potential

**Cons:**
- Requires API keys and network
- Latency for reads/writes
- Additional dependency

**Schema:**
```sql
sessions (
  id, start_time, end_time, summary, 
  key_facts JSONB, open_tasks JSONB
)

memory_entries (
  id, timestamp, category, content, 
  importance, expires_at
)
```

### Option 3: Hybrid (Best of Both)
File-based primary + Supabase backup

## Recommendation: Option 1 (File-Based)

**Why:**
- No external dependencies
- Fast local reads
- Works offline
- Simple to debug
- User has full control

**Implementation:**

### 1. Create `memory-manager` Skill

```bash
# Initialize skill
python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/init_skill.py memory-manager --path /root/.openclaw/workspace/skills --resources scripts
```

### 2. Core Scripts

**scripts/auto-save.py**
- Runs via cron every 5 min during sessions
- Appends to daily file
- Creates checkpoint if significant changes

**scripts/session-recovery.py**  
- Runs at session start
- Reads MEMORY.md + latest checkpoint
- Generates recovery summary

**scripts/heartbeat-check.py**
- Runs every hour
- Detects if session died unexpectedly
- Creates recovery entry

### 3. Cron Jobs

```bash
# Every 5 minutes - auto-save
*/5 * * * * /root/.openclaw/workspace/skills/memory-manager/scripts/auto-save.py

# 3:55 AM - final backup before reset  
55 3 * * * /root/.openclaw/workspace/skills/memory-manager/scripts/final-backup.py

# 4:05 AM - post-reset recovery check
5 4 * * * /root/.openclaw/workspace/skills/memory-manager/scripts/post-reset-recovery.py
```

### 4. Session State Format

```json
{
  "session_id": "uuid",
  "started_at": "2026-02-17T04:05:00Z",
  "last_activity": "2026-02-17T04:35:00Z",
  "conversation_summary": "User asked about memory reset...",
  "key_facts_learned": [
    "User lives in Melbourne",
    "Wants robust memory system"
  ],
  "open_tasks": [
    "Design memory system",
    "Install skill"
  ],
  "user_preferences": {
    "location": "Melbourne",
    "timezone": "AEST"
  }
}
```

## Questions for You

1. **Supabase:** Do you want external backup or file-only?
2. **Frequency:** How often should auto-save run? (5 min? 1 min?)
3. **Privacy:** Any data you DON'T want logged?
4. **Alerts:** Should I notify you when I recover from a reset?

## Next Steps

1. Confirm approach (file-only vs hybrid)
2. I'll build the memory-manager skill
3. Install and test
4. Monitor for a few days

What's your preference?