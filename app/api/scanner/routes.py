from fastapi import APIRouter, HTTPException, status
import uuid, redis, json

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


rdb = redis.Redis(host="localhost", port = 6379, decode_responses=True)

@router.post("/scan")
def start_scan(request: dict):
    scan_id = str(uuid.uuid4())
    domain = request.get("domain")
    job = {
        "scan_id": scan_id,
        "domain": domain,
        "status": "in progress",
        "progress": "0%"
    }
    rdb.lpush("scan_jobs", json.dumps(job))

    return {"scan_id": scan_id, "message": "Scan started"}