from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes.guest import router as guest_router
from app.api.routes.signal import router as signal_router
from app.api.routes.interview import router as interview_router
from app.startup import on_startup

app = FastAPI(title="Podcast Guest Research Infrastructure", on_startup=[on_startup])

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static assets (dashboard, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(guest_router, prefix="/research", tags=["Research"])
app.include_router(signal_router, prefix="/signals", tags=["Signals"])
app.include_router(interview_router, prefix="/interview", tags=["Interview Intelligence"])

# Dashboard endpoint
@app.get("/", response_class=FileResponse)
async def get_dashboard():
    return FileResponse("app/static/dashboard.html")
