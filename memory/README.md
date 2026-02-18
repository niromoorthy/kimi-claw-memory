# Memory System

## Structure

- `memory/YYYY-MM-DD.md` — Daily conversation logs and events
- `MEMORY.md` — Curated long-term facts, preferences, active projects
- `memory/heartbeat-state.json` — Periodic check tracking

## Rules

1. **End of every session:** Append summary to today's daily file
2. **Key facts learned:** Update MEMORY.md immediately
3. **Session start:** Read last 3 days + MEMORY.md
4. **Projects/URLs:** Always document in MEMORY.md under Active Projects

## Daily File Template

```markdown
# 2026-02-17

## Summary
Brief overview of what happened today.

## Key Facts
- Learned: [fact worth remembering]
- Decided: [decision made]
- Created: [files/projects]

## Links/References
- [url] — [what it's for]

## Open Items
- [ ] Things to follow up on
```
