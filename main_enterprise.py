import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from platform.api_gateway.router import api_router
from platform.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    description="Multi-Tenant Smart City Enterprise API"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
