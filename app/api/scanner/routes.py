from fastapi import APIRouter
from api.scanner.service import create_scan_task_to_queue
from api.scanner.schemas import RequestScanTask
from core.redis_queue import RedisClient
import json

router = APIRouter()

@router.post("/scanner/register-scan-task")
async def register_scan_task(request: RequestScanTask):
    return await create_scan_task_to_queue(request)


@router.get("/scanner/scanlist")
def get_scan_list():
    redis_client = RedisClient() 
    data = redis_client.redis.lrange("scan_queue", 0, -1)
    return  [json.loads(item) for item in data]
    # return [item for item in data]

@router.get("/scanner/clear")
def clear_scan_queue():
    redis_client = RedisClient() 
    redis_client.redis.delete("scan_queue")
    return {"message": "Scan queue cleared"}