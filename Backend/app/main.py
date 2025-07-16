# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .models import HealthResponse
from .routes.newsletter import router as newsletter_router
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(title="Scout Newsletter API - 3rd push")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. "Include" the chapter in our main book.
#    This line adds all the endpoints from newsletter.py to our main app.
#    - prefix adds '/api' to all URLs from that router.
#    - tags groups them in the documentation.
app.include_router(newsletter_router, prefix="/api", tags=["Newsletter"])


@app.get("/")
def read_root():
    """A root endpoint that provides basic API information."""
    return {"message": "Welcome to the Scout Newsletter API!", "docs_url": "/docs"}


# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

# 2. Add the new /health endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Checks the health of the API and its dependencies.
    """
    # Check the status of critical dependencies, like API keys
    services_status = {
        "openai_api_key": "configured" if os.getenv("OPENAI_API_KEY") else "missing",
        "tavily_api_key": "configured" if os.getenv("TAVILY_API_KEY") else "missing"
    }
    
    # Determine the overall status
    overall_status = "healthy"
    if "missing" in services_status.values():
        overall_status = "unhealthy"

    return HealthResponse(
        status=overall_status,
        services=services_status
    )


# THE EXSTRA error handling, super important for the future & for debugging & production
# -----------------------------------------------------------------------------------------------------------------


# 4. Add these two new handler blocks at the end of the file.
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """
    Handles errors that we raise on purpose (HTTPException).
    Formats them into our standard error response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Client Error",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """
    Handles any unexpected error that occurs in the application.
    This is the final safety net.
    """
    # In a real app, you would log the full error `str(exc)` to a file or monitoring service.
    print(f"An unexpected error occurred: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server. Please try again later.",
            "timestamp": datetime.now().isoformat(),
        },
    )
