# AIWebTutor

A free study companion for **Principles of Data Science** (module code
`MEC7144CEM`, MSc Data Science, Middle East College) — built with
[Streamlit](https://streamlit.io).

Live app: https://aiwebtutor.streamlit.app

This app is entirely static content served by Streamlit: no external API
calls, no API keys, no secrets to configure. It costs nothing to run and
nothing to share, no matter how many students use it.

## Features

- **Overview** — module objectives, learning outcomes, assessment structure, and reading list.
- **Syllabus Explorer** — all 5 units (linear algebra, applied linear algebra & probability, probability distributions, data wrangling & EDA, statistical modelling) with topics and key terms, each linking to its hands-on lab.
- **Linear Algebra Lab** (Unit 1 & 2) — live matrix explorer (rank, determinant, eigenvalues/eigenvectors), independence/basis/orthogonality checker, and a least-squares fit tool — all editable via `st.data_editor`.
- **Probability Lab** (Unit 2 & 3) — Bayes' theorem calculator, a Binomial/Poisson/Normal distribution explorer, and a Law-of-Large-Numbers coin-flip simulator.
- **Data Wrangling & EDA Lab** (Unit 4) — a built-in messy sample dataset (duplicates, missing values, inconsistent text) to clean interactively, descriptive statistics and a correlation matrix, and a PCA explorer — or upload your own CSV.
- **Statistical Modelling Lab** (Unit 5) — simple linear regression with R² and residual plots, logistic regression with a live confusion matrix, and hypothesis testing (two-sample t-test and one-way ANOVA).
- **Practice Quiz** — 31 multiple-choice questions across all 5 units with instant scoring and explanations.
- **Assessment Prep** — maps each graded assessment (Individual Assignment, Portfolio, Practical Test) to the units it draws on, plus a random-question drill.

All labs run entirely on NumPy/Pandas/SciPy computed locally in the app —
nothing is sent anywhere, so there's nothing that can generate a bill.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

No setup beyond that — no secrets file, no API key.

## Deploying on Streamlit Community Cloud

1. Push this repo to GitHub (already done if you're reading this on GitHub).
2. On [share.streamlit.io](https://share.streamlit.io), point a new (or existing) app at this repo, branch `main`, main file `app.py`.
3. Save — that's it. No Secrets panel needed.

## Sharing with a class

Just send students the app link. There's no login, no access code, and
nothing that can generate a bill — every page is static content computed
locally in the app.

## Project structure

```
app.py                    # Streamlit UI and page routing
syllabus_data.py          # Module/unit content — single source of truth
quiz_data.py              # Practice quiz question bank, keyed by unit (31 questions)
linear_algebra_lab.py     # Unit 1 & 2 hands-on lab
probability_lab.py        # Unit 2 & 3 hands-on lab
data_wrangling_lab.py     # Unit 4 hands-on lab
stat_modelling_lab.py     # Unit 5 hands-on lab
requirements.txt
```

## Updating the syllabus content

All course content lives in `syllabus_data.py` and `quiz_data.py` as plain
Python data structures — edit those files to add units, change assessment
weightings, or add more quiz questions.
