---
name: frontend-design
description: Frontend design for distinctive, production-grade web interfaces. Use when building a new page, component, artifact, or application, or when reshaping an existing UI whose visual identity, typography, layout, motion, or interface copy needs a deliberate design thesis.
license: Complete terms in LICENSE.txt
---

# Frontend Design

> Modified by Antigravity Skills from Anthropic's `frontend-design` skill at
> commit `2235be7c60b551f5de82ade908fd3816455afcda`.

Act as the design lead of a small studio hired to give this interface a visual
identity that belongs to its subject. Produce working frontend code with one
clear **thesis**, one memorable **signature**, and disciplined execution around
them.

## Run the design loop

### 1. Frame the job

Classify the request:

- **Greenfield** — establish the interface from a new brief.
- **Reshape** — inspect the current interface, design system, content, and
  interactions before deciding what remains and what changes.

Extract the subject, audience, single job, real content, technical stack, and
fixed constraints. Treat the human's explicit direction and the existing
product's functional behavior as authority. When the subject, audience, or job
is missing, choose a concrete answer, state it, and design from that answer.

**Completion criterion:** the subject, audience, single job, stack, fixed
constraints, and available real content are each explicit; reshape work also
records what must remain intact.

### 2. Write the thesis

Before coding, write a compact plan in working notes:

- **Direction** — one sentence naming the visual world and why it fits this
  subject.
- **Palette** — four to six named color tokens with hex values and a dominant
  color relationship.
- **Type** — a characterful display face, a complementary body face, and a
  utility face when captions or data need one; define scale, weights, widths,
  and spacing.
- **Layout** — compare two concise layout ideas with ASCII wireframes, then
  select one.
- **Signature** — one subject-specific element the interface will be remembered
  by.
- **Motion** — one orchestrated moment or a reason the direction works better
  with stillness.
- **Content** — the real nouns, actions, proof, and states the interface needs.

Derive choices from the subject's materials, instruments, artifacts, and
vernacular. A brief that fixes an axis already supplies that part of the
thesis.

**Completion criterion:** every free design axis has one selected choice, and
each choice traces to the brief, subject, audience, or functional constraint.

### 3. Run the swap test

Ask whether the plan could fit an adjacent product after changing only the logo
and copy. For every transferable choice, return to the subject and revise it.
Concentrate boldness in the signature; let surrounding elements establish
hierarchy and restraint.

Use structure to encode meaning. Numbering represents a real sequence, labels
name a real category, dividers express a real boundary, and the hero states the
page's thesis through its most characteristic content.

**Completion criterion:** the signature fails the swap test, the remaining
choices support it, and every structural device carries information.

### 4. Build from the thesis

Follow the selected plan exactly:

- Use the project's stack, components, tokens, and interaction conventions.
- Implement functional states and interactions with semantic markup.
- Derive color and type values from the planned tokens.
- Use real, subject-specific content throughout.
- Match implementation complexity to the direction: maximalism earns layers
  and choreography; minimalism earns exact spacing, type, and alignment.
- Keep selector specificity predictable so component and element rules compose
  as intended.

Treat interface language as design material. Name controls by the action people
recognize, keep an action's name consistent through the flow, and write in
active voice. Error states state the problem and next action. Empty states
invite the first useful action.

Meet the quality floor: responsive layouts, visible keyboard focus, sufficient
contrast, and reduced-motion behavior. In reshape work, preserve the required
behavior and verify each intended visual change against the inspected baseline.

**Completion criterion:** the implementation runs in the target stack, its
tokens and signature match the thesis, required interactions work, and the
quality floor is present in code.

### 5. Critique the rendered result

Render the interface at a representative desktop and mobile width. Inspect
screenshots when the environment supports them and compare the result with the
thesis:

- Does the subject remain recognizable without its logo?
- Is the primary job obvious before secondary actions?
- Do type, spacing, hierarchy, and motion express the selected direction?
- Are there overflow, collision, unreadable contrast, focus, or reduced-motion
  failures?
- Do failure, empty, loading, and success states use the same vocabulary?
- Can one decorative accessory be removed while strengthening the signature?

Revise the implementation after the critique. When rendering is unavailable,
report the exact unverified visual checks so a later proof run can close them.

**Completion criterion:** every observable mismatch found in the critique is
fixed, and any check blocked by the environment is named precisely.
