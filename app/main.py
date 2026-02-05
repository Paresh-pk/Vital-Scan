from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="AI-Assisted Health Risk Assessment Platform",
    description="Privacy-first, AI-driven health risk intelligence API.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1 import endpoints
app.include_router(endpoints.router, prefix="/api/v1", tags=["Assessment"])

# Mount Frontend (Static Files)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", tags=["Assessment"])
async def root():
    return FileResponse('frontend/index.html')
