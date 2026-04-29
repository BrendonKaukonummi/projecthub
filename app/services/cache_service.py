from app.database.redis_client import redis_client

LATEST_ACTIVITY_KEY = "projecthub:latest_activity"

DEFAULT_TTL = 300


def set_latest_activity(message: str, ttl: int = DEFAULT_TTL) -> None:
    redis_client.set(LATEST_ACTIVITY_KEY, message, ex=ttl)
    print(f"   [CACHE] Stored latest activity (TTL: {ttl}s)")


def get_latest_activity() -> str | None:
    value = redis_client.get(LATEST_ACTIVITY_KEY)
    if value:
        print(f"   [CACHE] Retrieved latest activity from cache")
    else:
        print(f"   [CACHE] Cache miss - key expired or not set")
    return value


def delete_latest_activity() -> None:
    redis_client.delete(LATEST_ACTIVITY_KEY)
    print(f"   [CACHE] Deleted latest activity cache")


def set_user_recent_projects(user_id: int, projects_json: str, ttl: int = DEFAULT_TTL) -> None:
    key = f"USER_PROJECTS_KEY_PREFIX:{user_id}:recent_projects"
    redis_client.set(key, projects_json, ex=ttl)
    print(f"   [CACHE] Stored user {user_id}'s recent projects (TTL: {ttl}s)")


def get_user_recent_projects(user_id: int) -> str | None:
    key = f"USER_PROJECTS_KEY_PREFIX:{user_id}:recent_projects"
    value = redis_client.get(key)
    if value:
        print(f"   [CACHE] Retrieved user {user_id}'s projects from cache")
    else:
        print(f"   [CACHE] Cache miss for user {user_id}'s projects")
    return value


def delete_user_recent_projects(user_id: int) -> None:
    key = f"USER_PROJECTS_KEY_PREFIX:{user_id}:recent_projects"
    redis_client.delete(key)
    print(f"   [CACHE] Deleted user {user_id}'s projects cache")
    

async def get_latest_activity_with_fallback() -> str:
    """Get latest activity from cache, or MongoDB if cache miss.
    
    This implements the Cache-Aside pattern:
    1. Check cache
    2. If miss, query database
    3. Store result in cache
    4. Return result
    
    Returns:
        Latest activity message
    """
    # 1. Try cache first
    cached = get_latest_activity()
    if cached:
        return cached
    
    # 2. Cache miss - query MongoDB
    print("   [CACHE] Cache miss - querying MongoDB")
    from app.services import log_service
    
    logs = await log_service.get_recent_logs(limit=1)
    if not logs:
        return "No activity yet"
    
    latest_log = logs[0]
    activity_message = (
        f"User {latest_log.user_id} performed '{latest_log.action_type}'"
    )
    
    # 3. Store in cache
    set_latest_activity(activity_message, ttl=DEFAULT_TTL)
    
    # 4. Return result
    return activity_message