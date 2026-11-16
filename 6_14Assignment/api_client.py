
"""
Module 6 Project — AI Dashboard
API Client
"""

import requests

API_BASE = "http://localhost:8000"


def normalize_task(task):
    """Convert backend task fields to Module 6 format."""

    task["done"] = task.get("completed", False)
    return task


def login(username: str, password: str):

    try:
        response = requests.post(
            API_BASE + "/auth/token",
            data={
                "username": username,
                "password": password
            }
        )

        if not response.ok:
            return None, "Login failed. Check your credentials."

        data = response.json()
        token = data.get("access_token")

        if not token:
            return None, "No access token received."

        return token, None

    except requests.ConnectionError:
        return None, "Cannot connect to the backend."


def get_tasks(token: str):

    try:
        response = requests.get(
            API_BASE + "/tasks/",
            headers={"Authorization": f"Bearer {token}"}
        )

        if not response.ok:
            return None, "Unable to retrieve tasks."

        tasks = response.json()

        return [normalize_task(task) for task in tasks], None

    except requests.ConnectionError:
        return None, "Cannot connect to the backend."


def create_task(token: str, title: str):

    try:
        response = requests.post(
            API_BASE + "/tasks/",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": title}
        )

        if not response.ok:
            return None, "Unable to create task."

        task = response.json()

        return normalize_task(task), None

    except requests.ConnectionError:
        return None, "Cannot connect to the backend."


def complete_task(token: str, task_id: int):

    try:
        response = requests.patch(
            API_BASE + f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"completed": True}
        )

        if not response.ok:
            return None, "Unable to complete task."

        task = response.json()

        return normalize_task(task), None

    except requests.ConnectionError:
        return None, "Cannot connect to the backend."
