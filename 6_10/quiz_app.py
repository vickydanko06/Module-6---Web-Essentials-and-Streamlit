"""
L9 — Stateful Quiz App  (STARTER)
===================================
Run with:
    streamlit run solution.py

Your goal: build a 5-question multiple-choice quiz app that tracks state
across re-runs using st.session_state.

Required features:
    1. 5 hardcoded multiple-choice questions on course topics
    2. Session state tracking: current_question, score, answered
    3. Show the question and radio-button options
    4. Submit button → reveal right/wrong feedback
    5. Next button → advance to the next question
    6. Progress bar and "Question X of 5" indicator
    7. Results screen with final score and Restart button

Session state lifecycle:
    1. INITIALIZE — set defaults once with the pattern:
         if "key" not in st.session_state:
             st.session_state.key = default_value
    2. READ   — use st.session_state.key anywhere
    3. UPDATE — assign st.session_state.key = new_value
    4. RESET  — reassign all keys to defaults (Restart button)
"""

import streamlit as st


st.set_page_config(
    page_title="Quiz App",
    page_icon="📝",
    layout="centered"
)

# ── Step 1: Quiz data ──────────────────────────────────────────────────────
# TODO: Create a list called QUESTIONS with 5 dicts.
# Each dict should have:
#   "question"    : str  — the question text
#   "options"     : list — 4 answer choices
#   "answer"      : str  — must match exactly one of the options
#   "explanation" : str  — shown after the user answers
QUESTIONS = [
   {
        "question": "What is Python?",
        "options": [
            "A programming language",
            "An operating system",
            "A database",
            "A web browser"
        ],
        "answer": "A programming language",
        "explanation": "Python is a popular, high-level programming language."
    },
    {
        "question": "Which keyword defines a function in Python?",
        "options": ["func", "define", "def", "function"],
        "answer": "def",
        "explanation": "The def keyword is used to define a function in Python."
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["int", "str", "bool", "list"],
        "answer": "bool",
        "explanation": "The bool data type represents True or False."
    },
    {
        "question": "Which Python collection uses key-value pairs?",
        "options": ["List", "Tuple", "Set", "Dictionary"],
        "answer": "Dictionary",
        "explanation": "A dictionary stores data as key-value pairs."
    },
    {
        "question": "What does st.session_state do in Streamlit?",
        "options": [
            "Styles the page",
            "Stores data across reruns",
            "Creates a database",
            "Stops the application"
        ],
        "answer": "Stores data across reruns",
        "explanation": "st.session_state preserves values across Streamlit reruns for a user's session."
    }
]

# ── Step 2: Session state initialisation ──────────────────────────────────
# Use this pattern for EVERY piece of state:
#   if "key" not in st.session_state:
#       st.session_state.key = default_value
#
# This runs ONLY on the first load. On every re-run (after a widget
# interaction), session_state already has the key so the block is skipped.

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected" not in st.session_state:
    st.session_state.selected = None

if "show_results" not in st.session_state:
    st.session_state.show_results = False

# ── Step 3: Page config ───────────────────────────────────────────────────
# TODO: st.set_page_config and st.title



# ══════════════════════════════════════════════════════════════════════════
# RESULTS SCREEN
# Render when st.session_state.show_results is True
# ══════════════════════════════════════════════════════════════════════════
# TODO: if st.session_state.show_results:
#   - Calculate percentage score
#   - Show st.success / st.warning based on score
#   - Show st.progress(pct / 100)
#   - Show a Restart button that resets all session state keys
#   - Call st.stop() so the quiz below doesn't render
#   - Call st.rerun() after resetting state to refresh the page

# ══════════════════════════════════════════════════════════════════════════
# QUIZ SCREEN
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.show_results:
    st.title("Quiz Results")

    total_qs = len(QUESTIONS)
    pct = int(st.session_state.score / total_qs * 100)

    st.write(
        f"Your score: {st.session_state.score}/{total_qs}"
    )
    if pct >= 80:
        st.success("Excellent work!")
    elif pct >= 50:
        st.warning("Good effort! Keep practicing.")
    else:
        st.error("Keep practicing. You'll improve!")

    st.progress(pct / 100)

    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.selected = None
        st.session_state.show_results = False

        # Clear saved radio-button selections
        for i in range(len(QUESTIONS)):
            key = f"q_{i}"
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

    st.stop()
# TODO: Get the current question from QUESTIONS[st.session_state.current_q]
q_index = st.session_state.current_question
total_qs = len(QUESTIONS)

question_data = QUESTIONS[q_index]

# TODO: Show progress indicator: "Question X of 5"
st.title("Python Quiz")

st.write(f"Question {q_index + 1} of {total_qs}")
st.progress((q_index + 1) / total_qs)

st.subheader(question_data["question"])
# TODO: Show st.progress(q_index / total_qs)

# TODO: Show st.subheader with the question text

# TODO: Show st.radio with the answer options
#   - Use disabled=True after the user has submitted (st.session_state.answered)
#   - Give it a unique key per question: key=f"q_{q_index}"
#   - Store the selection in st.session_state.selected
selected = st.radio(
    "Choose your answer:",
    question_data["options"],
    key=f"q_{q_index}",
    disabled=st.session_state.answered
)

st.session_state.selected = selected

# TODO: If not yet answered: show a Submit button
#   - On click: set st.session_state.answered = True
#   - If correct: increment st.session_state.score
#   - Call st.rerun() to trigger a re-render showing feedback

# TODO: If answered: show feedback
#   - st.success if correct, st.error if wrong (show the correct answer)
#   - st.info with the explanation
#   - Show a Next / Finish button
#     - If last question: set show_results = True, call st.rerun()
#     - Otherwise: increment current_q, reset answered/selected, call st.rerun()
if not st.session_state.answered:
    if st.button("Submit Answer"):
        st.session_state.answered = True

        if st.session_state.selected == question_data["answer"]:
            st.session_state.score += 1

        st.rerun()

else:
    if st.session_state.selected == question_data["answer"]:
        st.success("Correct!")
    else:
        st.error(
            f"Incorrect! The correct answer is: "
            f"{question_data['answer']}"
        )

    st.info(question_data["explanation"])

    if st.button(
        "Finish Quiz" if q_index == total_qs - 1 else "Next Question"
    ):
        if q_index == total_qs - 1:
            st.session_state.show_results = True
        else:
            st.session_state.current_question += 1
            st.session_state.answered = False
            st.session_state.selected = None

        st.rerun()