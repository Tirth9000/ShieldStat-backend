import uuid, json
from api.scanner.schemas import RequestScanTask 
from core.redis_queue import RedisClient

redis_client = RedisClient()

async def create_scan_task_to_queue(data: RequestScanTask):
    user_id = data.user_id
    target = data.target

    scan_id = str(uuid.uuid4())
    scan_job = {
        "user_id": user_id,
        "scan_id": scan_id,
        "target": target,
        "status": "pending",
        "progress": 0
    }

    #store in redis queue
    redis_client.PushToQueue(data = scan_job)

    return {"message": "Scan task registered successfully", "scan_id": scan_id}
