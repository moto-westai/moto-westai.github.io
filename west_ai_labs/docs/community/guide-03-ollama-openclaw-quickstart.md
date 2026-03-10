# Guide 03: Ollama + OpenClaw Quickstart

> **Series:** Gaming PC → AI Agent Setup | West AI Labs Community
> **Level:** Beginner — you've done the Ubuntu/Ollama setup from Guide 02

---

## What We're Building

By the end of this guide, you'll have:
- OpenClaw installed and running
- An AI agent connected to your Ollama models
- A working agent you can actually talk to

Think of **Ollama** as the engine — it runs the AI model on your GPU. **OpenClaw** is everything around the engine: memory, personality, Discord integration, tools, and the ability to actually *be* an agent instead of just a chatbot.

---

## Step 1: Install Node.js

OpenClaw runs on Node.js (a JavaScript runtime). If you did the Ubuntu setup in Guide 02, you probably don't have it yet.

```bash
# Install Node Version Manager (nvm) — the best way to manage Node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Reload your shell config
source ~/.bashrc

# Install Node 20 (LTS)
nvm install 20
nvm use 20
nvm alias default 20

# Verify
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

---

## Step 2: Install OpenClaw

```bash
npm install -g openclaw
```

That's it. OpenClaw is now a global command on your system.

Verify:
```bash
openclaw --version
```

---

## Step 3: First Run — Initialize Your Workspace

OpenClaw needs a home directory. Run this to set it up:

```bash
openclaw init
```

This creates `~/.openclaw/workspace/` — the folder where your agent's memory, personality files, and configuration live. We'll explore this more in Guide 05.

You'll be prompted for a few things:
- **Workspace name:** Give your agent setup a name (e.g., "home", "gaming-rig")
- **Default model:** We'll set this up next

---

## Step 4: Connect OpenClaw to Ollama

Ollama runs a local API server on your machine. OpenClaw needs to know how to reach it.

```bash
openclaw config set model.provider ollama
openclaw config set model.baseUrl http://localhost:11434
```

Now tell it which model to use by default. Use one you've already pulled (from Guide 02):

```bash
# If you pulled llama3.1:
openclaw config set model.default llama3.1

# Or qwen2.5:7b:
openclaw config set model.default qwen2.5:7b

# Or the 14B version if your VRAM supports it:
openclaw config set model.default qwen2.5:14b
```

> 💡 **Which model should you use?** For general assistant/agent work, `qwen2.5:14b` is excellent if your GPU supports it. For lighter systems, `llama3.1` (8B) is a strong choice. You can always switch later.

---

## Step 5: Start the Gateway

The OpenClaw **Gateway** is the background service that keeps your agent running, handles incoming messages, and manages connections to Discord, Telegram, or other channels.

```bash
openclaw gateway start
```

Check that it's running:
```bash
openclaw gateway status
```

You should see something like:
```
● OpenClaw Gateway
  Status: running
  PID: 12345
  Model: ollama/qwen2.5:14b
  Channels: 0 connected
```

### Make It Start Automatically on Boot

```bash
openclaw gateway enable
```

This sets up a systemd service so your agent comes back online after reboots without you having to do anything.

---

## Step 6: Test Your Agent

Let's make sure everything's talking to each other:

```bash
openclaw chat
```

This opens a direct terminal chat with your agent. Type "Hello, what can you do?" and hit Enter.

If you get a response, **your agent is alive.** 🎉

If you get an error:
- Make sure Ollama is running: `ollama serve` (or check `systemctl status ollama`)
- Make sure the model is downloaded: `ollama list`
- Check the gateway logs: `openclaw gateway logs --tail 50`

---

## Step 7: Basic Configuration

Your agent's home is `~/.openclaw/workspace/`. Let's look at what's there:

```bash
ls ~/.openclaw/workspace/
```

You'll see:
```
SOUL.md       ← Your agent's personality (we cover this in Guide 05)
USER.md       ← Info about you, so the agent knows who it's helping
MEMORY.md     ← Long-term memory (the agent updates this itself)
AGENTS.md     ← Operating instructions for the agent
openclaw.env  ← Secret keys and API tokens (NOT shared)
memory/       ← Daily log files
```

### Set Your Name

Open `USER.md` in a text editor:
```bash
nano ~/.openclaw/workspace/USER.md
```

Add your name and any context you want the agent to know about you:
```markdown
# USER.md - About Your Human

- **Name:** [Your name]
- **Timezone:** America/Chicago (or yours)

## Context
[Anything you want your agent to know about you]
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

---

## Step 8: The `ollama launch openclaw` Shortcut

Once everything is configured, your daily workflow is just:

```bash
# Start everything
ollama serve &          # Start Ollama (if not already running as a service)
openclaw gateway start  # Start OpenClaw gateway

# Chat directly
openclaw chat

# Check status
openclaw gateway status

# Stop when done
openclaw gateway stop
```

> 💡 If you set up the systemd services (Guide 02 for Ollama, `openclaw gateway enable` above), you don't need to manually start anything — both services start on boot automatically.

---

## What's Happening Under the Hood

Here's the flow when you send your agent a message:

```
You type a message
       ↓
OpenClaw Gateway receives it
       ↓
Gateway loads your agent's SOUL.md + recent MEMORY.md
       ↓
Sends the message + context to Ollama API
       ↓
Ollama runs inference on your GPU (the model thinks)
       ↓
Response comes back to Gateway
       ↓
Gateway processes it (runs tools, updates memory if needed)
       ↓
You see the response
```

The whole thing happens on your hardware. No cloud. No API bills. No data leaving your house.

---

## Model Switching

You can switch models on the fly:

```bash
# Switch to a different model
openclaw config set model.default llama3.1

# Or specify per-session
openclaw chat --model qwen2.5:14b
```

This is useful for testing — some tasks (like coding) do better with certain models.

---

## Jr.'s Setup for Reference

When Jr. set up Hohenheim for D&D campaigns, his workflow looked like this:

1. Pulled `qwen2.5:14b` on Ollama (14B model, fits his RTX 3080)
2. Set it as his default model in OpenClaw
3. Wrote a D&D-focused SOUL.md (covered in Guide 05)
4. Connected it to Discord (covered in Guide 04)
5. Let his friends talk to Hohenheim in a dedicated channel

His friends don't know (or care) that it's running off a gaming PC in his bedroom. They just know Hohenheim never forgets their character's backstory and keeps the campaign moving.

---

## Troubleshooting

**"Connection refused" when testing chat**
→ Ollama isn't running. Run: `ollama serve`

**Responses are slow**
→ Check GPU usage: `watch -n1 nvidia-smi` — if GPU utilization is 0%, you're running on CPU. Verify CUDA is set up (Guide 02).

**"Model not found" errors**
→ The model name in config doesn't match what's downloaded. Run `ollama list` to see exact names.

**Gateway won't start**
→ Check logs: `openclaw gateway logs --tail 100`
→ Common fix: Port conflict — something else is on port 3821. Try: `lsof -i :3821`

---

## Next Step

**→ [Guide 04: Discord Integration](./guide-04-discord-integration.md)**

Your agent can chat in the terminal. Now let's put it in Discord so your community (or your friends' D&D group) can actually use it.

---

*West AI Labs Community Guide Series | Updated Feb 2026*
