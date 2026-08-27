"""
AIWebTutor -- an AI-powered study companion for the Principles of Data
Science module (MEC7144CEM, MSc Data Science, Middle East College).

Run locally with:
    streamlit run app.py

Deployed on Streamlit Community Cloud at aiwebtutor.streamlit.app.
Set ANTHROPIC_API_KEY in the app's Secrets for the AI Tutor chat to work;
every other page works without it.
"""

import random

import streamlit as st

from syllabus_data import MODULE_INFO, UNITS
from quiz_data import QUIZ_BANK
import tutor

st.set_page_config(
    page_title="AIWebTutor - Principles of Data Science",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------- sidebar --
if st.session_state.pop("_switch_to_chat", False):
    st.session_state["nav_page"] = "💬 AI Tutor Chat"

st.sidebar.title("📊 AIWebTutor")
st.sidebar.caption(f"{MODULE_INFO['code']} - {MODULE_INFO['title']}")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Overview", "📚 Syllabus Explorer", "💬 AI Tutor Chat", "📝 Practice Quiz", "🎯 Assessment Prep"],
    key="nav_page",
)
st.sidebar.divider()
st.sidebar.caption(
    f"{MODULE_INFO['programme']} - {MODULE_INFO['college']}\n\n"
    f"{MODULE_INFO['level']} - {MODULE_INFO['credit_hours']} credit hours/points"
)

# ------------------------------------------------------------- Overview ---
if page == "🏠 Overview":
    st.title("Principles of Data Science - AI Study Companion")
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
            if st.button(f"Ask the AI Tutor about Unit {u['id']}", key=f"ask_unit_{u['id']}"):
                st.session_state["pending_question"] = (
                    f"Can you give me an overview of Unit {u['id']}: {u['title']}, "
                    f"and explain how its topics connect to the rest of the module?"
                )
                st.session_state["_switch_to_chat"] = True
                st.rerun()

# ----------------------------------------------------------- AI Tutor Chat -
elif page == "💬 AI Tutor Chat":
    st.title("AI Tutor Chat")

    if not tutor.is_configured():
        st.warning(
            "The AI Tutor isn't configured yet. Add an `ANTHROPIC_API_KEY` "
            "to this app's Streamlit Secrets to enable live chat answers.\n\n"
            "In the meantime, use **Syllabus Explorer** and **Practice Quiz** "
            "-- they work without an API key."
        )
    else:
        st.caption(
            "Ask about linear algebra, probability, data wrangling, EDA, or "
            "statistical modelling - answers are grounded in this module's syllabus."
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        pending = st.session_state.pop("pending_question", None)
        prompt = st.chat_input("Ask a question about the module...") or pending

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    reply = st.write_stream(tutor.stream_reply(st.session_state.messages))
                except Exception as e:
                    reply = (
                        "Sorry, I couldn't reach the AI tutor service just now "
                        f"({e}). Please try again in a moment."
                    )
                    st.error(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        if st.session_state.messages and st.button("Clear conversation"):
            st.session_state.messages = []
            st.rerun()

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
            cols = st.columns(len(related_units) or 1)
            for c, uid in zip(cols, related_units):
                with c:
                    if st.button(f"Quiz: Unit {uid}", key=f"prep_quiz_{a['name']}_{uid}"):
                        st.session_state["_jump_unit"] = uid
                        st.info("Head to **Practice Quiz** in the sidebar and pick this unit.")

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
