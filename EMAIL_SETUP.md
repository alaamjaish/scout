# 📧 Email Setup Guide for Scout v2.0

## 🎯 **Quick Setup for Gmail (Recommended)**

### **Step 1: Get Gmail App Password**
1. Go to **Google Account settings**: https://myaccount.google.com
2. Click **"Security"** → **"2-Step Verification"** → **"App passwords"**
3. Create new app password for **"Scout Newsletter"**
4. **Copy the 16-character password** (you'll need this!)

### **Step 2: Add to Your .env File**
Add these lines to your `.env` file:

```
# Existing keys
TAVILY_API_KEY=your-tavily-key
OPENAI_API_KEY=your-openai-key

# NEW: Email configuration
SMTP_EMAIL=your-gmail@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

### **Step 3: Test It!**
Run Scout v2.0 and try sending an email to yourself!

---

## 🔧 **Alternative Email Providers**

### **For Outlook/Hotmail:**
```
SMTP_EMAIL=your-email@outlook.com
SMTP_PASSWORD=your-app-password
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### **For Yahoo:**
```
SMTP_EMAIL=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

---

## ⚠️ **Important Security Notes**

- **Never use your regular email password!** Always use app-specific passwords
- **Keep your .env file private** - never commit it to GitHub
- **App passwords are safer** than regular passwords for automated sending

---

## 🧪 **Testing Checklist**

- ✅ Gmail app password created
- ✅ Credentials added to .env file
- ✅ Scout v2.0 running locally
- ✅ Email sent successfully to yourself
- ✅ Email received and looks beautiful!

---

**Ready to test? Run:** `streamlit run app.py` 