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
        print("\n   🔧 Setup Instructions:")
        print("   - Go to resend.com and create a free account")
        print("   - Get your API key from the dashboard")
        print("   - Add RESEND_API_KEY=your_api_key to .env file")
        print("   - Make sure your domain (levanttalk.com) is verified")
        return False

def get_test_email():
    """Get email address for testing"""
    print("\n2️⃣ Email Address Setup...")
    
    while True:
        email = input("   📧 Enter test email address: ").strip()
        
        if '@' in email and '.' in email:
            return email
        else:
            print("   ❌ Please enter a valid email address")

def send_test_email(email):
    """Send a test newsletter email"""
    print(f"\n3️⃣ Sending Test Email to {email}...")
    
    sender = EmailSender()
    
    # Create test newsletter content
    test_content = """
# 🧪 Test Newsletter

This is a test email from your Scout AI Newsletter Generator!

## ✅ What this test confirms:
- **API Connection**: Your Resend API is working
- **Domain Setup**: levanttalk.com is properly configured  
- **Email Delivery**: Emails can reach the recipient
- **HTML Formatting**: Beautiful newsletter styling

## 🚀 Next Steps:
1. Check your inbox (and spam folder)
2. If you receive this email, Scout is ready to go!
3. Start generating real newsletters in the main app

---

**Powered by:**
- 🔍 Tavily Search API
- 🤖 OpenAI GPT
- 📧 Resend Email API
- 🌐 levanttalk.com domain

Happy newsletter generation! 🎉
    """.strip()
    
    success, result_message = sender.send_newsletter(
        recipient_email=email,
        newsletter_content=test_content,
        topic="Resend API Test"
    )
    
    if success:
        print("   ✅ Test email sent successfully!")
        print(f"   📧 {result_message}")
        print("\n   🎯 What to check:")
        print("   - Check your inbox for the test email")
        print("   - Check spam/junk folder if not in inbox")
        print("   - Verify the email formatting looks good")
        return True
    else:
        print("   ❌ Test email failed!")
        print(f"   💬 Error: {result_message}")
        
        if "domain" in result_message.lower():
            print("\n   🔧 Domain Issues:")
            print("   - Make sure levanttalk.com is verified in Resend")
            print("   - Check Resend dashboard for domain status")
        elif "api key" in result_message.lower():
            print("\n   🔧 API Key Issues:")
            print("   - Verify your RESEND_API_KEY in .env file")
            print("   - Make sure API key has sending permissions")
        
        return False

def check_environment():
    """Check if .env file exists and is configured"""
    print("🔍 Checking Environment Configuration...")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        print("\n   📝 Create .env file with:")
        print("   RESEND_API_KEY=re_your_api_key_here")
        return False
    
    resend_key = os.getenv('RESEND_API_KEY')
    if not resend_key:
        print("   ❌ RESEND_API_KEY not found in .env")
        print("\n   📝 Add to your .env file:")
        print("   RESEND_API_KEY=re_your_api_key_here")
        return False
    
    if resend_key.startswith('re_'):
        print("   ✅ Resend API key format looks correct")
        return True
    else:
        print("   ⚠️  API key format unusual (should start with 're_')")
        return True

def main():
    """Main test function"""
    print_header()
    
    # Check environment setup
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ Environment setup incomplete. Please fix the issues above.")
        return
    
    print()
    
    # Test API configuration
    api_ok = test_api_configuration()
    if not api_ok:
        print("\n❌ API configuration failed. Please fix the issues above.")
        return
    
    # Get test email
    test_email = get_test_email()
    
    # Send test email
    email_sent = send_test_email(test_email)
    
    # Final results
    print("\n" + "=" * 50)
    if email_sent:
        print("🎉 SUCCESS! Resend email system is working perfectly!")
        print("\n✅ Your Scout Newsletter Generator is ready to:")
        print("   - Generate AI-powered newsletters")
        print("   - Send beautiful HTML emails via Resend")
        print("   - Use your verified levanttalk.com domain")
        print("\n🚀 Run the main app: streamlit run app.py")
    else:
        print("❌ Email test failed. Please check the errors above.")
        print("\n🔧 Common solutions:")
        print("   - Verify your Resend API key")
        print("   - Check domain verification at resend.com")
        print("   - Make sure .env file is properly configured")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your setup and try again.") 