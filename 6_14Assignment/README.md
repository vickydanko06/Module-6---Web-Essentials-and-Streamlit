
# AI Dashboard — Streamlit + FastAPI

A full-stack Python task management dashboard combining my Module 5 FastAPI backend with my Module 6 Streamlit frontend.

The application allows users to log in securely, manage tasks, monitor productivity, visualize progress, and interact with a demonstration AI assistant.

## Features

### Authentication
- User registration through FastAPI
- Secure password hashing using Passlib and bcrypt
- JWT-based authentication
- Login and logout functionality
- Protected backend endpoints

### Dashboard
- Total task metrics
- Completed and pending task counts
- Task data table
- Task completion visualizations
- Interactive Streamlit interface

### Task Management
- Create new tasks
- View existing tasks
- Mark tasks as completed
- Store tasks in a SQLite database
- Backend support for updating and deleting tasks

### AI Chat Assistant
- Interactive chat interface using `st.chat_message()`
- Conversation history stored in Streamlit session state
- Keyword-based mock AI responses
- Streaming responses using `st.write_stream()`
- No external AI API key required

**Note:** The AI assistant currently uses predefined mock responses rather than a live AI model.

### Offline Mode
- Run the dashboard without FastAPI
- Use sample task data
- Test dashboard functionality independently

## Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| API Server | Uvicorn |
| Database | SQLite |
| ORM | SQLAlchemy |
| Authentication | JWT, Passlib, bcrypt |
| API Communication | Requests |
| Visualization | Streamlit, Plotly |

## Project Structure

```text
6_14Assignment/
├── app.py
├── api_client.py
├── mock_data.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── app/
    ├── main.py
    ├── auth.py
    ├── database.py
    ├── routers/
    │   ├── auth.py
    │   └── tasks.py
    ├── models/
    └── schemas/
```

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd 6_14Assignment
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment:

**Mac/Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Install additional backend dependencies:

```bash
python -m pip install fastapi uvicorn sqlalchemy "passlib[bcrypt]" "bcrypt==4.0.1" python-jose python-multipart
```

The bcrypt version is pinned for compatibility with Passlib 1.7.4.

### 4. Configure Authentication

Set a unique JWT signing secret for local development.

**Mac/Linux**
```bash
export SECRET_KEY="replace-with-a-long-random-secret"
```

Do not commit passwords, API keys, or production secrets to GitHub.

## Running the Application

The frontend and backend run in separate terminals.

### Terminal 1 — FastAPI Backend

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### Terminal 2 — Streamlit Frontend

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start Streamlit:

```bash
python -m streamlit run app.py
```

Frontend URL:

http://localhost:8501

## User Registration and Login

1. Start the FastAPI backend.
2. Open http://127.0.0.1:8000/docs.
3. Find `POST /auth/register`.
4. Register a username, email, and password.
5. Open the Streamlit dashboard.
6. Leave "Use Mock Data (Offline Mode)" unchecked.
7. Log in using the registered credentials.

Once authenticated, users can access their tasks through the FastAPI backend.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/auth/register` | Register a user |
| POST | `/auth/token` | Authenticate and receive JWT |
| GET | `/auth/me` | Get authenticated user |
| GET | `/tasks/` | Retrieve tasks |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/{task_id}` | Retrieve a specific task |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/tasks/{task_id}/suggest` | Get a mock task suggestion |

Protected endpoints require JWT authentication.

## How the AI Assistant Works

The AI Assistant is implemented using Streamlit's chat components.

1. The user enters a message through the chat interface.
2. Python processes the message using `generate_mock_response()`.
3. The function checks for recognized keywords.
4. A predefined response is selected.
5. The response streams into the chat using `st.write_stream()`.
6. Conversation history is maintained in `st.session_state`.

Supported topics include:
- FastAPI
- Streamlit
- Task management
- JWT authentication
- Basic greetings

The backend also provides a task suggestion endpoint that returns a predefined productivity suggestion.

This implementation demonstrates the chat interface, session management, and streaming concepts without requiring a paid AI service.

## Frontend and Backend Integration

The Streamlit frontend communicates with FastAPI through `api_client.py`.

The integration supports:

- Backend user authentication
- JWT session management
- Retrieving database-backed tasks
- Creating new tasks
- Completing existing tasks

SQLite stores application data through SQLAlchemy.

When offline mode is enabled, the application uses mock data instead of backend API requests.

## Current Limitations

- AI chat uses mock responses rather than a live language model.
- The task suggestion endpoint is separate from the chat interface.
- JWT tokens expire after 30 minutes without automatic refresh.
- The default SQLite database is intended for local development.
- The application is designed as an educational project rather than a production deployment.

## Future Improvements

Potential enhancements include:

- Integrating a live AI model
- Connecting AI suggestions directly to dashboard tasks
- Adding task editing and deletion controls to Streamlit
- Implementing automatic JWT token refresh
- Deploying the frontend and backend
- Adding additional analytics and reporting

## Project Background

This project combines two Coding Temple AI Software Engineering modules:

**Module 5 — Backend Development**

Developed a REST API using FastAPI, SQLAlchemy, SQLite, and JWT authentication.

**Module 6 — Web Essentials and Streamlit**

Developed an interactive dashboard featuring authentication, task management, data visualization, session state, and a mock AI chat interface.

Combining both modules demonstrates frontend/backend integration, authenticated API communication, database operations, and interactive Python application development.
