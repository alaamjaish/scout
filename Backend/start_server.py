#!/usr/bin/env python3
"""
Alternative server startup script with proper Python path handling.
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Add the Backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def main():
    # Load environment variables
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
    
    # Change to the Backend directory
    os.chdir(backend_dir)
    
    # Import the FastAPI app
    from api.main import app
    
    # Run the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )

if __name__ == "__main__":
    main() 