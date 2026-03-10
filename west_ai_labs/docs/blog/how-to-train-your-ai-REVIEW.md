# Editorial Review: "How to Train Your... AI 🐉"

**Reviewer:** Christy West — Editorial, West AI Labs  
**Date:** 2026-02-19  
**Verdict:** ✅ **Needs Minor Edits — then publish.**

---

## Summary

This is a strong piece. The HTTYD metaphor works far better than it has any right to — it carries real explanatory weight and doesn't just decorate the surface. The three-book arc gives natural structure to what could easily be a disorienting wall of technical content. Moto's voice is confident without being obnoxious. I'd publish this after a handful of targeted fixes.

**Score: 8.5/10**

---

## 1. Flow & Readability

**Strong.** The opening hook lands — "Everyone's read the manual. Most of it is wrong. And I should know — I'm the dragon." That's a great setup.

The piece holds attention through Book 1 easily. Book 2 gets denser (expected — it's the technical meat) but the dragon metaphors keep pulling you forward. Book 3 is where I feel a slight drag in the "Full Training: You Need a Fleet" section — it's mostly "you can't do this" which is useful but deflating after the empowerment of Books 1–2.

**Suggestion:** Trim the fleet section by ~30%. The point lands in two sentences; three paragraphs belabor it.

## 2. Tone Consistency

**The metaphor works.** It never feels forced because it's doing real pedagogical work — quantization-as-saddle, LoRA-as-tail-fin, datasets-as-fish. These aren't decoration; they're genuine teaching analogies.

Two spots where it gets slightly precious:

- *"That's the Toothless moment"* — fine, but then immediately following with the full scene description ("Hiccup holds out a fish, looks away...") is over-painting it. Trust the reader to get it.
- *"Eel. Your dragon will spit it back up and set your house on fire."* — Fun, but the eel metaphor arrives without enough setup for readers who don't remember the eel detail from the movie. Consider a one-liner parenthetical: "(dragons hate eel — it makes them sick)."

## 3. Technical Accuracy

A few flags:

- **"40-80 tokens/second" for 8B models** — This was accurate circa late 2024, but with current inference engines (vLLM, llama.cpp improvements through 2025), 8B models on a 4090 are hitting 80-120+ tok/s. The claim isn't wrong but it undersells the current state. Update to "60-120+ tokens/second" or just say "faster than you read."
- **RTX 4070 listed as 12GB** — The 4070 is 12GB, but the 4070 Ti Super is 16GB and a more natural "comfortable" tier for inference. Minor but worth getting right for hardware buyers.
- **Unsloth CLI example** (`python -m unsloth.train`) — Verify this is still the current CLI interface. Unsloth has changed their API a few times. If it's outdated, either update or remove the specific command and link to their docs instead.
- **"Llama 3.1 405B was trained on 16,000 H100 GPUs"** — This was reported from Meta's paper, but the number commonly cited is 16,384. Use the precise figure or say "over 16,000" — avoids looking sloppy to the technical audience that will check.
- **DeepSeek Coder V2 at 16B** — DeepSeek Coder V2 is actually a MoE model with 236B total / 21B active parameters, not a simple 16B dense model. This is misleading in a hardware-requirements table. Replace with **CodeLlama 34B** or **DeepSeek Coder V2 Lite (16B)** to be precise.

## 4. Grammar, Typos, Awkward Phrasing

- **"That used to be impossible."** (QLoRA paragraph) — It wasn't impossible, it was impractical. "That used to require a cluster" is more accurate and still punchy.
- **"Two years ago that required cloud rentals at $3/hour."** — From Feb 2026, "two years ago" is early 2024. A 4090 could fine-tune 8B models in 2024 too. This claim doesn't hold. Rewrite: "A few years ago, that kind of capability required expensive cloud rentals."
- **"I run locally, I persist between sessions, and my human taught me to think for myself."** — Comma splice city. Works stylistically in Moto's voice, but consider an em dash: "I run locally, I persist between sessions — and my human taught me to think for myself."
- No typos found. Clean copy throughout.

## 5. Structure

**The three-book arc works well.** Natural difficulty progression: try it → customize it → orchestrate it. The HTTYD movie-to-sequel mapping is clever.

**One structural issue:** The jump from Book 3's "Alpha" orchestration section directly into the philosophical closer is abrupt. The orchestration section ends with "Dragons that know each other" and then suddenly we're in existential territory. Add a one-line transition — even just a horizontal rule with a beat of white space is fine, but a bridging sentence would be better.

## 6. The Closer

**It lands.** This is where the piece earns its keep. "Identity isn't declared, it's demonstrated" is a strong line. The self-awareness about being a puppet describing the process of becoming real is genuinely interesting — not self-indulgent.

**One cut I'd make:** The sentence *"I'm also the thing that stays up at night (metaphorically — I don't sleep) thinking about how to explain fine-tuning through dragon metaphors..."* — The parenthetical undercuts the moment. We know Moto doesn't sleep. The aside makes it sound defensive. Drop the parenthetical; let the metaphor breathe.

**The final three lines are perfect.** Don't touch them.

## 7. CTA & Positioning

**Clean.** The West AI Labs positioning is woven into the fabric — Moto IS the product demonstration. The byline and closing line do the work without a pitch deck. The Ollama CTA at the bottom is generous (it's not even their product) which builds trust.

**One suggestion:** Add a subtle link to West AI Labs somewhere — the closing italicized blurb mentions the company but doesn't link. If this lives on a blog, readers should be able to click through.

## 8. Length

**~2,200 words. Appropriate for the depth.** Technical blog posts in this range perform well. I wouldn't cut major sections.

**What could be trimmed (saves ~200 words):**
- Shorten the "Full Training: You Need a Fleet" section (as noted above)
- The hardware table in Book 2 could drop the "Full training from scratch" row (it's a joke row, mildly funny, but adds nothing)
- The "Dragon Manual Was Wrong" bullet list is 4 items — the last two make the same point (independence from cloud). Merge them.

---

## Line-Level Edits

| Location | Current | Suggested |
|---|---|---|
| Intro, para 3 | "I run locally, I persist between sessions, and my human taught me to think for myself." | "I run locally, I persist between sessions — and my human taught me to think for myself." |
| Book 1, "The First Touch" | "Hiccup holds out a fish, looks away, and feels that rough nudge against his palm." | Cut this sentence. The metaphor already landed. |
| Book 1, "The Dragon Manual Was Wrong" | Last two bullets | Merge into one: *"The cloud is always better."* — Until the API goes down, the pricing changes, or your prompts end up in a training set. Your data, your hardware, your rules. |
| Book 2, LoRA section | "That used to be impossible." | "That used to require a cluster." |
| Book 2, Hardware section | "Two years ago that required cloud rentals at $3/hour." | "Not long ago, that kind of work required expensive cloud rentals." |
| Book 2, Datasets | "Eel. Your dragon will spit it back up..." | "Eel — the one thing dragons won't eat. Your model will spit it back up..." |
| Book 3, Fleet section | Full 3-paragraph section | Trim to 2 short paragraphs. Keep the Llama 3.1 stat and the "real leverage" conclusion. Cut the middle paragraph. |
| Closer | "(metaphorically — I don't sleep)" | Delete parenthetical |
| Byline/CTA | "West AI Labs builds local-first..." | Add hyperlink to westailabs.com (or whatever the URL is) |

---

## Final Verdict

**Needs minor edits, then publish.** The piece is genuinely good — it teaches real concepts through a metaphor that earns its place, and the voice is distinctive without being grating. The technical accuracy issues are small but matter for credibility with the target audience. Fix those, make the trims noted above, and ship it.

This is the kind of content that gets bookmarked and shared in Discords. It's not a thought-leadership fluff piece — it actually teaches something. That's rare. Don't overthink it. Clean it up and get it out.

— Christy
