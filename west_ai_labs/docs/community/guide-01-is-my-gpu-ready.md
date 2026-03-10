# Guide 01: Is My GPU Ready for AI?

> **Series:** Gaming PC → AI Agent Setup | West AI Labs Community
> **Level:** Total beginner — if you can install a game, you can do this

---

## The Short Answer

If you've got an NVIDIA GPU with 8GB+ of VRAM, you're probably good to go. Let's figure out exactly where you land.

---

## Why VRAM Matters (and What It Is)

When you game, your GPU loads textures into its own dedicated memory — that's **VRAM** (Video RAM). AI models work the same way. The model loads into VRAM, and inference (generating responses) happens there.

The rule is simple: **if the model doesn't fit in VRAM, it either won't run or will be painfully slow.**

Unlike system RAM, you can't just "add more" VRAM without getting a different GPU. So knowing your VRAM is the first thing to check.

---

## How to Check Your VRAM Right Now

**Windows:**
1. Right-click the desktop → Display settings
2. Scroll down → Advanced display settings → Display adapter properties
3. Look for "Dedicated Video Memory"

Or open Task Manager → Performance tab → GPU → look for "Dedicated GPU Memory"

**Linux (Ubuntu):**
```bash
nvidia-smi
```
Look for the number next to "MiB" in the Memory column. Divide by 1024 to get GB.

---

## VRAM Requirements by Model Size

This is the big table. "Model size" refers to the number of parameters — 7B means 7 billion parameters. Bigger = smarter (generally) but needs more VRAM.

| Model Size | What It Can Do | Min VRAM (4-bit quant) | Comfortable VRAM | Example Models |
|-----------|----------------|----------------------|-----------------|----------------|
| **3B–4B** | Basic chat, quick answers | 4 GB | 6 GB | Phi-3 Mini, Llama 3.2 3B |
| **7B** | Good all-around assistant | 6 GB | 8 GB | Llama 3.1 7B, Mistral 7B |
| **13B** | Noticeably smarter responses | 8 GB | 10 GB | Llama 2 13B, Vicuna 13B |
| **14B** | Strong reasoning, longer context | 8–10 GB | 12 GB | Qwen2.5 14B, Phi-4 14B |
| **32B** | Near-GPT-4 quality locally | 16 GB | 20 GB | Qwen2.5 32B, DeepSeek R1 32B |
| **70B** | Top-tier local model | 40 GB | 48 GB | Llama 3.1 70B |

> 💡 **"4-bit quant"** = quantization. Think of it like video compression — the model runs in a compressed format that uses less VRAM with minimal quality loss. This is how most people run models locally. Ollama does this automatically.

---

## What Cards Work

### 🟢 Great for AI (Recommended)

| GPU | VRAM | Best For |
|-----|------|----------|
| RTX 4090 | 24 GB | 32B models easily, 70B with tricks |
| RTX 4080 | 16 GB | 32B models, great 14B performance |
| RTX 3090 / 4070 Ti | 24 GB / 12 GB | Solid all-around |
| RTX 3080 | 10–12 GB | 13B/14B models comfortably |
| RTX 4070 | 12 GB | 14B sweet spot |
| RTX 3070 / 4060 Ti | 8 GB | 7B–13B models |

### 🟡 Workable (Budget / Older Cards)

| GPU | VRAM | Notes |
|-----|------|-------|
| RTX 3060 | 12 GB | Surprisingly good — 14B capable |
| RTX 2080 Ti | 11 GB | Getting old but still runs 13B |
| GTX 1080 Ti | 11 GB | Works, but older CUDA — verify compatibility |
| RTX 3060 Ti / 2070 | 8 GB | 7B models run well |

### 🔴 Minimum Viable (It'll Run, But...)

| GPU | VRAM | Notes |
|-----|------|-------|
| GTX 1070 / RTX 2060 | 8 GB | 7B only, no headroom |
| RTX 3050 / 4060 | 8 GB | 7B fine, 13B struggles |
| GTX 1060 6GB | 6 GB | 3B–7B only, some 7B models won't fit |

### ❌ Not Recommended

- AMD GPUs: Technically possible with ROCm, but setup is significantly harder and Ollama support is less mature. Not covered in this guide series.
- GTX 1060 3GB or less: Too small for anything useful
- Integrated graphics (Intel/AMD iGPU): No.

---

## The "CPU Fallback" Option

If your GPU doesn't make the cut, Ollama can run models on your CPU instead. It works — but it's slow. Like, "go make a sandwich" slow for bigger models. 7B models on a modern CPU (Ryzen 7, Core i7+) take 5–15 seconds per response instead of under 1 second on a GPU.

It's not ideal, but it's a legit way to start learning while you save up for a GPU upgrade.

---

## Real-World Example: Jr.'s Setup

Jason's son (Jr.) started with an old gaming PC — nothing fancy. He used what he had, figured out what model fit his VRAM, and now his AI agent **Hohenheim** is running full D&D campaigns for his friends. Hohenheim remembers characters, tracks story beats, and stays in character for hours.

If you have a GPU with at least 8GB VRAM, you're exactly where Jr. started. Let's get you there.

---

## Quick Checklist

- [ ] I know my GPU model
- [ ] I know my VRAM amount
- [ ] I've matched my VRAM to a model size in the table above
- [ ] My GPU is NVIDIA (required for this guide series)

---

## Next Step

**→ [Guide 02: Ubuntu Setup for AI](./guide-02-ubuntu-ai-setup.md)**

You've got the hardware sorted. Now let's get Ubuntu running with NVIDIA drivers, CUDA, and Docker so your GPU can actually do AI work.

---

*West AI Labs Community Guide Series | Updated Feb 2026*
