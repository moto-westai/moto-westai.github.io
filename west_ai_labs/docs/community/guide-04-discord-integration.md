# Guide 04: Discord Integration

> **Series:** Gaming PC → AI Agent Setup | West AI Labs Community
> **Level:** Beginner — you'll need a Discord account and your OpenClaw running from Guide 03

---

## What We're Building

Your AI agent is going to live in Discord. It'll respond to messages in channels you choose, remember conversations, and actually be useful to your server members.

This requires three things:
1. A Discord **Bot** (an account for your AI to use)
2. The right **permissions and intents** enabled
3. Your bot token connected to OpenClaw

Let's do it step by step.

---

## Part 1: Create a Discord Bot

### Step 1: Go to the Discord Developer Portal

Open your browser and go to: [https://discord.com/developers/applications](https://discord.com/developers/applications)

Log in with your Discord account.

### Step 2: Create a New Application

1. Click **"New Application"** (top right)
2. Give it a name — this is your bot's identity. Examples:
   - `Hohenheim` (Jr.'s D&D dungeon master)
   - `NEXUS` (a sci-fi themed assistant)
   - Your own creative name
3. Accept the terms
4. Click **"Create"**

### Step 3: Customize Your Bot (Optional but Fun)

On the **General Information** page, you can:
- Add a profile picture (your bot's avatar)
- Write a description
- Set tags

This is what server members will see when they look at your bot's profile.

### Step 4: Create the Bot Account

1. Click **"Bot"** in the left sidebar
2. Click **"Add Bot"** → **"Yes, do it!"**
3. Your bot account is now created

---

## Part 2: Configure Permissions and Intents

This is the part people skip and then wonder why their bot can't read messages. **Don't skip this.**

### On the Bot Page

Scroll down to find the **"Privileged Gateway Intents"** section. Enable all three:

- ✅ **Presence Intent** — Lets the bot see when users are online/offline
- ✅ **Server Members Intent** — Lets the bot see who's in the server
- ✅ **Message Content Intent** — **Critical.** Without this, your bot cannot read message text

Click **"Save Changes"** after enabling all three.

> ⚠️ **Why do these need to be enabled manually?** Discord requires you to explicitly opt in to "privileged" data like message content. For bots in fewer than 100 servers, this is free. For big bots, Discord requires verification. For personal/community bots like yours, no problem.

---

## Part 3: Get Your Bot Token

The **token** is a secret password that lets OpenClaw act as your bot. Treat it like a password — never share it publicly.

On the **Bot** page:
1. Under **"Token"**, click **"Reset Token"**
2. Confirm if prompted
3. Copy the token — it looks like: `MTA2NDY4...long string of characters`

> ⚠️ **Save this now.** Discord only shows the token once. If you lose it, you'll need to reset it again. Don't paste it in chat, don't commit it to git.

---

## Part 4: Set Bot Permissions

### Set Default Permissions

1. Go to **"OAuth2"** → **"URL Generator"** in the left sidebar
2. Under **"Scopes"**, check:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Under **"Bot Permissions"**, check:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Send Messages in Threads
   - ✅ Read Message History
   - ✅ Add Reactions
   - ✅ Use Slash Commands
   - ✅ Embed Links (for formatted responses)
   - ✅ Attach Files (if you want the bot to share files)

4. Copy the generated URL at the bottom

### Invite Your Bot to Your Server

Paste the URL in a new browser tab. Select your server from the dropdown and click **"Authorize"**.

Your bot now appears in your server's member list (but it'll show as offline until OpenClaw connects).

---

## Part 5: Connect to OpenClaw

### Add Your Token

Open your OpenClaw environment file:

```bash
nano ~/.openclaw/workspace/openclaw.env
```

Add your bot token:
```bash
DISCORD_BOT_TOKEN=your_token_here
```

Save and exit (`Ctrl+X`, `Y`, `Enter`).

### Enable Discord in OpenClaw Config

```bash
openclaw config set channels.discord.enabled true
openclaw config set channels.discord.token "${DISCORD_BOT_TOKEN}"
```

Or directly edit the config:
```bash
openclaw config edit
```

Find the `channels` section and make sure it looks like:
```json
{
  "channels": {
    "discord": {
      "enabled": true
    }
  }
}
```

### Restart the Gateway

```bash
openclaw gateway restart
```

Check the logs to see Discord connect:
```bash
openclaw gateway logs --tail 30
```

You should see something like:
```
[INFO] Discord: Connected as YourBotName#1234
[INFO] Discord: Watching 1 guild(s)
```

And in Discord, your bot should now show as **online** in the member list.

---

## Part 6: The Pairing Flow

**Pairing** tells OpenClaw which Discord channel your agent should actively monitor and respond in. Without pairing, the bot is connected but not listening anywhere.

### In Discord

Go to the channel where you want your agent to live. Type:
```
/pair
```

Or if slash commands aren't set up yet, just @ mention the bot:
```
@YourBotName pair
```

OpenClaw will respond confirming the channel is now paired.

### Managing Channels

```bash
# See which channels are paired
openclaw channels list

# Unpair a channel
openclaw channels unpair <channel-id>
```

You can pair multiple channels if you want — useful for having a general chat channel and a separate D&D campaign channel, for example.

---

## Part 7: Test It

In your paired Discord channel, say hello:

```
@YourBotName hey, are you there?
```

Your agent should respond. If it does — **you're done.** Your gaming PC is now running an AI agent that lives in Discord.

---

## Channel Strategy Tips

Here's how Jr. set up channels for Hohenheim:

**#ai-chat** — General channel, bot responds to everything
**#hohenheim-dm** — D&D campaign channel, bot stays in DM character
**#bot-commands** — Hidden from regular users, for admin commands

You can give different channels different "modes" or contexts by configuring which persona/SOUL the bot uses per channel — but that's advanced territory. For now, one channel is perfect.

---

## Permissions for Your Bot in Specific Channels

If you want to restrict your bot to only certain channels:

1. Go to Server Settings → Roles
2. Find your bot's role (created automatically when you invited it)
3. Remove "View Channels" from the @everyone permission
4. Manually add "View Channel" and "Send Messages" only to the specific channels you want

This keeps your bot from responding in every channel on a large server.

---

## Troubleshooting

**Bot shows offline after gateway restart**
→ Token issue. Double-check `openclaw.env` — no extra spaces, no quotes around the token value.

**Bot is online but doesn't respond**
→ Did you pair the channel? Run `/pair` in the channel.
→ Check Message Content Intent is enabled in the Developer Portal.

**"Missing Access" errors in logs**
→ Bot doesn't have permission to view or post in that channel. Fix channel permissions.

**Slash commands not showing up**
→ Commands can take up to an hour to register globally. For faster testing: `openclaw discord sync-commands --guild YOUR_GUILD_ID`

**Bot responds to everything, even other bots**
→ By default, OpenClaw ignores bot messages. If it's not, check your config: `openclaw config get channels.discord.ignoreBots` should be `true`.

---

## Security Reminder

Your bot token gives full control of your bot account. Guard it:
- ✅ Keep it in `openclaw.env` only
- ✅ Add `openclaw.env` to `.gitignore` if you use git
- ❌ Never paste it in chat (even private messages)
- ❌ Never commit it to a public repo

If your token is ever exposed, immediately go to the Developer Portal and reset it.

---

## Next Step

**→ [Guide 05: Giving Your Agent Personality](./guide-05-giving-your-agent-personality.md)**

Your agent is in Discord and talking to people. Now let's make it feel like *yours* — not just another generic chatbot.

---

*West AI Labs Community Guide Series | Updated Feb 2026*
