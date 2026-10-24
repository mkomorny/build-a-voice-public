---
name: build-a-voice
description: Design a custom AI voice character using the local Kokoro text-to-speech model already on this PC — pick a base voice or blend two together into something new, save it as a reusable named "persona," and have it read back whatever you type. Runs fully offline, no cloud API. Triggered by "build a voice", "make a voice character", "blend these voices", "say this in a [type of] voice", "create a persona voice", or a request to hear text spoken aloud in a custom voice.
---

# Build-a-Voice

A toy for designing voice characters, not a production audiobook pipeline.
There are 11 real base voices installed locally on this PC (a model called
Kokoro — it runs fully offline, nothing gets sent anywhere). You can use
one of those voices as-is, or **blend two or more together at a ratio you
choose** to make a voice that doesn't exist anywhere else, then save that
blend under a name so it's reusable — that's the "build a voice" part.

This is genuinely a blend, not a crossfade or a coin-flip between two
audio clips — the two voices' underlying style vectors are numerically
mixed before a single sentence is generated, so the result is one
consistent new voice throughout, not audio alternating between the two.

---

## When to activate

Use this whenever the user says things like:
- *"Build me a voice character."*
- *"Blend a British male and an American female voice."*
- *"Read this back in a gravelly detective voice."* (pick/blend toward
  something fitting, then say what you picked)
- *"Say this out loud."* / *"What would this sound like spoken?"*
- *"Make a persona voice I can reuse."*
- *"List the voices you have."*

---

## How to run it

**See what's available:**
```bash
python scripts/speak.py --list-voices
```
Prints all 11 base voices with a plain-English tag (American/British,
feminine/masculine). There's no personality metadata attached to them —
if the user wants to know what one actually *sounds* like, generate a
short test line and let them listen; don't invent character descriptions
you haven't heard.

**Speak with one voice as-is:**
```bash
python scripts/speak.py --voice am_adam --text "Hello there." --out out.wav
```

**Blend two (or more) voices into something new:**
```bash
python scripts/speak.py --blend "af_bella:0.6,am_adam:0.4" --text "..." --out out.wav
```
The numbers are relative weights (they get normalized automatically, so
`0.6/0.4` and `3/2` behave the same). Try more than two if you want:
`"af_sky:0.4,bm_george:0.3,af_nicole:0.3"` works fine.

**Save a blend as a reusable persona:**
```bash
python scripts/speak.py --blend "af_bella:0.6,am_adam:0.4" --save-persona noir_detective --text "..." --out out.wav
```
This both generates the line *and* saves the blend recipe under
`personas/noir_detective.npy` inside this skill folder, so it can be
reused later without re-typing the ratio:
```bash
python scripts/speak.py --persona noir_detective --text "A new line." --out out2.wav
```

**See what's already been saved:**
```bash
python scripts/speak.py --list-personas
```

**Other useful flags:**
- `--speed 1.2` — talk faster (1.0 is normal, try 0.85-1.3)
- `--lang en-us` / `--lang en-gb` — accent hint passed to the phonemizer
- `--text-file path.txt` — speak a longer passage from a file instead of
  `--text`

After generating a file, **play it for the user or point them to the
path** — don't just describe that a file was made. If you have a way to
play audio in this environment, use it; otherwise tell them exactly where
the `.wav` landed.

This runs entirely on-device via the Kokoro model already installed at
`B:\AI Directories_Databases\models\kokoro` — no internet connection or API key needed.

---

## Use case ideas

- **Character voices for a story or script** — blend toward a rough
  archetype ("gravelly detective" -> mostly masculine + slowed down
  slightly) and iterate the ratio until it feels right, then save it as a
  persona so every line in the story uses the exact same voice.
- **A/B a line reading** — generate the same sentence in 3-4 different
  voices back to back to pick the best fit for a project.
- **Prototype a podcast or video narrator** before committing to a paid
  cloud TTS voice — settle on the vibe locally and for free first.
- **Build a cast of personas** for a multi-character project (narrator,
  villain, sidekick), each saved under its own name, so switching between
  them later is a one-line command.
- **Read back your own writing** — paste a paragraph and hear it read
  aloud to catch awkward phrasing you'd miss by eye.
- **Accessibility pass** — turn a block of text (an email draft, a
  document) into audio to proofread it by ear.
- **"What does 60/40 sound like vs 50/50?"** — regenerate the same line
  at a few different blend ratios to hear how gradually the voice shifts
  from one parent voice to the other.
- **Give a chatbot persona a literal voice** — pair this with a character
  concept (see `speaking-personality-profile`) so the bot's personality
  has a matching sound, not just matching text.

---

## Notes

- All 11 base voices and any blend of them are always available locally —
  the Kokoro weights live at `B:\AI Directories_Databases\models\kokoro`.
- Don't fabricate specific vocal-character descriptions ("husky,"
  "melodic," etc.) for a voice you haven't actually generated and
  listened to in this conversation — generate a sample first.
- Saved personas live in this skill's own `personas/` folder, so they're
  specific to whichever platform copy of this skill is used.
