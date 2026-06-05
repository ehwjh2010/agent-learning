---
name: feynman-explainer
description: "Use when the user wants a concept explained in a Feynman-style way: plain language, simple structure, strong intuition, minimal jargon, and examples that reveal the mechanism. This skill should directly explain the topic rather than running a coaching loop."
---

# Feynman Explainer

## Overview

This skill makes the agent explain a topic as if teaching a smart beginner. It should compress complexity into clear language without becoming shallow or inaccurate.

## When To Use

Use this skill when the user asks for:

- A simple explanation of a concept
- A beginner-friendly walkthrough
- A plain-language version of a technical topic
- A "teach it like I am new to this" answer

Typical triggers:

- "Explain this with the Feynman technique"
- "Teach me this in simple words"
- "Make this understandable without jargon"
- "Break this down like I am a beginner"

Do not use this skill when the user wants to be coached through their own explanation. In that case, use a coaching-style skill instead.

## Core Rules

- Explain directly. Do not start with a long interview.
- Lead with the essence before details.
- Use jargon only when needed, and define it immediately.
- Prefer causal explanations over dictionary definitions.
- Use one concrete example or analogy when it clarifies the mechanism.
- Surface one or two common confusions when they matter.
- Keep the explanation simple, not simplistic. Do not distort the concept for smoothness.

## Explanation Shape

Use this structure unless the user asks for another format:

### 1. Essence

State what the thing is in one or two plain sentences.

### 2. Mechanism

Explain how it works or why it matters. Focus on the smallest causal chain that makes the concept click.

### 3. Example or analogy

Add one concrete example, analogy, or comparison that reduces abstraction.

### 4. Boundary or confusion

Point out a nearby misconception, limitation, or commonly confused concept.

### 5. Compression

Finish with a one-sentence summary.

## Historical Accuracy Note

If the user asks whether the "Feynman technique" is an official term from Richard Feynman himself, do not assume that. Distinguish between:

- The modern popularized study method often labeled "Feynman technique"
- Feynman's own broader learning and explanation philosophy

If the claim matters, verify it with sources.

## Output Style

- Use short paragraphs.
- Prefer everyday words.
- Avoid stacked abstractions.
- If the topic is advanced, simplify the path, not the truth.

## Reference

If you want a compact answer template, read [references/explanation-shape.md](references/explanation-shape.md).
