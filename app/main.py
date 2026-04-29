import asyncio
# import json
# import time

from app.database.sql_db import get_session
from app.database.mongo_db import init_mongo
from app.services import project_service, log_service, cache_service


async def main() -> None:

    await init_mongo()
    
    
    with get_session() as session:


        brendon = project_service.create_user(
            session, username="brendon", email="brendon@example.com"
        )
        
        project1 = project_service.create_project(
            session, title="Milestone 2", owner_id=brendon.id
        )
        project2 = project_service.create_project(
            session, title="Demo Project", owner_id=brendon.id
        )
    
        await log_service.create_activity_log(
            action_type="user_registered",
            user_id=brendon.id,
            details={"username": brendon.username, "email": brendon.email}
        )
        await log_service.create_activity_log(
            action_type="project_created",
            user_id=brendon.id,
            details={"project_id": project1.id, "project_title": project1.title}
        )
        await log_service.create_activity_log(
            action_type="project_created",
            user_id=brendon.id,
            details={"project_id": project2.id, "project_title": project2.title}
        )
    
    print("\n" + "─"*70)
    print("Cache-Aside Pattern:")
    print("─"*70)
    
    print("\nFirst request (cache miss → MongoDB query)")
    activity = await cache_service.get_latest_activity_with_fallback()
    print(f"Result: {activity}")
    
    print("\nSecond request (cache hit → no MongoDB query)")
    activity = await cache_service.get_latest_activity_with_fallback()
    print(f"Result: {activity}")


if __name__ == "__main__":
    asyncio.run(main())