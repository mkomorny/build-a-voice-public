# Example playthrough

What a finished Build-a-Voice result + write-up should look like.

---

**Request:** "Build me a gravelly noir detective voice and read this line:
'The rain hadn't stopped in three days, and neither had the questions.'"

**Command:**
```bash
python scripts/speak.py --blend "am_adam:0.7,bm_george:0.3" --speed 0.9 \
  --save-persona noir_detective \
  --text "The rain hadn't stopped in three days, and neither had the questions." \
  --out noir_line1.wav
```

**Write-up to the user:**

> Blended 70% Adam (American) with 30% George (British) and slowed it to
> 0.9x for a bit more weight — saved it as `noir_detective` so you can
> reuse the exact voice later. Here's the line: `noir_line1.wav`. Want it
> slower, a different blend ratio, or a second line in the same voice?

Then, later in the same conversation:

**Request:** "Give me another line in that same voice."

**Command:**
```bash
python scripts/speak.py --persona noir_detective \
  --text "She walked in like she already knew how this was going to end." \
  --out noir_line2.wav
```

---

Keep the write-up short: name the blend/persona used, mention anything
non-default (speed, saved name), point to the file, and offer an easy
follow-up (different ratio, different speed, another line). Don't narrate
the script's internals unless asked, and don't describe how a voice
*sounds* beyond what you can hear from a generated file.
