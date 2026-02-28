from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_tables
from app.api import workflows
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create DB tables
    await create_tables()
    yield
    # Shutdown: cleanup if needed
    pass

app = FastAPI(
    title="AI Workflow Automation API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS — allows React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])

@app.get("/")
async def root():
    return {"message": "AI Workflow Automation API is running ✅"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
