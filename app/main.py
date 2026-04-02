import asyncio

from app.database.sql_db import get_session
from app.services import project_service

async def main() -> None:

    with get_session() as session:

        # proj_milestone1 = project_service.create_project(session, "Testiprojekti", 3)

        # task_milestone1 = project_service.create_task(session, "Testitehtävä", proj_milestone1.id, "in progress", "2026-04-12")

        # tag_milestone1 = project_service.create_tag(session, "Milestone 1")

        # project_service.add_tag_to_task(session, task_milestone1.id, tag_milestone1.id)

        # print(f"\n--- Projektin '{proj_milestone1.title}' in progress -tehtävät ---")
        # inprogress_tasks = project_service.get_tasks_by_project_and_status(
        #     session, proj_milestone1.id, "in progress")
        # for t in inprogress_tasks:
        #     print(f" - {t.name}")

        project_service.delete_project(session, 22)

        project_service.delete_task(session, 23)

        project_service.delete_tag(session, 19)
        

        # Aiemmat koodit:
        
        # user = project_service.create_user(session, "brendon", "brendon@amk.fi")

        # project_service.delete_user(session, 2)

        # project_service.create_project(session, "Testiprojekti", 3)
        
        # t1 = project_service.create_task(session, "Suunnittele kanta", proj.id)
        # t2 = project_service.create_task(session, "Koodaa mallit", proj.id)
        # t3 = project_service.create_task(session, "Testaa yhteys", 1)
        
        # tag_kiireellinen = project_service.create_tag(session, "Kiireellinen")
        # tag_backend = project_service.create_tag(session, "Backend")

        # project_service.add_tag_to_task(session, 1, 1)
        # project_service.add_tag_to_task(session, 2, 5)
        
        # full_project = project_service.get_project_with_tasks(session, proj.id)
        # if full_project:
        #     print(f"\nProjekti: {full_project.title}")
        #     print(f"Omistaja: {full_project.owner.username}")
        #     print(f"Tehtävät:")
        #     for task in full_project.tasks:
        #         print(f" - [{task.status}] {task.name}")

        # print("\nTehtävät tagilla 'Kiireellinen'")
        # urgent_tasks = project_service.get_tasks_by_tag(session, "Kiireellinen")
        # for t in urgent_tasks:
        #     print(f"Tehtävä: {t.name} | Projekti: {t.project.title}")
        #     print(f"Tunnisteet: {[tag.name for tag in t.tags]}")

if __name__ == "__main__":
    asyncio.run(main())