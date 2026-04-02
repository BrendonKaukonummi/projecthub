from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime

class TaskTagLink(SQLModel, table=True):
    task_id: int | None = Field(
        default=None, foreign_key="task.id", primary_key=True, ondelete="CASCADE"
    )
    tag_id: int | None = Field(
        default=None, foreign_key="tag.id", primary_key=True, ondelete="CASCADE"
    )

class ProjectUserLink(SQLModel, table=True):
    project_id: int | None = Field(
        default=None, foreign_key="project.id", primary_key=True, ondelete="CASCADE"
    )
    user_id: int | None = Field(
        default=None, foreign_key="user.id", primary_key=True, ondelete="CASCADE"
    )

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    username: str = Field(index=True, unique=True, min_length=3, max_length=20)
    email: str = Field(index=True, unique=True, min_length=5)

    projects: list["Project"] = Relationship(
        back_populates="owner",
        cascade_delete=True
    )

    joined_projects: list["Project"] = Relationship(
        back_populates="members",
        link_model=ProjectUserLink
    )

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="projects")

    tasks: list["Task"] = Relationship(
        back_populates="project",
        cascade_delete=True
    )

    members: list["User"] = Relationship(
        back_populates="joined_projects",
        link_model=ProjectUserLink
    )

    is_active: bool = Field(default=True)

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(min_length=3)
    status: str = Field(default="todo")

    project_id: int = Field(foreign_key="project.id")
    project: Project = Relationship(back_populates="tasks")

    tags: list["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTagLink
    )

    deadline: datetime | None = Field(default=None)
    priority: int | None = Field(default=None)

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, min_length=2)

    tasks: list["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTagLink
    )