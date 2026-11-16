
"""
Module 6 Project — AI Dashboard
================================
Run with:
    streamlit run app.py

Features:
    1. Authentication
    2. Dashboard and data visualisation
    3. Task management
    4. AI chat with streaming mock responses
    5. Sidebar and tabs
"""

import streamlit as st
from mock_data import MOCK_TASKS, MOCK_STATS, MOCK_USER, MOCK_TOKEN
import api_client
import time


# ── Step 1: Page configuration ─────────────────────────────────────────────

st.set_page_config(
    layout="wide",
    page_title="AI Dashboard",
    page_icon="🤖"
)


# ── Step 2: Session state initialisation ───────────────────────────────────

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "use_mock" not in st.session_state:
    st.session_state.use_mock = False

if "tasks" not in st.session_state:
    st.session_state.tasks = [task.copy() for task in MOCK_TASKS]

if "ai_api_key" not in st.session_state:
    st.session_state.ai_api_key = ""

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a helpful AI assistant."
    )


# ── Helper functions ───────────────────────────────────────────────────────

def generate_mock_response(message):
    """Generate an offline response for the AI chat."""

    message = message.lower()

    if "fastapi" in message:
        return (
            "FastAPI is a modern Python framework for building APIs. "
            "It uses Python type hints and supports automatic validation."
        )

    elif "streamlit" in message:
        return (
            "Streamlit is a Python framework for building interactive "
            "web applications and dashboards."
        )

    elif "task" in message:
        return (
            "You can manage your tasks in the Tasks tab. "
            "You can add new tasks and mark existing tasks as complete."
        )

    elif "hello" in message or "hi" in message:
        return (
            "Hello! Welcome to your AI Dashboard. "
            "How can I help you today?"
        )

    elif "jwt" in message or "authentication" in message:
        return (
            "JWT stands for JSON Web Token. It is commonly used "
            "to securely authenticate users when accessing APIs."
        )

    else:
        return (
            "That's a great question! I'm your offline AI assistant. "
            "I can help you learn about Python, Streamlit, FastAPI, "
            "authentication, and task management."
        )


def stream_response(response):
    """Display a mock AI response one word at a time."""

    for word in response.split():
        yield word + " "
        time.sleep(0.03)


# ════════════════════════════════════════════════════════════════════════════
# SECTION A — AUTHENTICATION
# ════════════════════════════════════════════════════════════════════════════

if not st.session_state.token:

    st.title("🤖 AI Dashboard")
    st.subheader("Welcome! Please log in to continue.")

    with st.form("login_form"):

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        use_mock = st.checkbox("Use Mock Data (Offline Mode)")

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if login_button:

            if use_mock:
                st.session_state.token = MOCK_TOKEN
                st.session_state.username = MOCK_USER
                st.session_state.use_mock = True
                st.session_state.tasks = [
                    task.copy() for task in MOCK_TASKS
                ]

                st.success("Logged in using mock data!")
                st.rerun()

            elif username and password:

                token, error = api_client.login(
                    username,
                    password
                )

                if token:
                    st.session_state.token = token
                    st.session_state.username = username
                    st.session_state.use_mock = False

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error(error or "Login failed.")

            else:
                st.error(
                    "Please enter your username and password."
                )

    st.info(
        "Check 'Use Mock Data' to explore the dashboard "
        "without starting the FastAPI backend."
    )

    st.stop()


# ════════════════════════════════════════════════════════════════════════════
# SECTION B — SIDEBAR
# ════════════════════════════════════════════════════════════════════════════

with st.sidebar:

    st.title("🤖 AI Dashboard")

    st.divider()

    st.write(
        f"Logged in as **{st.session_state.username}**"
    )

    if st.session_state.use_mock:
        st.caption("🟢 Offline Mock Mode")
    else:
        st.caption("🔵 Live API Mode")

    if st.button("Logout", use_container_width=True):

        st.session_state.token = None
        st.session_state.username = None
        st.session_state.use_mock = False
        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.subheader("⚙️ AI Chat Settings")

    st.text_input(
        "AI API Key",
        type="password",
        key="ai_api_key"
    )

    st.text_area(
        "System Prompt",
        key="system_prompt"
    )

    st.divider()

    st.caption("Module 6 Project — Streamlit AI Dashboard")


# ════════════════════════════════════════════════════════════════════════════
# SECTION C — MAIN CONTENT (TABS)
# ════════════════════════════════════════════════════════════════════════════

st.title("🤖 Welcome to Your AI Dashboard")

st.write(
    "Manage your tasks, track your progress, "
    "and interact with your AI assistant."
)

tab_dash, tab_tasks, tab_chat = st.tabs([
    "📊 Dashboard",
    "✅ Tasks",
    "🤖 AI Chat"
])


# ── Load tasks ─────────────────────────────────────────────────────────────

if st.session_state.use_mock:

    tasks = st.session_state.tasks

else:

    api_tasks, error = api_client.get_tasks(
        st.session_state.token
    )

    if api_tasks is not None:
        st.session_state.tasks = api_tasks
    else:
        st.error(error or "Unable to load tasks.")
        st.warning("Showing previously loaded tasks.")

    tasks = st.session_state.tasks


# ── TAB 1: Dashboard ────────────────────────────────────────────────────────

with tab_dash:

    st.header("📊 Dashboard Overview")

    total_tasks = len(tasks)

    done_tasks = sum(
        1 for task in tasks if task.get("done", False)
    )

    pending_tasks = total_tasks - done_tasks

    # Metrics row

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Tasks",
        total_tasks
    )

    col2.metric(
        "Completed Tasks",
        done_tasks
    )

    col3.metric(
        "Pending Tasks",
        pending_tasks
    )

    st.divider()

    # Task dataframe

    st.subheader("📋 Task Overview")

    if tasks:

        st.dataframe(
            tasks,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No tasks available yet.")

    # Data visualisation

    st.subheader("📈 Task Completion Chart")

    if tasks:

        chart_data = {
            "Status": ["Completed", "Pending"],
            "Count": [done_tasks, pending_tasks]
        }

        st.bar_chart(
            chart_data,
            x="Status",
            y="Count",
            color="#4CAF50"
        )

        completion_rate = (
            done_tasks / total_tasks * 100
            if total_tasks > 0 else 0
        )

        st.write(
            f"Task completion rate: **{completion_rate:.1f}%**"
        )

    else:
        st.info("Add tasks to see your chart.")


# ── TAB 2: Tasks ────────────────────────────────────────────────────────────

with tab_tasks:

    st.header("✅ Task Management")

    # Add task form

    st.subheader("➕ Add a New Task")

    with st.form("add_task_form"):

        new_task_title = st.text_input(
            "Task Title",
            placeholder="Enter your new task..."
        )

        add_button = st.form_submit_button(
            "Add Task",
            use_container_width=True
        )

        if add_button:

            if new_task_title.strip():

                if st.session_state.use_mock:

                    next_id = max(
                        [task["id"] for task in tasks],
                        default=0
                    ) + 1

                    new_task = {
                        "id": next_id,
                        "title": new_task_title.strip(),
                        "done": False,
                        "created_at": time.strftime("%Y-%m-%d")
                    }

                    st.session_state.tasks.append(new_task)

                    st.success("Task added successfully!")
                    st.rerun()

                else:

                    new_task, error = api_client.create_task(
                        st.session_state.token,
                        new_task_title.strip()
                    )

                    if new_task is not None:

                        st.success("Task added successfully!")
                        st.rerun()

                    else:
                        st.error(error or "Unable to add task.")

            else:
                st.warning("Please enter a task title.")

    st.divider()

    # Display task list

    st.subheader("📝 Your Tasks")

    if tasks:

        for task in tasks:

            col1, col2 = st.columns([4, 1])

            with col1:

                if task.get("done", False):
                    st.markdown(
                        f"~~{task['title']}~~ ✅"
                    )
                else:
                    st.write(
                        f"🔵 {task['title']}"
                    )

                st.caption(
                    f"Created: {task.get('created_at', 'N/A')}"
                )

            with col2:

                if not task.get("done", False):

                    if st.button(
                        "Complete",
                        key=f"complete_{task['id']}"
                    ):

                        if st.session_state.use_mock:

                            for item in st.session_state.tasks:

                                if item["id"] == task["id"]:
                                    item["done"] = True

                            st.success("Task completed!")
                            st.rerun()

                        else:

                            updated_task, error = (
                                api_client.complete_task(
                                    st.session_state.token,
                                    task["id"]
                                )
                            )

                            if updated_task is not None:

                                st.success("Task completed!")
                                st.rerun()

                            else:
                                st.error(
                                    error or "Unable to complete task."
                                )

            st.divider()

    else:
        st.info(
            "You don't have any tasks yet. Add one above!"
        )


# ── TAB 3: AI Chat ─────────────────────────────────────────────────────────

with tab_chat:

    st.header("🤖 AI Assistant")

    st.write(
        "Ask questions about Python, Streamlit, FastAPI, "
        "authentication, or task management."
    )

    # Display previous chat messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # Receive user input

    user_prompt = st.chat_input(
        "Ask me anything..."
    )

    if user_prompt:

        # Save and display user message

        st.session_state.messages.append({
            "role": "user",
            "content": user_prompt
        })

        with st.chat_message("user"):
            st.write(user_prompt)

        # Generate mock AI response

        response = generate_mock_response(user_prompt)

        # Display streaming response

        with st.chat_message("assistant"):

            full_response = st.write_stream(
                stream_response(response)
            )

        # Save assistant response

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

