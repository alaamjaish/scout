#!/usr/bin/env python3
"""
Simple script to run the FastAPI server.
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print("🚀 Starting Scout AI Newsletter Generator API...")
    print(f"📡 Server: http://{host}:{port}")
    print(f"📚 Docs: http://{host}:{port}/docs")
    print(f"🔧 Health: http://{host}:{port}/health")
    print("=" * 50)
    
    # Run the server
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning",
        reload_dirs=["."] if debug else None
    )

if __name__ == "__main__":
    main() 