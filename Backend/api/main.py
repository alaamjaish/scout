"""
Main FastAPI application for Scout AI Newsletter Generator.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import routes
from .routes.newsletter import router as newsletter_router
from .models.schemas import HealthResponse

# Create FastAPI app
app = FastAPI(
    title="Scout AI Newsletter Generator",
    description="AI-powered newsletter generation with intelligent research and quality control",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(newsletter_router, prefix="/api", tags=["newsletter"])

@app.get("/papa")
async def papa():
    return {"message": "habibi inta ya ghali"} # this is a test endpoint



@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Scout AI Newsletter Generator API",
        "version": "3.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check if core modules can be imported
        from core.smart_searcher import smart_search_brain
        from core.scraper import get_latest_articles
        from core.llm import generate_newsletter
        from core.quality_checker import smart_teacher_check
        from core.self_fixer import fix_newsletter
        
        services = {
            "core_modules": "healthy",
            "api": "healthy"
        }
        
        # Check for API keys (optional)
        openai_key = os.getenv("OPENAI_API_KEY")
        tavily_key = os.getenv("TAVILY_API_KEY")
        
        services["openai"] = "configured" if openai_key else "not_configured"
        services["tavily"] = "configured" if tavily_key else "not_configured"
        
        return HealthResponse(
            status="healthy",
            version="3.0.0",
            timestamp=datetime.now(),
            services=services
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            version="3.0.0",
            timestamp=datetime.now(),
            services={"error": str(e)}
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000) 