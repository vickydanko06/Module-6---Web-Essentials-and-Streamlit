"""
L11 — Streamlit + FastAPI: Frontend  (STARTER)
================================================
Run with (after starting the backend):
    streamlit run frontend.py

Your goal: build a Streamlit frontend for the task API.

Required features:
    1. Login form (stores JWT in session state on success)
    2. Sidebar showing logged-in user + logout button
    3. Metrics row (total / done / pending tasks)
    4. Task list with Complete button per pending task
    5. Add task form (POST to API)
    6. Error handling for connection errors and 401s
    7. Auth gate: show login if no token, app if token exists

Key patterns:
    Auth gate:
        if st.session_state.token is None:
            # show login form
            st.stop()
        # rest of app (only reached when logged in)

    Centralised api_call(method, path, **kwargs):
        • Adds Authorization: Bearer <token> header automatically
        • Returns (data, error_string) — one of them is None
        • Handles 401 → clears token → returns error message
        • Handles ConnectionError → returns helpful error message
"""

import streamlit as st
import requests

API_BASE = "http://localhost:8000"

# ── Page config ────────────────────────────────────────────────────────────
# TODO: st.set_page_config
st.set_page_config()

# ── Session state ──────────────────────────────────────────────────────────
# TODO: Initialise "token" to None
# TODO: Initialise "username" to None

if "token" not in st.session_state:
    st.session_state["token"] = None
    st.session_state["username"] = None

# ══════════════════════════════════════════════════════════════════════════
# CENTRALISED API CLIENT
# ══════════════════════════════════════════════════════════════════════════
# TODO: Implement api_call(method, path, **kwargs)
#   - Inject Authorization header if token exists
#   - Call requests.request(method, API_BASE + path, headers=headers, ...)
#   - If 401: clear token and username, return (None, "Session expired...")
#   - If not response.ok: return (None, f"API error {status}: {text}")
#   - If 204: return ({}, None)
#   - Otherwise: return (response.json(), None)
#   - Catch ConnectionError: return (None, "Cannot connect to the API...")
def api_call(method: str, path: str, **kwargs):
    headers = kwargs.pop("headers", {}).copy()

    # Inject authentication token when available
    token = st.session_state.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.request(
            method,
            API_BASE + path,
            headers=headers,
            **kwargs
        )

        # Session expired or invalid token
        if response.status_code == 401:
            st.session_state.token = None
            st.session_state.username = None
            return None, "Session expired. Please log in again."

        # Handle unsuccessful responses
        if not response.ok:
            return None, (
                f"API error {response.status_code}: {response.text}"
            )

        # Successful response with no content
        if response.status_code == 204:
            return {}, None

        # Successful JSON response
        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to the API. Make sure the backend is running."


# ══════════════════════════════════════════════════════════════════════════
# AUTH GATE
# ══════════════════════════════════════════════════════════════════════════
# TODO: if st.session_state.token is None:
#   - Show login form (st.form)
#   - On submit: call api_call("POST", "/auth/token", json={...})
#   - On success: store token + username in session state, st.rerun()
#   - On error: st.error(error_message)
#   - Call st.stop() so the app below doesn't render
if not st.session_state.get("token"):
    st.title("Task Manager")
    st.subheader("Please log in")

    with st.form("login_form"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Log in")

    if login_submitted:
        data, error = api_call(
            "POST",
            "/auth/token",
            json={
                "username": username_input,
                "password": password_input
            }
        )

        if error:
            st.error(error)
        else:
            st.session_state.token = data["access_token"]
            st.session_state.username = data["username"]
            st.rerun()

    # Do not render the main app until authenticated
    st.stop()


# ══════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════
st.title("My Task Manager")
st.caption("Manage your tasks in one place.")
# ── Sidebar ────────────────────────────────────────────────────────────────
# TODO: with st.sidebar:
#   - App title + divider
#   - Show "Logged in as [username]"
#   - Logout button → clear token + username + st.rerun()
with st.sidebar:
    st.title("Task Manager")
    st.divider()

    st.write(f"Logged in as **{st.session_state.username}**")

    if st.button("Log out", use_container_width=True):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()
# ── Load tasks ─────────────────────────────────────────────────────────────
# TODO: tasks, error = api_call("GET", "/tasks")
# TODO: If error: st.error(error); tasks = []
tasks, error = api_call("GET", "/tasks")

if error:
    st.error(error)
    tasks = []
# ── Metrics ────────────────────────────────────────────────────────────────
# TODO: Calculate total, done, pending
# TODO: Display 3 st.metric() in 3 columns
total = len(tasks)
done = sum(1 for task in tasks if task["done"])
pending = total - done

col1, col2, col3 = st.columns(3)

col1.metric("Total Tasks", total)
col2.metric("Completed", done)
col3.metric("Pending", pending)

st.divider()
# ── Add task form ──────────────────────────────────────────────────────────
# TODO: st.form with a text_input and submit button
# TODO: On submit: api_call("POST", "/tasks", json={"title": ...})
#       → st.success / st.error, then st.rerun()
st.subheader("Add a Task")

with st.form("add_task_form", clear_on_submit=True):
    new_title = st.text_input("Task title", placeholder="What needs to be done?")
    add_submitted = st.form_submit_button("Add Task")

if add_submitted:
    if not new_title.strip():
        st.warning("Please enter a task title.")
    else:
        data, error = api_call(
            "POST",
            "/tasks",
            json={"title": new_title.strip()}
        )

        if error:
            st.error(error)
        else:
            st.success("Task created successfully!")
            st.rerun()

st.divider()

# ── Task list ──────────────────────────────────────────────────────────────
# TODO: For each task:
#   - Show title (strikethrough if done: f"~~{title}~~" in markdown)
#   - Show status (st.success for done, st.warning for pending)
#   - For pending tasks: Complete button → api_call("PATCH", f"/tasks/{id}/complete")
#     → st.rerun() on success

st.subheader("Your Tasks")

if not tasks:
    st.info("You don't have any tasks yet. Add one above!")
else:
    for task in tasks:
        task_id = task["id"]
        title = task["title"]
        is_done = task["done"]

        with st.container(border=True):
            col_task, col_status, col_action = st.columns(
                [4, 2, 2]
            )

            with col_task:
                if is_done:
                    st.markdown(f"~~{title}~~")
                else:
                    st.write(title)

            with col_status:
                if is_done:
                    st.success("Completed")
                else:
                    st.warning("Pending")

            with col_action:
                if not is_done:
                    if st.button(
                        "Complete",
                        key=f"complete_{task_id}"
                    ):
                        data, error = api_call(
                            "PATCH",
                            f"/tasks/{task_id}/complete"
                        )

                        if error:
                            st.error(error)
                        else:
                            st.rerun()