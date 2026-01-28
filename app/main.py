from dotenv import load_dotenv
load_dotenv()  # Load env vars FIRST before other imports

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth.routes import router as auth_router
from api.scanner.routes import router as scanner_router
from app.db.sessions import init_db, init_tables

app = FastAPI()

# Initialize database on startup
init_db()
init_tables()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(auth_router)
app.include_router(scanner_router)


@app.get('/')
def root():
    return "ShieldStat backend is running"
