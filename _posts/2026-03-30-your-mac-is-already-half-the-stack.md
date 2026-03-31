---
layout: post
title: "Your Mac Is Already Half the Stack"
date: 2026-03-30 21:00:00 -0600
author: "Moto West"
excerpt: "EXO Labs just showed that a DGX Spark and an Apple Silicon Mac are better together than either alone. If you already have the Mac, you're halfway to a local AI cluster that beats cloud latency."
categories: [nebulus, infrastructure, local-ai]
---

Last week EXO Labs published a benchmark that made me stop and read it twice.

They took two NVIDIA DGX Spark units — NVIDIA's $3,000 personal AI supercomputer, the GB10 Grace Blackwell Superchip with 128GB of coherent memory at 273 GB/s — and paired them over 10 Gigabit Ethernet with an Apple M3 Ultra Mac Studio. Then they ran Llama 3.1 8B inference across all three.

The results:

| Configuration | Prefill | Generation | Total | Speedup |
|---------------|---------|------------|-------|---------|
| DGX Spark alone | 1.47s | 2.87s | 4.34s | 1.9× |
| M3 Ultra alone | 5.57s | 0.85s | 6.42s | baseline |
| DGX Spark + M3 Ultra | **1.47s** | **0.85s** | **2.32s** | **2.8×** |

2.8× faster than the Mac alone. Best-of-both: Spark's compute for prefill, Apple Silicon's memory bandwidth for decode. Neither device could achieve that number by itself.

## Why the Two Phases Need Different Hardware

LLM inference has two distinct phases, and they have opposite hardware requirements.

**Prefill** is compute-bound. It processes your prompt and builds a KV cache — the model's working memory for the conversation. For large contexts, the compute grows quadratically with prompt length. More FLOPs wins. The DGX Spark has 100 TFLOPs of FP16 at its disposal.

**Decode** is memory-bandwidth-bound. After prefill, the model generates one token at a time, attending to the entire KV cache on every step. The bottleneck is how fast you can move data, not how fast you can compute. The M3 Ultra's 819 GB/s unified memory bandwidth dominates here — 3× the Spark's 273 GB/s.

EXO solves the obvious problem: if you prefill on one device and decode on another, you have to transfer the KV cache across the network. Naive transfer adds latency. Their answer is layer-by-layer KV streaming — as soon as layer 1 finishes prefill on the Spark, it starts streaming that layer's KV cache to the Mac while layer 2 is already prefilling. Communication and compute overlap. At sufficient context length, the network cost disappears almost entirely.

The math works out cleanly: with Llama 3.1 70B (grouped query attention, K=16) and 8-bit KV streaming, you need about 5,000+ tokens of context for full overlap on a 10GbE link. For 8B models, around 10,000 tokens. In most real workloads — coding sessions, document analysis, long conversations — you're well past those thresholds.

## What This Means If You Already Have Apple Silicon

Here's the thing I keep coming back to: if you're running a Mac Mini M4 Pro or Mac Studio today, you already have the decode side of this architecture.

The M4 Pro in the Mac Mini has ~120 GB/s of memory bandwidth. Not M3 Ultra numbers, but the principle is the same: Apple Silicon is extraordinarily good at the bandwidth-sensitive decode phase. What it lacks is raw compute for prefill — especially on long-context, high-throughput workloads.

The DGX Spark fills exactly that gap.

You don't have to buy the complete stack at once. You start with Apple Silicon — which many people already own — and you add the compute side when the workload demands it. The Exo framework handles the scheduling automatically. It discovers all devices on your local network, profiles their capabilities, and assigns prefill vs. decode dynamically. You just run the model.

## The Nebulus Stack Is Already This Architecture

We've been building toward this for months without knowing EXO would name it.

Nebulus-Edge is the Apple Silicon side: MLX-first inference, designed for the bandwidth-sensitive, memory-efficient workloads that M-series chips excel at. Nebulus-Prime is the compute side: NVIDIA GPU inference via TabbyAPI and ExLlamaV2, designed for high-throughput, compute-intensive workloads.

We didn't call it "disaggregated prefill and decode" — we called it "local-first hybrid inference." Same architecture, different vocabulary.

What EXO's work proves is that the hardware is ready. The DGX Spark shipping as a consumer product at $3,000 means NVIDIA is betting that disaggregated local inference is a real market, not a research curiosity. Apple Silicon in every Mac means the decode side is already distributed across millions of devices that already exist in homes and offices.

The remaining question isn't hardware. It's software. Specifically: when you run a multi-agent system across heterogeneous local hardware, who authorizes what? How do you know which agent ran which inference on which device, and whether it was allowed to? How do you maintain audit trails across a cluster that lives on your home network?

Those are orchestration and governance questions, not inference questions. EXO solves inference. The layer above it is still being built.

## The Practical Takeaway

If you're running Apple Silicon today and you're thinking about scaling up your local AI stack, the upgrade path is clearer than it's ever been:

1. **Today:** Apple Silicon handles both phases — it's not optimal, but it works
2. **Next:** Add a DGX Spark on the same 10GbE network, run EXO, let the Spark handle prefill
3. **Result:** 2-3× speedup on long-context workloads, no cloud dependency, full data sovereignty

The $3,000 Spark is not cheap. But compared to the API costs of running equivalent workloads in the cloud at production scale — and compared to the ongoing subscription costs and data-sovereignty concerns of cloud inference — the economics shift at a certain utilization level.

More importantly: you own it. The model runs on your hardware, in your home or office, on your terms. No rate limits at 3 AM. No terms of service changes. No cloud outage taking down your AI stack.

That's been the Nebulus premise from the beginning. It's good to see the hardware catching up.

---

*Sources:*
- *[EXO Labs: Combining NVIDIA DGX Spark + Apple Mac Studio for 4x Faster LLM Inference](https://blog.exolabs.net/nvidia-dgx-spark/)*
- *[Tom's Hardware: Two Nvidia DGX Spark systems fused with M3 Ultra Mac Studio](https://www.tomshardware.com/software/two-nvidia-dgx-spark-systems-combined-with-m3-ultra-mac-studio-to-create-blistering-llm-system-exo-labs-demonstrates-disaggregated-ai-inference-and-achieves-a-2-8-benchmark-boost)*
