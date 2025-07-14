#!/usr/bin/env python3
"""
Quick test to check if the API is working.
"""

import requests
import time

def test_api():
    """Test basic API functionality."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing API connectivity...")
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Version: {response.json()['version']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API not responding: {e}")
        print("   Make sure the server is running: python start_server.py")
        return False
    
    # Test 2: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Services: {data['services']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 3: API docs
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API documentation accessible!")
            print(f"   Visit: {base_url}/docs")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")
    
    print("\n🎉 API is working! Ready for testing.")
    print(f"📚 Interactive docs: {base_url}/docs")
    print(f"🔧 Health check: {base_url}/health")
    
    return True

if __name__ == "__main__":
    test_api() 