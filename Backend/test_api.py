#!/usr/bin/env python3
"""
Simple test script to verify the API is working correctly.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Status: {response.json()['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_root_endpoint():
    """Test the root endpoint."""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Version: {response.json()['version']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

def test_connection():
    """Test the API connection endpoint."""
    print("\n🔍 Testing API connection...")
    try:
        response = requests.get(f"{BASE_URL}/api/test-connection")
        if response.status_code == 200:
            print("✅ API connection test passed!")
            print(f"   Message: {response.json()['message']}")
        else:
            print(f"❌ API connection test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API connection test error: {e}")

def test_newsletter_generation():
    """Test newsletter generation (requires API keys)."""
    print("\n🔍 Testing newsletter generation...")
    try:
        data = {"topic": "Python programming"}
        response = requests.post(
            f"{BASE_URL}/api/generate-newsletter",
            json=data,
            timeout=60  # Newsletter generation takes time
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Newsletter generation test passed!")
            print(f"   Quality Score: {result['quality_score']}/50")
            print(f"   Processing Time: {result['processing_time']}s")
            print(f"   Newsletter Length: {len(result['newsletter'])} characters")
        else:
            print(f"❌ Newsletter generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Newsletter generation error: {e}")

def main():
    """Run all tests."""
    print("🚀 Scout AI Newsletter Generator API Tests")
    print("=" * 50)
    
    # Test basic endpoints
    test_health_check()
    test_root_endpoint()
    test_connection()
    
    # Test newsletter generation (this requires API keys)
    print("\n" + "=" * 50)
    print("📝 Newsletter Generation Test")
    print("   Note: This requires valid API keys in .env file")
    print("=" * 50)
    
    test_newsletter_generation()
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("   Visit http://localhost:8000/docs for interactive API documentation")
    print("=" * 50)

if __name__ == "__main__":
    main() 