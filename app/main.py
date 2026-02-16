"""FastAPI main application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api_routes import router
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Spark Intelligence Copilot",
    description="AI-powered Spark job analysis and optimization",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "spark-intelligence-copilot"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Spark Intelligence Copilot",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
