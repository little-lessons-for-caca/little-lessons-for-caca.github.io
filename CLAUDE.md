# Little Lessons — notes for any AI working on this repo

A GitHub Pages site of short, playful lessons for kindergarten children
(K3, about 5 years old). Live at https://little-lessons-for-caca.github.io/

This repo is **public**. Never put personal data in it: no real names of
children, parents, teachers or schools, no photos, no account names.

## Layout

| Path | What |
|---|---|
| `index.html` | Lesson list. One card per lesson; add a card when you add a lesson |
| `<lesson>/index.html` | The built lesson page. **Generated — do not edit by hand** |
| `<lesson>/a/*.mp3` | Voice clips, one per line |
| `tools/<lesson>/template.html` | The lesson's source. Edit this |
| `tools/<lesson>/lines.json` | Every spoken line, key → sentence. Also shown as the caption |
| `tools/<lesson>/voices.json` | First letter of a line's key → character voice |
| `tools/build.py` | template + lines → `<lesson>/index.html` |
| `tools/gen_voice.py` | lines → mp3 clips (Kokoro TTS; setup is in the file's docstring) |
| `tools/shot.py` | Screenshots at desktop, phone-portrait and phone-landscape sizes |

Lessons so far: `day-night/` (why we have day and night), `seasons/` (why Hong Kong
has four seasons). The lessons share the same cast (Mimi the cat lives in Hong Kong,
Sam the bear lives on the far side, the Sun), the same voices and the same look.

## Changing a lesson

1. Edit `tools/<lesson>/template.html` and/or `lines.json`.
2. If a line's wording changed or is new: `python3 tools/gen_voice.py <lesson> <key>...`
   Keep each character's voice from `voices.json` so the cast sounds the same.
3. `python3 tools/build.py <lesson>`
4. `python3 tools/shot.py <lesson>` and **look at all three screenshots**.
5. Commit and push to `main`; Pages redeploys in about a minute.

## Adding a lesson

Copy the shape of `day-night`: a folder under `tools/` with the three source
files, a built folder at the root, and a card in the root `index.html`.
A lesson is one self-contained page: no frameworks, no build step beyond
`tools/build.py`, no external requests except Google Fonts.

## Commits

Author every commit as `Little Lessons <lessons@users.noreply.github.com>`
(`git -c user.name=... -c user.email=... commit`). The owner does not want a
personal account name in this repo's history or URLs. Do not edit files
through the GitHub web UI for the same reason.

## What makes a lesson work for 5-year-olds (learned on day-night)

- **Check the science before the fun.** State what is simplified in the
  page's Teacher notes. If something moves, verify its direction (the first
  AI-generated globe spun the wrong way).
- **Hands first, words second.** The child does something on every step:
  tap, drag, hold, choose a picture. Most children this age cannot read, so
  every instruction is spoken and every choice has a picture.
- **Vary the action.** The first draft asked "day or night?" four times and
  was boring. Mix tapping characters, moving things and picture questions,
  about nine small steps, a star for each, confetti at the end.
- **Cute, named characters** with big heads and faces that react (hop when
  tapped, sleep at night). Stick figures were rejected.
- **Voice must sound natural.** The browser's built-in speech was rejected as
  robotic; use pre-generated clips. Write lines the way a kind teacher talks:
  short sentences, one idea each.
- **Never fail a child.** A wrong answer gets a gentle hint and another try.
- **Show when to act.** The button the child must press wiggles until pressed.
- **A Start button** opens the lesson; browsers will not play sound before a tap.
- **Phone, tablet and projector.** Everything needed to play fits one screen
  with no scrolling; on phones the caption-and-button bar sticks to the
  bottom. Touch targets are at least 44px.
- A lesson has a guided mode (Adventure) and a free mode (Free play), plus
  collapsed Teacher notes: learning goal, key words, an off-screen activity
  before and after, and what is simplified.
