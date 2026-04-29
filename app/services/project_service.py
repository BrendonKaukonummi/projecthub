from sqlmodel import Session, select
from app.models.sql_models import TaskTagLink, User, Project, Task, Tag
from datetime import datetime


def create_user(session: Session, username: str, email: str) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_project(session: Session, title: str, owner_id: int, is_active: bool = True) -> Project:
    project = Project(title=title, owner_id=owner_id, is_active=is_active)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def get_user_projects(session: Session, user_id: int) -> list[Project]:
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if user:
        return user.projects
    return []


def get_user(session: Session, user_id: int) -> User | None:
    user = session.get(User, user_id)
    return user


def create_task(session: Session, name: str, project_id: int, status: str = "todo", deadline: datetime | None = None, priority: int | None = None) -> Task:
    task = Task(name=name, project_id=project_id, status=status, deadline=deadline, priority=priority)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_project_with_tasks(session: Session, project_id: int) -> Project | None:
    statement = select(Project).where(Project.id == project_id)
    results = session.exec(statement)
    return results.first()


def create_tag(session: Session, name: str) -> Tag:
    tag = Tag(name=name)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def add_tag_to_task(session: Session, task_id: int, tag_id: int) -> Task | None:
    task = session.get(Task, task_id)
    tag = session.get(Tag, tag_id)
    if task and tag:
        task.tags.append(tag)
        session.add(task)
        session.commit()
    return task


def get_tasks_by_tag(session: Session, tag_name: str) -> list[Task]:
    statement = (
        select(Task)
        .join(TaskTagLink)
        .join(Tag)
        .where(Tag.name == tag_name)
    )
    return session.exec(statement).all()


def get_tasks_by_project_and_status(session: Session, project_id: int, status: str) -> list[Task]:
    statement = select(Task).where(Task.project_id == project_id).where(Task.status == status)
    return session.exec(statement).all()


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        print(f"Käyttäjää {user_id} ei löytynyt")
        return False
    session.delete(user)
    session.commit()
    print(f"Käyttäjä {user_id} poistettu")
    return True


def delete_project(session: Session, project_id: int) -> bool:
    project = session.get(Project, project_id)
    if not project:
        print(f"Projektia {project_id} ei löytynyt")
        return False
    session.delete(project)
    session.commit()
    print(f"Projekti {project_id} poistettu")
    return True


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if not task:
        print(f"Tehtävää {task_id} ei löytynyt")
        return False
    session.delete(task)
    session.commit()
    print(f"Tehtävä {task_id} poistettu")
    return True


def delete_tag(session: Session, tag_id: int) -> bool:
    tag = session.get(Tag, tag_id)
    if not tag:
        print(f"Tunnistetta {tag_id} ei löytynyt")
        return False
    session.delete(tag)
    session.commit()
    print(f"Tunniste {tag_id} poistettu")
    return True