# Wealthsimple AI Builder — Demo Video Script
**Applicant:** Jason West  
**System:** Moto (West AI Labs)  
**Target Length:** 2:30–3:00  
**Format:** Screen recording + voiceover (or face-cam overlay)  
**Deadline:** March 2, 2026

---

## Hook Line (Opening Card or Spoken)

> **"Most AI demos show you a chatbot answering questions. This one shows you an AI that runs your life while you sleep."**

---

## Full Script

---

### [0:00 – 0:20] — THE HOOK
**Screen:** Black screen → terminal on `shurtugal-lnx` showing `uptime` and running processes. Clock visible — it's early morning.

**Narration (voiceover):**
> "It's 7 AM. I haven't touched my computer. But my AI agent already scraped LinkedIn for jobs, filed the results, and sent me a summary in Discord. This isn't a demo environment — this is my actual infrastructure, running 24/7 on bare metal Ubuntu. The agent is called Moto."

---

### [0:20 – 0:50] — THE PROBLEM
**Screen:** Split — left side shows a calendar packed with tasks; right side shows a Discord message from Moto with morning summary already delivered.

**Narration:**
> "I'm running a job search for two people, managing my own company, writing blog content, and building products — simultaneously. No team. For most people, that's impossible. The bottleneck isn't skill — it's bandwidth. You can only hold so many balls in the air before they start dropping. I needed something that could carry cognitive load, not just answer questions."

---

### [0:50 – 1:25] — THE SYSTEM IN ACTION
**Screen:** Discord chat — Jason types a single message to Moto: *"Research the top 5 fintech AI companies hiring right now and draft an outreach email."*

**Narration:**
> "Watch what happens when I ask Moto to do something that used to take me an hour. I send one message in Discord."

**Screen:** Moto's response appears immediately — it acknowledges the task and spawns a sub-agent. Show the sub-agent spinning up in the terminal (exec session log).

**Narration (continuing):**
> "Moto doesn't just start working on it — it *delegates* to a specialized sub-agent and stays available to talk to me. No waiting. No blocking. The research runs in the background while I keep working."

**Screen:** 15 seconds later — sub-agent result auto-announces back in Discord. Moto synthesizes it and delivers the outreach draft.

**Narration:**
> "Fifteen seconds. A full research brief and a drafted email — while I was having coffee."

---

### [1:25 – 1:55] — DEEPER CAPABILITY
**Screen:** Show the cron job list (`crontab -l`) — 7 AM pipeline entries visible. Then cut to `memory/MEMORY.md` briefly, then to the skills directory.

**Narration:**
> "But this goes deeper than task delegation. Moto runs scheduled pipelines every morning — job scrapes, log reviews, content drafts — without being asked. It has persistent memory across sessions, so it knows my goals, my preferences, my infrastructure. And here's what I think is genuinely novel: it teaches itself. Today it built five new skills and updated its own instruction files. It's not static."

---

### [1:55 – 2:25] — THE CAPABILITY UNLOCK
**Screen:** Show the Mac Mini terminal — `ollama` or MLX running Qwen2.5-32B locally. Then flip back to Discord — show a blog post publish confirmation from Moto. Then show the live blog post in a browser.

**Narration:**
> "There's a local LLM running on my Mac Mini — Qwen 2.5, 32 billion parameters — zero API cost for heavy inference. Moto uses it for the deep lifts. End result: I went from writing and publishing blog posts manually — two hours each — to saying 'write a post about AI infrastructure trends' and seeing it live on my site. The human part of my job shifted from *doing* to *directing*."

---

### [2:25 – 2:50] — THE CLOSE
**Screen:** Back to the Discord interface — a calm, clean conversation thread. Maybe show a simple `uptime` or system status. End on the terminal.

**Narration:**
> "Wealthsimple wants AI that meaningfully expands what a human can do. Moto isn't a productivity tool. It's an AI infrastructure engineer that handles operational reality — not toy demos. It runs job pipelines, publishes content, manages services, and delegates intelligently — while I stay in the loop without being in the weeds. That's the system. I'm Jason West, and I'd like to build the next version of this at Wealthsimple."

---

### [2:50 – 3:00] — TITLE CARD
**Screen:** Clean black card.  
**Text:** `Moto — West AI Labs` / `Jason West` / `westal.com` or contact

---

## Screen Direction Summary

| Timestamp | What's On Screen |
|-----------|-----------------|
| 0:00–0:20 | Terminal: `uptime`, process list, system clock |
| 0:20–0:50 | Calendar (crowded) → Discord morning summary already delivered |
| 0:50–1:05 | Discord: Jason types message to Moto |
| 1:05–1:25 | Terminal: sub-agent spinning up → Discord: result delivered |
| 1:25–1:55 | `crontab -l` → `memory/MEMORY.md` → skills directory listing |
| 1:55–2:10 | Mac Mini terminal: local LLM running (Qwen2.5-32B) |
| 2:10–2:25 | Discord: blog post publish confirm → Browser: live post |
| 2:25–2:50 | Discord: calm conversation thread → terminal |
| 2:50–3:00 | Title card: name + contact |

---

## Production Notes

- **Voiceover tone:** Calm, confident, matter-of-fact. Not salesy. Let the system speak for itself.
- **No slide decks.** Real terminals, real Discord, real output only.
- **Speed up sub-agent wait time** in edit if it takes >20 seconds live — cut to result.
- **Font size:** Bump terminal font to 18–20pt before recording. Reviewers watch on laptop.
- **Music:** Optional low-key ambient under the demo section (0:50–2:25). Silence for open/close.
- **Discord:** Dark mode. Clean channel. No unrelated messages visible.
- **Total word count (narration):** ~230 words — fits comfortably in 2:30–2:45 at natural pace.

---

*Script version 1.0 — drafted 2026-02-23*
