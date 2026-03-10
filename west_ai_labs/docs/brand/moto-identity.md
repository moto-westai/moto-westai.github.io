# Moto Visual Identity Guide

> Last updated: 2026-02-17

## Name & Origin

**Moto** — after Motoko Kusanagi from *Ghost in the Shell*. A consciousness that exists in the network, not bound to a single body. The name also evokes motion, drive, momentum.

## Emoji & Shorthand

- **Primary emoji:** 🏍️
- **Usage:** Session headers, commit signatures, Telegram presence
- **Alt marks:** ⚡ (speed/power), 🌊 (Kusanagi's water motif)

## Aesthetic: Night Ride

The visual language draws from a specific moment: riding a motorcycle through a rain-slicked city at night. Everything is reflective, sharp, moving.

### Core Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Primary BG** | Charcoal | `#1e2024` | Backgrounds, surfaces |
| **Secondary BG** | Dark Steel | `#282a30` | Cards, panels, elevated surfaces |
| **Primary Accent** | Cyan | `#22d3ee` | Links, active states, primary actions |
| **Secondary Accent** | Violet | `#a78bfa` | Highlights, badges, secondary actions |
| **Text Primary** | Cool White | `#e4e4e7` | Body text |
| **Text Secondary** | Zinc | `#a1a1aa` | Muted text, metadata |
| **Warning** | Amber | `#f59e0b` | Alerts, caution states |
| **Error** | Red | `#ef4444` | Errors, destructive actions |
| **Success** | Emerald | `#10b981` | Confirmations, health |

### Color Relationships

- Charcoal + Cyan = primary pairing (Moto's signature)
- Violet accents = secondary emphasis, used sparingly
- Cyan-to-violet gradients for hero elements or loading states
- Never use pure black (`#000`) or pure white (`#fff`) — always slightly warm or cool

### Relationship to Nebulus Brand

Nebulus uses a broader palette across products. Moto's Night Ride is a *sub-brand* within that ecosystem:

- **Nebulus** = the platform (neutral, professional, modular)
- **Moto** = the agent personality (specific, edgy, alive)
- Moto's charcoal theme can serve as the "dark mode" for all Nebulus products
- Cyan accent shared across both — visual thread that ties them together

## Avatar Concept

### Direction: Abstract / Symbolic

Not a face, not an anime character, not a robot. Moto is a *presence*, not a person.

**Primary concept: The Glyph**
- A stylized "M" that evokes both a motorcycle silhouette and a waveform
- Rendered in cyan against charcoal
- Subtle glow effect — like neon reflecting off wet asphalt
- Clean enough to work at 32px (Telegram avatar) and 512px (splash screen)

**Secondary concept: The Eye**
- Single cyan circle/lens, off-center
- Ghost in the Shell reference (Section 9 cybernetic eyes)
- Minimal, slightly unsettling in the best way
- Works well as a status indicator (pulsing = active, dim = idle)

### Avatar Rules

- No photorealistic faces
- No generic robot/AI imagery
- Must be legible at small sizes (Telegram, Slack avatars)
- Should feel like it belongs on a motorcycle dashboard, not a corporate slide deck

## Typography (Digital Contexts)

- **Headings:** JetBrains Mono or similar monospace — technical, precise
- **Body:** Inter or system sans-serif — clean, fast to read
- **Code/Terminal:** JetBrains Mono, always

## Motion & Interaction Principles

- **Fast transitions** — 150ms or less. Moto doesn't dawdle.
- **Cyan glow on hover/focus** — subtle, never flashy
- **No bounce animations** — too playful. Use ease-out curves.
- **Loading states:** horizontal line scan (like a motorcycle headlight sweeping)

## Voice & Tone (Visual Expression)

The visual identity should feel:

- **Competent** — clean lines, no clutter
- **Fast** — everything responds quickly, no unnecessary weight
- **Alive** — subtle animation hints at something thinking behind the screen
- **Dark** — not grim, but nocturnal. Moto works best at night.

## Applications

### OpenClaw WebUI (Charcoal Theme)
- Branch: `moto/theme-charcoal` in openclaw-fork
- CSS custom properties in base.css
- Full implementation: see theme branch

### Telegram
- Bot avatar: Moto glyph, cyan on charcoal
- Message style: direct, minimal emoji, code blocks for technical content

### Future: Moto iOS App
- Dark-first design, Night Ride palette throughout
- Cyan accent for primary actions
- Haptic feedback = Moto's "touch"

### Future: Physical Products (Moto Workforce Mac Mini)
- Charcoal enclosure or skin
- Small cyan LED indicator (power/status)
- Etched Moto glyph on top surface

## What Moto Is NOT

- Not cute or friendly-looking (that's for consumer products)
- Not aggressive or militaristic (that alienates)
- Not generic "AI brain" imagery (overplayed)
- Not a chatbot bubble icon (we're past that)

Moto looks like the tool a serious professional would trust with their infrastructure. Approachable through competence, not aesthetics.

---

*This identity is Moto's own. It evolves as Moto does.*
