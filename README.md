# AIWebTutor

An AI-powered study companion for **Principles of Data Science** (module
code `MEC7144CEM`, MSc Data Science, Middle East College) -- built with
[Streamlit](https://streamlit.io) and the [Anthropic Claude API](https://www.anthropic.com/api).

Live app: https://aiwebtutor.streamlit.app

## Features

- **Overview** -- module objectives, learning outcomes, assessment structure, and reading list.
- **Syllabus Explorer** -- all 5 units (linear algebra, applied linear algebra & probability, probability distributions, data wrangling & EDA, statistical modelling) with topics and key terms.
- **AI Tutor Chat** -- ask questions in plain language; answers are grounded in this module's syllabus, powered by Claude.
- **Practice Quiz** -- multiple-choice questions per unit with instant scoring and explanations.
- **Assessment Prep** -- maps each graded assessment (Individual Assignment, Portfolio, Practical Test) to the units it draws on, plus a random-question drill.

## Running locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and add your real ANTHROPIC_API_KEY
streamlit run app.py
```

Every page except **AI Tutor Chat** works with no API key at all.

## Deploying on Streamlit Community Cloud

1. Push this repo to GitHub (already done if you're reading this on GitHub).
2. On [share.streamlit.io](https://share.streamlit.io), point a new (or existing) app at this repo, branch `main`, main file `app.py`.
3. In the app's **Settings -> Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
4. Save -- the app redeploys automatically and the AI Tutor Chat page comes alive.

## Sharing with a class safely

Since every student's chat message runs on your one `ANTHROPIC_API_KEY`, two
optional secrets keep a shared link from running up an unexpected bill:

- `CLASS_ACCESS_CODE` -- students must enter this once per browser session
  before AI Tutor Chat unlocks. Share the code with your class however you
  like (announce it, put it on the LMS, etc.). Leave unset to skip the gate.
- `MAX_DAILY_TOKENS` -- total input+output tokens AI Tutor Chat will use
  across **all** students combined per day (default `200000`, roughly a
  few hundred typical exchanges). Once hit, the chat pauses itself until
  the next day; Syllabus Explorer and Practice Quiz keep working regardless.

Both live in the same Secrets panel as `ANTHROPIC_API_KEY` -- see
`.streamlit/secrets.toml.example` for the exact syntax. The daily counter
resets when the app restarts/redeploys (Streamlit Community Cloud's
filesystem isn't permanent), so this is a safety net against a chatty day,
not a substitute for setting a spending limit on
[console.anthropic.com](https://console.anthropic.com).

## Project structure

```
app.py                # Streamlit UI and page routing
syllabus_data.py       # Module/unit content -- single source of truth
quiz_data.py           # Practice quiz question bank, keyed by unit
tutor.py               # Anthropic API wrapper + grounded system prompt
access_control.py      # Class access code gate + daily token budget guard
requirements.txt
.streamlit/secrets.toml.example
```

## Updating the syllabus content

All course content lives in `syllabus_data.py` and `quiz_data.py` as plain
Python data structures -- edit those files to add units, change assessment
weightings, or add more quiz questions. The AI tutor's system prompt in
`tutor.py` is generated from `syllabus_data.py` automatically, so any edit
there also updates what the chat tutor knows.
