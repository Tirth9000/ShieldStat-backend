from fastapi import FastAPI
# from api.auth.routes import router as auth_router
from api.scanner.routes import router as scanner_router
from api.webhooks.scanner import router as webhook_scanner_router

app = FastAPI()

# Include routers
# app.include_router(auth_router)
app.include_router(scanner_router)
app.include_router(webhook_scanner_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)