# AIWebTutor

A free study companion for **Principles of Data Science** (module code
`MEC7144CEM`, MSc Data Science, Middle East College) -- built with
[Streamlit](https://streamlit.io).

Live app: https://aiwebtutor.streamlit.app

This app is entirely static content served by Streamlit: no external API
calls, no API keys, no secrets to configure. It costs nothing to run and
nothing to share, no matter how many students use it.

## Features

- **Overview** -- module objectives, learning outcomes, assessment structure, and reading list.
- **Syllabus Explorer** -- all 5 units (linear algebra, applied linear algebra & probability, probability distributions, data wrangling & EDA, statistical modelling) with topics and key terms.
- **Practice Quiz** -- multiple-choice questions per unit with instant scoring and explanations.
- **Assessment Prep** -- maps each graded assessment (Individual Assignment, Portfolio, Practical Test) to the units it draws on, plus a random-question drill.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

No setup beyond that -- no secrets file, no API key.

## Deploying on Streamlit Community Cloud

1. Push this repo to GitHub (already done if you're reading this on GitHub).
2. On [share.streamlit.io](https://share.streamlit.io), point a new (or existing) app at this repo, branch `main`, main file `app.py`.
3. Save -- that's it. No Secrets panel needed.

## Sharing with a class

Just send students the app link. There's no login, no access code, and
nothing that can generate a bill -- every page is static content computed
locally in the app.

## Project structure

```
app.py               # Streamlit UI and page routing
syllabus_data.py      # Module/unit content -- single source of truth
quiz_data.py          # Practice quiz question bank, keyed by unit
requirements.txt
```

## Updating the syllabus content

All course content lives in `syllabus_data.py` and `quiz_data.py` as plain
Python data structures -- edit those files to add units, change assessment
weightings, or add more quiz questions.
