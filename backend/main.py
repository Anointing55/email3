from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import pandas as pd
# Add your other imports here

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Playwright on startup
@app.on_event("startup")
async def startup_event():
    app.state.playwright = await async_playwright().start()
    app.state.browser = await app.state.playwright.chromium.launch()

# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await app.state.browser.close()
    await app.state.playwright.stop()

@app.get("/")
async def root():
    return {"message": "Email3 Backend Running"}

# Add your other routes here
