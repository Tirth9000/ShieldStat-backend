from fastapi import APIRouter
from api.webhooks.schemas import ScannerWebhookRequest

router = APIRouter()


@router.post("/webhooks/scanner")
def scanner_webhook(request: ScannerWebhookRequest):
    data = request.data
    print(f"Received scanner webhook: {data}")

