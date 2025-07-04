#!/usr/bin/env python3
"""
🧪 Scout Resend Email Test Script

This script helps you test your Resend API configuration
before using Scout's full email functionality.

Usage:
1. Set your RESEND_API_KEY in .env file
2. Run: python test_resend.py
3. Follow the prompts to test email sending
"""

import os
import sys
from email_sender import EmailSender

def print_header():
    print("🚀 Scout Email Test - Resend Integration")
    print("=" * 50)
    print()

def test_api_configuration():
    """Test if Resend API key is configured"""
    print("1️⃣ Testing API Configuration...")
    
    sender = EmailSender()
    success, message = sender.test_email_connection()
    
    if success:
        print(f"   ✅ {message}")
        return True
    else:
        print(f"   ❌ {message}")
        print()
        print("🔧 How to fix:")
        print("   1. Go to https://resend.com and create a free account")
        print("   2. Get your API key from Dashboard → API Keys")
        print("   3. Add to your .env file: RESEND_API_KEY=re_your_key_here")
        print("   4. Run this test again")
        return False

def test_email_sending():
    """Test sending a real email"""
    print("\n2️⃣ Testing Email Sending...")
    
    email = input("   📧 Enter your email address to test: ").strip()
    
    if not email:
        print("   ❌ No email provided")
        return False
    
    # Create a test newsletter
    test_content = """
# 🧪 Scout Email Test

This is a **test email** from Scout AI Newsletter Generator!

## What this proves:
- ✅ Your Resend API key is working
- ✅ Scout can send beautiful HTML emails
- ✅ Email delivery is configured correctly

## Next steps:
1. Run Scout: `streamlit run app.py`
2. Generate real newsletters with AI research
3. Send them via email or download as files

**Congratulations!** Your email setup is working perfectly! 🎉
    """.strip()
    
    print(f"   📤 Sending test email to {email}...")
    
    sender = EmailSender()
    success, message = sender.send_newsletter(email, test_content, "Scout Email Test")
    
    if success:
        print(f"   ✅ {message}")
        print(f"   📧 Check your inbox at {email}!")
        return True
    else:
        print(f"   ❌ {message}")
        return False

def show_next_steps():
    """Show what to do after successful test"""
    print("\n🎉 Success! Your Scout email setup is ready!")
    print()
    print("📋 Next steps:")
    print("   1. Run Scout: streamlit run app.py")
    print("   2. Enter any topic (e.g., 'AI breakthroughs')")
    print("   3. Check 'Send via Email' option")
    print("   4. Enter recipient email")
    print("   5. Click 'Generate & Send Email'")
    print()
    print("🚀 Scout will research, generate, and email your newsletter!")

def main():
    print_header()
    
    # Test 1: API Configuration
    if not test_api_configuration():
        sys.exit(1)
    
    # Test 2: Email Sending (optional)
    print()
    choice = input("🔍 Want to test sending a real email? (y/n): ").strip().lower()
    
    if choice in ['y', 'yes']:
        if test_email_sending():
            show_next_steps()
        else:
            print("\n💡 The API key works, but email sending failed.")
            print("   This might be a temporary issue. Try again or use Scout directly.")
    else:
        print("\n✅ API test passed! You're ready to use Scout.")
        print("   Run 'streamlit run app.py' to start generating newsletters!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled. Run again anytime!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Try checking your .env file or running: python email_sender.py") 