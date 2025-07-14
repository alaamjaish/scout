#!/usr/bin/env python3
"""
Simple test to verify imports work correctly.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Testing imports...")

try:
    print("   Testing core imports...")
    from core.smart_searcher import smart_search_brain
    print("   ✅ smart_searcher imported successfully")
    
    from core.scraper import get_latest_articles
    print("   ✅ scraper imported successfully")
    
    from core.llm import generate_newsletter
    print("   ✅ llm imported successfully")
    
    from core.quality_checker import smart_teacher_check
    print("   ✅ quality_checker imported successfully")
    
    from core.self_fixer import fix_newsletter
    print("   ✅ self_fixer imported successfully")
    
    print("\n✅ All core imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

try:
    print("\n   Testing FastAPI imports...")
    from api.models.schemas import NewsletterRequest, NewsletterResponse
    print("   ✅ schemas imported successfully")
    
    from api.routes.newsletter import router
    print("   ✅ newsletter router imported successfully")
    
    from api.main import app
    print("   ✅ main app imported successfully")
    
    print("\n✅ All FastAPI imports successful!")
    print("🎉 Ready to start the server!")
    
except Exception as e:
    print(f"❌ FastAPI import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 