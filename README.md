# Build-a-Voice

> **Tri-Platform Agent Skill** for Claude Desktop / Code, Grok CLI, and Google Antigravity / Gemini.  
> Local Kokoro TTS Persona Blender — Design a custom offline Kokoro TTS voice persona: blend base voices by ratio, save personas, and synthesize speech locally.

---

## Overview

`build-a-voice` provides standardized capabilities across conversational AI platforms:
- Local Kokoro ONNX model and voices.bin support (B:\AI Directories_Databases\models\kokoro).
- 11 base voice catalog and multi-voice linear blending by weight ratio.
- Named persona profile saving and retrieval system.
- Speed tuning, en-us / en-gb language hints, and WAV generation.
- Tri-platform NTFS junctions connecting Claude, Grok, and Antigravity.
- Standard documentation suite: SKILL.md, HOW_TO_USE.txt, IMPLEMENTATION_PLAN.md, and README.md.

---

## Tri-Platform Architecture

Zero duplicate code across platforms. Canonical source resides in `.agents`:
- **Canonical Source**: `C:\Users\<you>\.agents\skills\build-a-voice`
- **Claude**: `C:\Users\<you>\.claude\skills\build-a-voice` (NTFS Junction)
- **Grok**: `C:\Users\<you>\.grok\skills\build-a-voice` (NTFS Junction)
- **Antigravity**: `C:\Users\<you>\.gemini\config\skills\build-a-voice` (NTFS Junction)

---

## Documentation Suite

- [`HOW_TO_USE.txt`](HOW_TO_USE.txt): Standardized user guide and prompt templates.
- [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md): Feature checklist and roadmap.
- [`App Changes Tracker.html`](App%20Changes%20Tracker.html): Interactive visual version log.
- [`SKILL.md`](SKILL.md): Agent system instructions and triggers.
