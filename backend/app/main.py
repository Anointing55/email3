# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .cleanup import setup_scheduler
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.getenv("PLAYWRIGHT_BROWSERS_PATH", "/opt/render/.cache/playwright")

app = FastAPI(
    title="Contact Info & Social Media Extractor",
    description="API for extracting contact information from websites",
    version="1.0.0",
    openapi_url="/openapi.json"
)

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Safe CORS fallback
cors_origins = os.getenv("ALLOWED_ORIGINS", "*")
origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add route prefixes
app.include_router(router, prefix="/api")

# Health route (optional but useful)
@app.get("/")
def read_root():
    return {"message": "Email & Social Link Extractor API is running"}

# Startup event for cleanup scheduler
@app.on_event("startup")
async def startup_event():
    setup_scheduler()
