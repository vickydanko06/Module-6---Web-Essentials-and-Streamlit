"""
L8 — Personal Stats Dashboard  (STARTER)
==========================================
Run with:
    streamlit run solution.py

Your goal: build a wide-layout dashboard with sidebar controls,
metrics, tabs, and an expander.

Required features:
    1. st.set_page_config(layout="wide")
    2. Sidebar with at least 2 control widgets (selectbox, radio, etc.)
    3. 3-column metrics row using st.metric() — include delta values
    4. 2 tabs: "Overview" and "Details"
    5. 1 expander with extra content (raw data, methodology, etc.)
    6. Data can be hardcoded

Layout concepts:
    st.set_page_config(layout="wide")  — expands to full browser width
    st.sidebar.*                       — everything here goes in the sidebar
    col1, col2, col3 = st.columns(3)   — 3 equal columns; use `with col1:`
    st.metric(label, value, delta)     — big number + arrow; delta can be a string
    tab1, tab2 = st.tabs(["A", "B"])   — tabbed sections; use `with tab1:`
    with st.expander("Title"):         — collapsible section

When to use tabs vs expanders:
    Tabs      → mutually exclusive views (Overview vs Details)
    Expanders → optional detail that most users won't need
"""

import streamlit as st

# ── Step 1: Page config ────────────────────────────────────────────────────
# TODO: Call st.set_page_config with layout="wide", a title, and an icon
# This must be the FIRST Streamlit call in the script.

st.set_page_config(page_title= "My Dashboard",page_icon="🚥", layout="wide")

# ── Step 2: Hardcoded data ────────────────────────────────────────────────
# TODO: Create some data to display.
# Suggestions:
#   WEEKLY_STUDY = {"Mon": 1.5, "Tue": 2.0, ...}
#   MODULES = {"Module 1": {"score": 88, "status": "Complete"}, ...}
#   SKILLS  = {"Python": 90, "SQL": 75, ...}

WEEKLY_STUDY = {"Mon": 1.5,"Tue": 2.0, "Wed": 2.5,"Thurs":1.5,"Fri": 0, "Sat": 4.0,"Sun":1.5}
MODULES={"Module 1":{"score":88, "status":"Complete"}, "Module 2":{"score":90, "status":"Complete"},"Module 3":{"score":71, "status":"Complete"}}
SKILLS = {"Python": 90,"SQL":75, "Rest API": 70, "Fast API": 77}


# ── Step 3: Sidebar controls ──────────────────────────────────────────────
# TODO: Use `with st.sidebar:` to add:
#   - st.header("Dashboard Controls")
#   - A selectbox (e.g., choose a module to focus on)
#   - A radio button (e.g., choose chart type)
with st.sidebar:
    st.header("Dashboard Controls")
    module_select = st.selectbox("Module Selection",list(MODULES.keys()))
    chart_select = st.radio("What chart type would you like to use",["Bar","line"])


# ── Step 4: Page title ────────────────────────────────────────────────────
# TODO: st.title() and st.caption()
st.title("Dashboard 6_9")
st.caption("Viewing Dash")


# ── Step 5: Metrics row ───────────────────────────────────────────────────
# TODO: Create 3 columns: col1, col2, col3 = st.columns(3)
# In each column, display a st.metric() with a label, value, and delta.
# Example:
#   with col1:
#       st.metric("Study Hours", "10.5 hrs", "+1.5 hrs vs last week")
col1, col2, col3 =st.columns(3)

with col1:
    st.metric("Study Hours","13.0 hrs","+1.5 hrs vs last week")
with col2:
    st.metric("Avg Score","83%","+5%")
with col3:
    st.metric("Skills","4","+1")


# ── Step 6: Tabs ──────────────────────────────────────────────────────────
# TODO: Create 2 tabs: "Overview" and "Details"
# tab_overview, tab_details = st.tabs(["📈 Overview", "📋 Details"])
tab_overview, tab_details = st.tabs(["📈 Overview", "📋 Details"])
#
# In tab_overview:
#   - st.subheader and a chart (st.bar_chart / st.line_chart)
with tab_overview:
    st.subheader("Weekly Study Hours")

    if chart_select == "Bar":
        st.bar_chart(WEEKLY_STUDY)
    else:
        st.line_chart(WEEKLY_STUDY)

    st.subheader("Skills Progress")
    st.bar_chart(SKILLS)
# In tab_details:
#   - Module progress table or list
#   - An st.expander with raw data or methodology notes
with tab_details:
    st.subheader("Module Progress")

    for module, details in MODULES.items():
        st.write(
            f"{module} — Score: {details['score']}% "
            f"| Status: {details['status']}"
        )

    
# ── Step 7: Expander ──────────────────────────────────────────────────────
# TODO: Inside the Details tab (or below), add:
#   with st.expander("Raw Data & Methodology", expanded=False):
#       st.json(your_data)
#       st.markdown("Explanation of how values are calculated...")
with st.expander("Raw Data & Methodology", expanded=False):
        st.subheader("Raw Data")

        st.json({
            "Weekly Study Hours": WEEKLY_STUDY,
            "Modules": MODULES,
            "Skills": SKILLS
        })

        st.markdown("""
        **Methodology**

        - Study hours represent the total hours studied each day.
        - Module scores are recorded as percentages.
        - Skill scores represent skill proficiency percentages.
        """)