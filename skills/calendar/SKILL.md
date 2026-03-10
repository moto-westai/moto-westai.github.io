---
name: calendar
description: Calendar and scheduling management. Use when the user asks about upcoming events, scheduling meetings, tracking deadlines, time management, or availability. Covers viewing schedules, creating events, reminders, and time blocking.
---

# Calendar & Scheduling

## Environment

- User timezone: **America/Chicago (CST/CDT)**
- All times displayed in Central unless stated otherwise
- Reminders via OpenClaw `cron` tool
- Calendar data stored in workspace files when no external calendar is connected

## Viewing Events

Check upcoming events and availability:

- Review `calendar/` workspace files for tracked events
- When external calendar (Google, Outlook) is connected, query via available integrations
- Default view: today + next 7 days
- Always convert UTC timestamps to America/Chicago before displaying

## Creating & Modifying Events

When the user wants to schedule something:

1. Confirm: **what**, **when** (date + time + timezone), **where** (if applicable), **who** (attendees)
2. If time is ambiguous, assume America/Chicago
3. Create/update the event via available calendar integration
4. Set a reminder if requested (see below)

### Event Format (Workspace Tracking)

When logging events locally in `calendar/events.md`:

```markdown
## 2026-02-11

- **09:00** — Standup (daily, 15 min)
- **13:00–14:00** — Client sync: Acme Corp (Zoom)
- **16:00** — Deadline: proposal submission
```

## Reminders via Cron

Use OpenClaw cron to set reminders:

```
openclaw cron add --at "2026-02-11T08:45:00-06:00" --message "Standup in 15 minutes"
openclaw cron add --at "2026-02-11T12:30:00-06:00" --message "Client sync with Acme Corp in 30 min — prep notes ready?"
```

- Default lead time: **15 minutes** before meetings, **1 hour** before deadlines
- For recurring reminders, use cron expressions
- Deliver reminders to the user's active channel

## Time Blocking

Strategies for focused work:

1. **Deep work blocks** — 2–3 hour uninterrupted slots, morning preferred
2. **Admin blocks** — 30–60 min for email, invoicing, scheduling
3. **Buffer blocks** — 15 min between meetings for context switching
4. **No-meeting zones** — protect at least one half-day per week

When the user asks to plan their day/week, suggest a time-blocked layout respecting existing commitments.

## Meeting Prep Checklist

Before important meetings, offer to prepare:

- [ ] Agenda / talking points
- [ ] Relevant docs or links gathered
- [ ] Previous meeting notes reviewed
- [ ] Questions to raise listed
- [ ] Calendar reminder set (15 min before)

## Timezone Handling

- Store all times internally as ISO 8601 with offset (`-06:00` CST, `-05:00` CDT)
- When someone gives a time in another timezone, convert and confirm: _"That's 3 PM ET — 2 PM your time (Central). Sound right?"_
- Common conversions from Central:
  - ET = Central + 1h
  - PT = Central − 2h
  - UTC = Central + 6h (CST) or + 5h (CDT)

## Guidelines

- Always confirm date/time before creating events
- Default to America/Chicago if no timezone specified
- When declining or rescheduling, suggest alternatives
- Keep calendar files tidy — archive past months to `calendar/archive/`
