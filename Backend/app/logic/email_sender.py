import requests
import os
import re
from typing import Optional, Tuple
import logging

# Set up logging for email operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailSender:
    """
    Professional email sending class for Scout newsletters
    Uses Resend API for reliable email delivery
    """
    
    def __init__(self):
        self.resend_api_key = None
        self.setup_email_config()
    
    def setup_email_config(self):
        """Setup email configuration from environment variables"""
        self.resend_api_key = os.getenv('RESEND_API_KEY')
        
        if self.resend_api_key:
            logger.info("Resend API configuration loaded successfully")
        else:
            logger.warning("RESEND_API_KEY not found in environment variables")
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email address format
        Returns True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def create_newsletter_email_data(self, 
                                   recipient_email: str, 
                                   subject: str, 
                                   newsletter_content: str,
                                   topic: str) -> dict:
        """
        Create email data for Resend API
        """
        # Create both plain text and HTML versions
        text_content = self.create_text_version(newsletter_content, topic)
        html_content = self.create_html_version(newsletter_content, topic)
        
        return {
            "from": "Scout AI Newsletter <noreply@levanttalk.com>",  # Your verified domain!
            "to": [recipient_email],
            "subject": subject,
            "text": text_content,
            "html": html_content
        }
    
    def create_text_version(self, newsletter_content: str, topic: str) -> str:
        """Create plain text version of newsletter"""
        return f"""
🚀 Scout AI Newsletter

Topic: {topic}

{newsletter_content}

---
This newsletter was curated using AI technology.
        """.strip()
    
    def create_html_version(self, newsletter_content: str, topic: str) -> str:
        """Create beautiful HTML version of newsletter"""
        # Convert markdown to basic HTML formatting
        html_content = newsletter_content.replace('\n', '<br>')
        html_content = self.convert_markdown_to_html(html_content)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scout AI Newsletter</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .topic {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #2196f3;
        }}
        .content {{
            font-size: 16px;
            line-height: 1.8;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
        .powered-by {{
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }}
        .resend-badge {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            display: inline-block;
            margin-top: 5px;
        }}
        .domain-badge {{
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            display: inline-block;
            margin-top: 5px;
            margin-left: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Scout AI Newsletter</h1>
            <p>AI-Powered Research & Insights</p>
        </div>
        
        <div class="topic">
            <strong>📝 Topic:</strong> {topic}
        </div>
        
        <div class="content">
            {html_content}
        </div>
        
        <div class="footer">
            <div class="powered-by">
                <small><em>This newsletter was curated using AI technology</em></small>
            </div>
        </div>
    </div>
</body>
</html>
        """.strip()
        
    def convert_markdown_to_html(self, content: str) -> str:
        """Convert basic markdown formatting to HTML"""
        # Headers
        content = re.sub(r'^### (.*$)', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.*$)', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^# (.*$)', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        
        # Bold and italic
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        
        # Links (basic)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
        
        # Lists (basic)
        content = re.sub(r'^- (.*$)', r'<li>\1</li>', content, flags=re.MULTILINE)
        content = re.sub(r'^(\* (.*$))', r'<li>\2</li>', content, flags=re.MULTILINE)
        
        return content
    
    def send_newsletter(self, 
                       recipient_email: str, 
                       newsletter_content: str, 
                       topic: str) -> Tuple[bool, str]:
        """
        Send newsletter email using Resend API
        Returns (success: bool, message: str)
        """
        try:
            # Validate inputs
            if not self.resend_api_key:
                return False, "Resend API key not configured. Please set RESEND_API_KEY environment variable."
            
            if not self.validate_email(recipient_email):
                return False, f"Invalid email address: {recipient_email}"
            
            # Create subject
            subject = f"Scout AI Newsletter: {topic}"
            
            # Prepare email data
            email_data = self.create_newsletter_email_data(
                recipient_email, subject, newsletter_content, topic
            )
            
            # Send via Resend API
            headers = {
                "Authorization": f"Bearer {self.resend_api_key}",
                "Content-Type": "application/json"
            }
            
            logger.info(f"Sending newsletter to {recipient_email} via Resend API")
            
            response = requests.post(
                "https://api.resend.com/emails",
                json=email_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                email_id = result.get('id', 'unknown')
                logger.info(f"Email sent successfully via Resend. ID: {email_id}")
                return True, f"Email sent successfully! Resend ID: {email_id} (via levanttalk.com)"
            else:
                error_details = response.text
                logger.error(f"Resend API error {response.status_code}: {error_details}")
                
                if response.status_code == 401:
                    return False, "Invalid Resend API key. Please check your RESEND_API_KEY."
                elif response.status_code == 422:
                    return False, "Invalid email data. Please check the recipient email address."
                elif response.status_code == 429:
                    return False, "Rate limit reached. Please wait a moment and try again."
                else:
                    return False, f"Email sending failed. Resend API error: {error_details}"
                
        except requests.exceptions.Timeout:
            logger.error("Resend API request timed out")
            return False, "Email sending timed out. Please check your internet connection and try again."
        
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Resend API")
            return False, "Cannot connect to email service. Please check your internet connection."
        
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
    
    def test_email_connection(self) -> Tuple[bool, str]:
        """
        Test Resend API configuration
        Returns (success: bool, message: str)
        """
        try:
            if not self.resend_api_key:
                return False, "Resend API key not configured"
            
            # Test API key validity by making a simple request
            headers = {
                "Authorization": f"Bearer {self.resend_api_key}",
                "Content-Type": "application/json"
            }
            
            # Use Resend's domains endpoint to test API key
            response = requests.get(
                "https://api.resend.com/domains",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Resend API connection test successful")
                return True, "Resend API connection successful! Domain levanttalk.com ready to send emails."
            elif response.status_code == 401:
                return False, "Invalid Resend API key"
            else:
                return False, f"Resend API test failed: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Resend API test error: {str(e)}")
            return False, f"Connection test failed: {str(e)}"

# Convenience function for backward compatibility
def send_newsletter_email(recipient_email: str, newsletter_content: str, topic: str) -> Tuple[bool, str]:
    """
    Convenience function to send newsletter email
    Compatible with existing app.py code
    """
    sender = EmailSender()
    return sender.send_newsletter(recipient_email, newsletter_content, topic)

# Test function for development
def test_email_setup() -> None:
    """Test email configuration and connection"""
    sender = EmailSender()
    success, message = sender.test_email_connection()
    print(f"Test result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    print(f"Message: {message}")

if __name__ == "__main__":
    test_email_setup() 