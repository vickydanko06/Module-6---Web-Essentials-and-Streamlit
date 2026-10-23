"""
L7 — Streamlit Exploration App  (STARTER)
===========================================
Run with:
    streamlit run solution.py

Your goal: build an interactive app called "Python Learning Journey" that
uses 5+ widget types and shows content that changes based on widget values.

KEY CONCEPT — The re-run model:
    Every time a user interacts with a widget, Streamlit re-executes the
    ENTIRE script from top to bottom. This means:
      • Widget functions (st.slider, st.selectbox, etc.) both RENDER the
        widget AND RETURN the current value in the same call.
      • Just use the returned value immediately — no event handlers needed.
      • Write code like a normal top-to-bottom Python script.

Widgets to use (at least 5):
    st.slider()       — returns a number (int or float)
    st.selectbox()    — returns one item from a list
    st.radio()        — returns one item from a list (shown as radio buttons)
    st.multiselect()  — returns a list of selected items
    st.text_input()   — returns a string
    st.checkbox()     — returns True or False
"""

import streamlit as st

# ── Page configuration ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Python Learning Journey",
    page_icon="🐍",
    layout="centered",
)

st.title("🐍 Python Learning Journey")
st.caption("Adjust the widgets to explore your progress and learning path.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# Widget 1 — st.slider
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("1. Experience Level")
# TODO: Create a slider asking "How many weeks have you been coding?"
#       min_value=0, max_value=52, value=8, step=1
#       Store the result in `weeks`
weeks = st.slider("How many weeks have you been coding?",min_value=0,max_value=52, value=8,step=1)


# TODO: Use weeks to determine a level label (Beginner / Intermediate / Advanced)
if weeks <= 17:
    level_label = "Beginner"
elif weeks <=34:
    level_label = "Intermediate"
else:
    level_label="Advanced"

# TODO: Display the level using st.metric()
# Hint: st.metric(label="...", value=level_label, delta=f"{weeks} weeks")

st.metric(
    label="Your experience level",
    value=level_label,
    delta=f"{weeks} weeks"
)
st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# Widget 2 — st.selectbox
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("2. Current Topic")
# TODO: Create a selectbox with at least 5 Python topics as options
#       Store the result in `topic`
topic = st.selectbox("Favorite Topic",["Rest API","Fast API","Streamlit","HTML/CSS","Python"])

# TODO: Show a topic-specific tip using st.info()
# Hint: use a dict to map topic → tip, then look up tips[topic]
tips={
    "Rest API":"Learn how APIs use HTTP methods like GET and POST to exchange data.",
    "Fast API": "Practice building API endpoints and validating data with Pydantic.",
    "Streamlit": "Build interactive apps using widgets such as sliders and selectboxes.",
    "HTML/CSS": "Learn HTML to structure web pages and CSS to style them.",
    "Python": "Practice variables, loops, functions, and dictionaries."
}
st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# Widget 3 — st.radio
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("3. Learning Style")
# TODO: Create radio buttons asking how the student learns best
#       Options: ["Reading docs", "Watching videos", "Building projects", "Pair programming"]
#       Use horizontal=True to display them in a row
#       Store the result in `style`
style=st.radio("What method of learning works the best for you",["Reading docs","Watching videos","Building projects","Pair Programming"],horizontal=True)

# TODO: Show a resource recommendation based on the selected style
if style == "Reading docs":
    st.info("Recommendation: Explore the official Python documentation at docs.python.org.")
elif style == "Watching videos":
    st.info("Recommendation: Find a Python tutorial on YouTube and follow along.")
elif style == "Building projects":
    st.info("Recommendation: Build a small project, such as a calculator or to-do list.")
elif style == "Pair Programming":
    st.info("Recommendation: Find a coding partner and solve Python challenges together.")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# Widget 4 — st.multiselect
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("4. Tools & Libraries You Use")
# TODO: Create a multiselect with tools: pandas, requests, FastAPI, Streamlit, SQLite, etc.
#       Set default=["requests", "Streamlit"]
#       Store the result in `selected_tools`
selected_tools = st.multiselect("What tools have you used?",["pandas","requests","FastAPI","Streamlit","SQLite"],default=["requests","Streamlit"])

# TODO: If tools are selected, list them with checkmarks
# TODO: If no tools selected, show st.warning()
if selected_tools:
    st.write("### Your selected tools")
    for tool in selected_tools:
        st.write(f"✅ {tool}")
else:
    st.warning("Please select at least one tool or library!")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# Widget 5 — st.text_input
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("5. Project Idea Generator")
# TODO: Create a text_input asking for a keyword (e.g. "weather", "fitness")
#       Store the result in `project_keyword`
project_keyword = st.text_input("What is your keyword", placeholder="e.g. weather,fitness,books")

# TODO: If a keyword is entered, generate 3-4 project ideas using that keyword
#       Hint: use an f-string like f"A {keyword} tracker that stores data in SQLite"
if project_keyword:
    st.write(f"### Project Ideas for: {project_keyword}")

    ideas = [f"A {project_keyword} tracker that stores data in SQLite",
        f"A {project_keyword} dashboard built with Streamlit",
        f"A {project_keyword} API built with FastAPI",
        f"A {project_keyword} app that fetches data using requests"]
# TODO: If empty, show a prompt to enter a keyword

    for idea in ideas:
        st.write(f"{idea}")
else:
        st.info("Enter a keyword above to generate your project ideas")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# Widget 6 — st.checkbox
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("6. Progress Summary")
# TODO: Create a checkbox labelled "Show my personalised learning summary"
#       Set value=True so it starts checked
#       Store the result in `show_summary`
show_summary = st.checkbox("Show my personalized learning summary",value=True)

# TODO: If show_summary is True, display a summary using all the widget values
#       collected above (weeks, topic, style, selected_tools, project_keyword)
# Hint: use st.success() with a multi-line f-string
if show_summary:
    st.success(
        f"""
        🎉 Your Python Learning Summary

        📅 Coding experience: {weeks} weeks

        📚 Current topic: {topic}

        🧠 Preferred learning style: {style}

        🛠️ Tools you use: {", ".join(selected_tools) if selected_tools else "None selected"}

        💡 Project keyword: {project_keyword if project_keyword else "Not entered yet"}

        Keep learning and building projects. You're making progress!
        """
    )