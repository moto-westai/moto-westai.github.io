# Apple Foundation Models API & Private Cloud Compute Research
## West AI Labs — Moto iOS Integration Analysis
**Date:** February 18, 2026  
**Status:** Active Research  

---

## 1. Foundation Models API

### What It Is
Apple's Foundation Models framework (introduced WWDC25, shipped with iOS 26/macOS Tahoe 26) gives developers **direct access to the on-device ~3B parameter language model** powering Apple Intelligence. It's a Swift-native API for text generation, structured output, and tool calling.

### Key Capabilities
- **Text generation** — summarization, entity extraction, text understanding, refinement, short dialog, creative content
- **Structured output ("Guided Generation")** — constrain model output to Swift types via `@Generable` macro; produces JSON-schema-aligned typed responses
- **Tool calling** — model can invoke developer-defined `Tool` instances during generation
- **Streaming responses** — async streaming for real-time UI updates
- **Image understanding** — vision encoder (ViTDet-L, 300M params on-device; ViT-g 1B on server) for multimodal input
- **Content tagging** — specialized adapter via `SystemLanguageModel(useCase: .contentTagging)` for entity extraction, topic detection
- **Multi-turn conversation** — `LanguageModelSession` maintains transcript history

### What It Does NOT Do (Currently)
- **No embeddings API exposed** — the framework is generation-only; no public embedding endpoint for RAG/vector search
- **No direct PCC access for developers** — the API routes to on-device model only; PCC is used by Apple's own features (Siri, system intelligence), not exposed to third-party apps via this framework
- **Not a general chatbot** — Apple explicitly says the 3B model "is not designed to be a chatbot for general world knowledge"

### API Surface (Swift)
```swift
import FoundationModels

// Get the model
let model = SystemLanguageModel.default

// Check availability
switch model.availability {
case .available: break
case .unavailable(let reason): // handle
}

// Create session with instructions
let session = LanguageModelSession {
    "You are a helpful assistant for my app."
}

// Simple generation
let result = try await session.respond(to: "Summarize this text...")
print(result.content)

// Structured output
@Generable
struct MovieReview {
    var sentiment: String
    var score: Int
    var summary: String
}
let review: MovieReview = try await session.respond(to: prompt, generating: MovieReview.self)

// Streaming
for try await partial in session.streamResponse(to: "Write a story...") {
    print(partial.content)
}

// Tool calling
struct WeatherTool: Tool { ... }
let session = LanguageModelSession(tools: [WeatherTool()])
```

### Model Architecture Details (from Apple ML Research)
- **On-device:** ~3B parameters, split into two blocks (5:3 depth ratio), KV cache sharing reduces memory 37.5%, optimized for Apple silicon Neural Engine
- **Server (PCC):** Parallel Track Mixture-of-Experts (PT-MoE) — multiple smaller transformer "tracks" process tokens independently, synchronize only at boundaries. Reduces synchronization overhead by ~87.5%
- **Context:** Interleaved sliding-window local attention (RoPE) + global attention (NoPE) for long context
- **Languages:** 15 languages supported
- **Vision:** On-device ViTDet-L (300M params) with novel Register-Window mechanism; server ViT-g (1B params)

### Pricing & Rate Limits
- **FREE** — on-device inference has zero API cost, no rate limits, works offline
- No per-token charges, no subscription beyond Apple Developer Program
- Guardrails are mandatory and cannot be disabled (Apple content safety policies enforced)

### Developer Requirements
- Apple Developer Program ($99/yr)
- Xcode 26+
- iOS 26 / macOS Tahoe 26
- Apple Intelligence-capable device (iPhone 15 Pro+, M-series Macs, recent iPads)
- Must comply with [Acceptable Use Requirements](https://developer.apple.com/apple-intelligence/acceptable-use-requirements-for-the-foundation-models-framework/)

---

## 2. Private Cloud Compute (PCC) Architecture

### How It Works
PCC is Apple's secure cloud inference infrastructure:
- **Custom server nodes** built on Apple silicon (currently M2 Ultra, transitioning to M5)
- **Hardened OS** — not macOS; a stripped-down, purpose-built operating system
- **Stateless processing** — no data retention; requests are processed and discarded
- **Encrypted end-to-end** — device encrypts request, PCC node processes in Secure Enclave, result returned encrypted
- **Verifiable transparency** — Apple publishes PCC software images for independent security audit
- **No operator access** — even Apple cannot see user data in transit or at rest

### M5 PCC Update (February 17, 2026 — BREAKING)
- Apple's latest PCC software release references **M5 chips (model J226C)** in PCC servers
- Skipped M3 Ultra and M4 for PCC — going straight from M2 Ultra to M5
- **"Private Cloud Compute Agent Worker"** discovered in the software — runs a **version of iOS with a new agentic architecture** for serving AI requests
- This is distinct from the previous PCC worker model; suggests Apple is building autonomous agent-style task execution in the cloud

### What "PCC Agent Worker" Likely Means
- PCC moving from simple request→response inference to **multi-step agentic task execution**
- Running iOS (not just the PCC OS) suggests these workers can access iOS frameworks, APIs, and capabilities
- Aligns with Apple's Siri transformation plans — Siri becoming an agent that can take actions across apps
- Apple's deal with Google to use Gemini models in PCC means third-party models running in Apple's secure infrastructure
- **Implication:** Apple is building the infrastructure for AI agents that can execute complex, multi-step tasks while maintaining privacy guarantees

### Dedicated AI Server Chips
- Ming-Chi Kuo reports Apple developing **dedicated AI server chips** (not M-series)
- Mass production: second half of 2026, deployment: 2027
- PCC servers now being manufactured in **Houston, Texas** (part of $600B domestic investment)

---

## 3. Developer Access Requirements

### What We Need to Get Started

| Requirement | Status | Notes |
|---|---|---|
| Apple Developer Program | **DEFERRED** | $99/yr — waiting on Mac Mini situation |
| Mac with Apple Silicon | ✅ | Mac Mini M4 Pro at 192.168.4.30 |
| macOS Tahoe 26 | **NEEDED** | Must install macOS 26 beta |
| Xcode 26 | **NEEDED** | Comes with macOS 26 |
| Apple Intelligence enabled | **NEEDED** | Must be enabled in Settings, model downloads ~2GB |
| iOS 26 device for testing | **NEEDED** | iPhone 15 Pro+ or use Simulator |
| iOS 26.4 beta | **FUTURE** | Contains PCC Agent Worker interface code |

### Hardware Compatibility
- **Mac Mini M4 Pro** — fully compatible with Foundation Models framework on macOS
- Can run Xcode 26 simulator for iOS app testing
- Can also run the on-device model directly for macOS app development
- **Note:** The M4 Pro Mac Mini has sufficient RAM and Neural Engine for the 3B model

---

## 4. Moto iOS Integration Opportunities

### 4.1 On-Device 3B Model as Fast Local Fallback — **YES, HIGH VALUE**
The Foundation Models API is a **perfect fit** for Moto's local inference tier:
- **Zero cost, zero latency to cloud** — runs entirely on device
- **Works offline** — critical for phone-as-node reliability
- **Good at:** Summarization, entity extraction, text understanding, classification, short dialog
- **Not good at:** General world knowledge, complex reasoning, long-form generation
- **Use cases for Moto:**
  - Quick intent classification ("Is this a command, question, or chat?")
  - Entity extraction from user input
  - Summarizing notifications/emails
  - Generating structured responses (via Guided Generation)
  - Local tool routing decisions

### 4.2 PCC for Heavier Inference — **NOT YET AVAILABLE TO DEVELOPERS**
- Currently, PCC is **only accessible through Apple's own system features** (Siri, Writing Tools, etc.)
- The Foundation Models framework routes **only to the on-device model**
- **No public API for developers to send requests to PCC**
- This may change — the PCC Agent Worker suggests Apple is expanding PCC capabilities
- **Watch for WWDC26 (June 2026)** for potential developer PCC access

### 4.3 Revised Tiered Architecture

**Current plan:** Phone → Mac Mini (MLX) → Cloud (Anthropic/OpenAI)

**With Foundation Models integration:**
```
Tier 0: On-Device (Apple 3B model via Foundation Models)
  → Fast, free, offline, private
  → Intent classification, entity extraction, simple generation
  → Response time: <500ms

Tier 1: Edge (Mac Mini M4 Pro via MLX)  
  → Larger models (7B-70B), local network
  → Complex reasoning, long generation, embeddings
  → Response time: 1-5s

Tier 2: Cloud (Anthropic Claude / OpenAI)
  → Most capable models
  → Complex analysis, world knowledge, multi-modal
  → Response time: 2-10s

Future Tier 1.5: PCC (if Apple opens developer access)
  → Apple's server models, privacy-preserving
  → Would replace some Cloud tier usage
```

### 4.4 App Intents / Siri Integration — **HIGH VALUE**
- Foundation Models framework + App Intents = Siri can invoke Moto features
- Users say "Hey Siri, ask Moto to..." → routes to Moto's App Intent → uses Foundation Models for processing
- This makes Moto a **first-class citizen in the Apple Intelligence ecosystem** rather than competing with it
- Tool calling in Foundation Models means the on-device model can invoke Moto's defined tools

### 4.5 Embeddings for Local RAG — **NOT AVAILABLE**
- Foundation Models framework does **not expose an embeddings API**
- For on-device RAG, we'd still need:
  - MLX-based embedding model on Mac Mini, OR
  - Core ML model for on-device embeddings (separate from Foundation Models), OR
  - Wait for Apple to add embeddings to the framework (possible future addition)
- **Alternative:** Use the model's entity extraction + content tagging for lightweight "poor man's RAG" (keyword-based retrieval + LLM reranking)

---

## 5. Development Environment Setup

### Mac Mini M4 Pro (192.168.4.30) — Required Steps

1. **Enroll in Apple Developer Program** ($99/yr) — required for beta access
2. **Install macOS Tahoe 26 beta** — download from developer.apple.com
3. **Install Xcode 26 beta** — ~30GB download
4. **Enable Apple Intelligence** — Settings → Apple Intelligence & Siri → Enable
5. **Wait for model download** — the 3B model downloads automatically (~2GB)
6. **Create new Xcode project** — SwiftUI app targeting iOS 26
7. **Import FoundationModels** — start coding against the API

### Simulator vs Device
- **Simulator:** Can test Foundation Models on Mac (uses Mac's Neural Engine)
- **Physical device:** Need iPhone 15 Pro+ running iOS 26 beta for real device testing
- **Tart VM option:** Could create a clean macOS 26 VM for isolated dev environment, but Neural Engine passthrough may not work in VMs — test on bare metal recommended

### Xcode 26 Key Features for AI Development
- **Coding Tools powered by ChatGPT** — AI-assisted code completion
- **Foundation Models playground** — test prompts directly in Xcode
- **Swift 6.2** — required for `@Generable` macro and other Foundation Models features

---

## 6. Competitive Implications

### Does PCC Agent Worker Help or Threaten Moto?

**It helps — significantly:**
- Apple is building the **platform** for agentic AI, not the **apps**
- Foundation Models framework is Apple saying "build AI features in YOUR apps"
- PCC Agent Worker makes the infrastructure better, which benefits apps like Moto
- Apple Intelligence handles system-level tasks; Moto handles **personal AI assistant** tasks
- Apple's privacy-first approach **validates Moto's local-first architecture**

**Positioning strategy — "Alongside, not against":**
- Moto should be an **Apple Intelligence-native app** — use Foundation Models, App Intents, Siri integration
- Moto's value prop becomes: "Your personal AI that works WITH Apple Intelligence, extending it with your own models, memory, and multi-device orchestration"
- Apple provides the on-device model; Moto provides the **orchestration, memory, and multi-model routing**
- Key differentiator: Moto connects to **non-Apple infrastructure** (Mac Mini MLX, Anthropic, OpenAI) — something Apple Intelligence alone can't do

**Threats to watch:**
- If Apple opens PCC to developers AND adds embeddings + RAG, some of Moto's edge tier becomes redundant
- If Siri becomes truly agentic (multi-step, cross-app), it competes directly with Moto's orchestration layer
- Apple could restrict apps that "replicate Apple Intelligence functionality" — monitor App Store guidelines

### Competitive Landscape Shift
- Apple hosting partner models (Gemini on PCC) turns Google/OpenAI into utility providers
- This validates the **multi-model orchestration** approach — even Apple routes to different models for different tasks
- Startups building AI assistants that DON'T integrate with Apple Intelligence will be at a disadvantage
- **West AI Labs' local-first, privacy-first positioning is strongly aligned with Apple's direction**

---

## 7. March 4, 2026 Apple Event — What to Watch

### Confirmed: "Special Apple Experience" — March 4, NYC/London/Shanghai

**Expected announcements (March 2-4 rollout per Gruber):**
- **MacBook Pro with M5 Pro / M5 Max** — likely March 4
- **M5 MacBook Air** — possibly same week
- **iPhone 17e** — budget iPhone
- **8th-gen iPad Air** — M-series update
- **12th-gen iPad** — entry-level refresh
- **Budget MacBook (~$599)** — new product category

### What to Watch for Moto/West AI Labs:
1. **M5 Mac Mini** — expected spring/summer 2026 (M5 and M5 Pro options). Macworld reports no consistent upgrade cycle. May NOT be at March 4 event — could be later
2. **Foundation Models API updates** — any expansion of capabilities, PCC developer access
3. **Apple Intelligence enhancements** — new Siri agentic features that signal PCC Agent Worker going live
4. **Pricing on M5 Pro/Max** — informs Mac Mini M5 Pro pricing expectations
5. **Any developer-facing PCC announcements** — would be a game-changer

### Mac Mini M5 Timeline
- Current Mac Mini M4 Pro is available and fully capable for our development
- M5 Mac Mini likely **spring/summer 2026** — not imminent
- **Recommendation:** Don't wait for M5 Mac Mini. The M4 Pro is excellent for development and MLX inference

---

## 8. Timeline & Recommendations

### DO NOW (February 2026)

| Priority | Action | Cost | Effort |
|---|---|---|---|
| **P0** | Decide on Apple Developer Program enrollment | $99/yr | Low |
| **P0** | Resolve Mac Mini situation (brother keeping it?) | $0 or ~$1,400 | Decision |
| **P1** | Install macOS Tahoe 26 beta on Mac Mini | $0 | 2 hours |
| **P1** | Install Xcode 26, create Foundation Models test project | $0 | 1 day |
| **P1** | Build proof-of-concept: Foundation Models for intent classification | $0 | 2-3 days |
| **P2** | Prototype Moto's Tier 0 integration (on-device model for quick tasks) | $0 | 1 week |

### DO SOON (March-April 2026)

| Priority | Action | Notes |
|---|---|---|
| **P1** | Watch March 4 event for M5 pricing, AI updates | Informs hardware decisions |
| **P1** | Implement App Intents for Siri integration in Moto | Makes Moto Apple Intelligence-native |
| **P1** | Build tiered routing: Foundation Models → MLX → Cloud | Core architecture feature |
| **P2** | Explore Core ML for on-device embeddings (separate from Foundation Models) | Enables local RAG |
| **P2** | Test Foundation Models tool calling for Moto's action system | Could replace custom intent parsing |

### WAIT FOR (WWDC26 — June 2026)

| Item | Why Wait |
|---|---|
| PCC developer access | Not available yet; may be announced at WWDC26 |
| Foundation Models embeddings | Not in current API; may be added |
| M5 Mac Mini purchase | Wait for announcement + pricing |
| Dedicated AI server chip plans | Apple's 2027 timeline; too early to plan around |

### Key Strategic Decisions

1. **Apple Developer Program — Enroll NOW.** $99/yr is trivial. Blocks everything else.
2. **Mac Mini — Use the M4 Pro.** Don't wait for M5. It's more than capable.
3. **Foundation Models — Integrate as Tier 0.** Free, fast, private. Perfect for intent routing and simple tasks.
4. **Don't compete with Siri.** Be the bridge between Apple Intelligence and the broader AI ecosystem.
5. **Keep MLX tier.** Foundation Models doesn't replace the need for larger local models — it complements them.

---

## Sources

- [Apple Foundation Models Documentation](https://developer.apple.com/documentation/FoundationModels)
- [WWDC25: Meet the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/286/)
- [WWDC25: Deep dive into the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/301/)
- [Apple ML Research: Foundation Models 2025 Updates](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)
- [Apple ML Research: Tech Report 2025](https://machinelearning.apple.com/research/apple-foundation-models-tech-report-2025)
- [9to5Mac: M5-based PCC Architecture](https://9to5mac.com/2026/02/17/apple-plans-m5-based-private-cloud-compute-architecture-for-apple-intelligence/)
- [Apple Newsroom: Foundation Models framework](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/)
- [Apple Security: Private Cloud Compute](https://security.apple.com/blog/private-cloud-compute/)
- [MacRumors: March 4 Event Preview](https://www.macrumors.com/2026/02/17/apple-event-march-2026-preview/)
- [Macworld: 2026 Mac Mini Rumors](https://www.macworld.com/article/2964754/2026-mac-mini-m5-pro-design-specs-release-date.html)
- [CreateWithSwift: Exploring Foundation Models](https://www.createwithswift.com/exploring-the-foundation-models-framework/)
