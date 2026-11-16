# project/starter/app/models/task.py
# Module 5 Project — Task model
#
# TODO: Define the Task ORM model
# Fields: id, title, description (optional), completed (bool, default False), owner_id (FK)
# Relationship: task belongs to a user

# project/starter/app/models/task.py
# Module 5 Project — Task model

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import Optional

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Task title
    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # Optional task description
    description: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )

    # Task completion status (defaults to False)
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Foreign key connecting task to its user
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationship to User model
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="tasks"
    )
