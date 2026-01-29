from pydantic import BaseModel


class ScannerWebhookRequest(BaseModel):
    scan_id: str
    event: str
    data: str