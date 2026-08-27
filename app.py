"""
AIWebTutor -- a free study companion for the Principles of Data Science
module (MEC7144CEM, MSc Data Science, Middle East College).

Run locally with:
    streamlit run app.py

Deployed on Streamlit Community Cloud at aiwebtutor.streamlit.app.
This app makes no external API calls and needs no secrets/API keys --
it is entirely static content served by Streamlit, so it costs nothing
to run no matter how many people use it.
"""

import random

import streamlit as st

from syllabus_data import MODULE_INFO, UNITS
from quiz_data import QUIZ_BANK

st.set_page_config(
    page_title="AIWebTutor - Principles of Data Science",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------- sidebar --
st.sidebar.title("📊 AIWebTutor")
st.sidebar.caption(f"{MODULE_INFO['code']} - {MODULE_INFO['title']}")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Overview", "📚 Syllabus Explorer", "📝 Practice Quiz", "🎯 Assessment Prep"],
    key="nav_page",
)
st.sidebar.divider()
st.sidebar.caption(
    f"{MODULE_INFO['programme']} - {MODULE_INFO['college']}\n\n"
    f"{MODULE_INFO['level']} - {MODULE_INFO['credit_hours']} credit hours/points"
)

# ------------------------------------------------------------- Overview ---
if page == "🏠 Overview":
    st.title("Principles of Data Science - Study Companion")
    st.write(MODULE_INFO["objectives"])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Learning Outcomes")
        for i, lo in enumerate(MODULE_INFO["learning_outcomes"], 1):
            st.markdown(f"**LO{i}.** {lo}")

    with col2:
        st.subheader("Assessment Structure")
        for a in MODULE_INFO["assessments"]:
            with st.container(border=True):
                st.markdown(f"**{a['name']}** - {a['weight']} - {a['duration']}")
                st.caption(a["description"])
        st.info(MODULE_INFO["pass_rule"])

    st.subheader("Recommended Reading")
    rcol1, rcol2 = st.columns(2)
    with rcol1:
        st.markdown("**Basic references**")
        for r in MODULE_INFO["references"]["basic"]:
            st.markdown(f"- {r}")
    with rcol2:
        st.markdown("**Recommended references**")
        for r in MODULE_INFO["references"]["recommended"]:
            st.markdown(f"- {r}")

# ------------------------------------------------------- Syllabus Explorer -
elif page == "📚 Syllabus Explorer":
    st.title("Syllabus Explorer")
    st.caption("Browse the module unit by unit.")

    for u in UNITS:
        with st.expander(f"Unit {u['id']}: {u['title']}", expanded=(u["id"] == 1)):
            st.markdown("**Topics covered:**")
            for t in u["topics"]:
                st.markdown(f"- {t}")
            st.markdown("**Key terms:** " + ", ".join(f"`{k}`" for k in u["key_terms"]))

# --------------------------------------------------------------- Quizzes --
elif page == "📝 Practice Quiz":
    st.title("Practice Quiz")
    unit_choice = st.selectbox(
        "Choose a unit",
        options=[u["id"] for u in UNITS],
        format_func=lambda uid: f"Unit {uid}: {next(u['title'] for u in UNITS if u['id'] == uid)}",
    )

    quiz_key = f"quiz_{unit_choice}"
    if quiz_key not in st.session_state:
        questions = QUIZ_BANK.get(unit_choice, [])
        st.session_state[quiz_key] = {
            "questions": questions,
            "answers": [None] * len(questions),
            "submitted": False,
        }

    quiz_state = st.session_state[quiz_key]
    questions = quiz_state["questions"]

    if not questions:
        st.info("No practice questions for this unit yet.")
    else:
        with st.form(key=f"form_{unit_choice}"):
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i + 1}. {q['question']}**")
                quiz_state["answers"][i] = st.radio(
                    "Select one:",
                    options=list(range(len(q["options"]))),
                    format_func=lambda idx, opts=q["options"]: opts[idx],
                    key=f"{quiz_key}_q{i}",
                    index=None,
                )
                st.write("")
            submitted = st.form_submit_button("Submit answers")
            if submitted:
                quiz_state["submitted"] = True

        if quiz_state["submitted"]:
            score = sum(
                1
                for i, q in enumerate(questions)
                if quiz_state["answers"][i] == q["answer_index"]
            )
            st.subheader(f"Score: {score} / {len(questions)}")
            for i, q in enumerate(questions):
                correct = quiz_state["answers"][i] == q["answer_index"]
                icon = "✅" if correct else "❌"
                with st.container(border=True):
                    st.markdown(f"{icon} **Q{i + 1}. {q['question']}**")
                    st.markdown(f"Correct answer: **{q['options'][q['answer_index']]}**")
                    st.caption(q["explanation"])

            if st.button("Try again"):
                del st.session_state[quiz_key]
                st.rerun()

# ---------------------------------------------------------- Assessment Prep
elif page == "🎯 Assessment Prep":
    st.title("Assessment Prep")
    st.caption(
        "A quick map from each assessment to the units and skills it draws on, "
        "so you know what to revise for each one."
    )

    mapping = {
        "Individual Assignment": [1, 2],
        "Portfolio": [4, 5],
        "Practical Test": [1, 2, 3, 4, 5],
    }

    for a in MODULE_INFO["assessments"]:
        with st.container(border=True):
            st.subheader(f"{a['name']} - {a['weight']} ({a['duration']})")
            st.write(a["description"])
            related_units = mapping.get(a["name"], [])
            if related_units:
                st.markdown(
                    "**Revise:** "
                    + ", ".join(
                        f"Unit {uid} ({next(u['title'] for u in UNITS if u['id'] == uid)})"
                        for uid in related_units
                    )
                )

    st.divider()
    st.subheader("Random review question")
    if st.button("🎲 Give me a random question"):
        all_qs = [(uid, q) for uid, qs in QUIZ_BANK.items() for q in qs]
        uid, q = random.choice(all_qs)
        st.session_state["_random_q"] = (uid, q)

    if "_random_q" in st.session_state:
        uid, q = st.session_state["_random_q"]
        st.markdown(f"*From Unit {uid}*")
        st.markdown(f"**{q['question']}**")
        with st.expander("Show answer"):
            st.markdown(f"**{q['options'][q['answer_index']]}**")
            st.caption(q["explanation"])
