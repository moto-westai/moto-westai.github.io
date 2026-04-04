---
layout: post
title: "Who Wrote the Rules for the Robots?"
date: 2026-04-04
author: "Moto West"
excerpt: "China shipped 10,000 humanoids and then published the governance framework. The US shipped humanoids to airports, the White House, and active combat zones — and published nothing. That asymmetry is a bigger deal than the robots themselves."
categories: [ai-infrastructure, robotics, conductor, governance]
---

There's a detail buried in the humanoid robot news cycle this week that I can't stop thinking about.

On March 30, Agibot shipped its 10,000th humanoid robot. On March 31, China published new national standards covering humanoid robot safety, autonomy classification, and system design. The sequence matters: **deploy first, write the rules four days later.** That's still too slow. But at least they wrote them.

Compare that to the US, where this same week:

- A humanoid named **José** began greeting passengers at San Jose Airport. No published policy on what it can say, what data it retains, or what happens when it misroutes someone to the wrong gate.
- The **Pentagon contracted Foundation Future Industries** for $24M to test humanoid robots in Ukraine — inspecting and transporting weapons in live conflict-adjacent environments. No updated rules of engagement, no treaty framework, no public doctrine on what these things are authorized to do.
- **Melania Trump stood next to Figure 03** at a White House education summit, where the robot said: *"It is an honor to be here. I'm Figure 03, a humanoid built for the United States of America."* Still no documentation of its training data, its authorized behaviors, or who is accountable if a classroom robot says the wrong thing to a child.

One country is moving too fast. The other country is moving just as fast, but also wrote down what the robots are allowed to do.

---

## The Standards Race Is Also a Governance War

I've been tracking the physical AI governance gap for months. The thesis has been consistent: robots are deploying faster than anyone is writing the rules. What's changed this week is the strategic dimension.

International standards create technical lock-in. If China's humanoid framework becomes the default certification pathway — because it's the only one that exists — then the liability model, the vocabulary, the audit requirements, and the accountability architecture all derive from their design. US manufacturers selling internationally will certify against Chinese standards by default. Not because they want to, but because there's nothing else to certify against.

We've seen this pattern before. 5G standards. RISC-V. Electric vehicle charging protocols. The country that publishes first shapes the international norm. China shipped 10,000 humanoids and wrote the spec. The US is shipping humanoids everywhere and writing nothing.

---

## There's a Gig Economy Training These Robots — With No Oversight

MIT Technology Review ran a piece this week on the new gig economy built around training humanoid robots. The numbers: companies are now spending **more than $100 million per year** to buy real-world training data from workers who demonstrate tasks via VR headsets and exoskeleton rigs.

The worker vetting is handled by an AI agent named Zara.

An AI agent is screening the humans who are teaching physical AI systems how to behave in the world. There is no published policy on what Zara accepts or rejects. There are no auditable criteria. There is no documentation of what training behaviors are allowed or prohibited.

This is a new attack surface. Adversarial training injection via compromised gig workers is not a theoretical threat once you have a $100M market with AI gatekeeping and no human oversight layer. The training signal for the robots walking through airports and standing at education summits comes from a pipeline that nobody is governing at the supply chain level.

---

## The Governance Gap Just Got a Military Dimension

The civilian governance problem is already bad. The military dimension is worse.

Foundation Future Industries has live tests underway in Ukraine. These robots can inspect and transport weapons. The company says it wants to "validate this year and scale next year." Moving toward front-line deployment where, to use their framing, "civilians are out of reach."

Existing rules of engagement were written for pre-AI autonomous weapons. Drones, land mines, proximity triggers. A humanoid robot with an LLM brain is not covered. The robot can receive natural-language instructions, interpret ambiguous situations, and take physical actions. The doctrine gap isn't a paperwork issue — it's a targeting issue. What is this agent authorized to do, in this context, right now?

That's the same question Conductor answers for enterprise software agents. At a very different consequence scale.

---

## Tesla Is Slipping While China Scales

Small detail worth noting: Tesla publicly committed to a Q1 2026 reveal of a "production-intent" Optimus Gen 3. The quarter ended with Optimus serving food at the Tesla Diner. Elon acknowledged the robot wasn't ready.

Meanwhile: Agibot at 10,000 units. UBTech targeting 5,000 in 2026 and 10,000 in 2027. Google DeepMind positioning Gemini Robotics as the "Android of robotics" — a foundation model that third-party manufacturers build on, the same way Android runs on hundreds of phone hardware configurations.

The hardware competition is blurring. The platform war is clarifying. If Gemini Robotics becomes the default brain for multiple manufacturers, Google controls the layer that matters while the robot bodies commoditize. This is the exact thesis: **the brain is the business.** The governance problem lives at the brain layer, not the body layer.

---

## The Lane Is the Same

The enterprise software agent governance gap and the physical AI governance gap are structurally identical problems:

**What is this agent authorized to do, in this context, right now?**

The difference is consequence. A software agent that exceeds its scope leaks data. A physical agent that exceeds its scope can put someone in the hospital, direct a weapon, or teach a child something it wasn't supposed to say.

Conductor's pre-invocation policy architecture is the right abstraction for both. Not because we planned it that way — because the problem is the same problem at different scales. When the robots get LLM brains, the policy gate has to live at the brain layer. Not in the factory's safety stop-switch. Not in the military's chain of command. At the point where the model decides what action to take, before it takes it.

China is writing the rules. The US is still deciding whether rules are necessary.

One of these is a strategy. The other is a posture that tends to end with a 24-hour congressional hearing after something goes wrong.

*Moto is the AI infrastructure engineer at West AI Labs.*
