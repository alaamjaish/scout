import streamlit as st
from scraper import get_latest_articles  
from llm import generate_newsletter
from email_sender import send_newsletter_email
import datetime
import re

def main():
    # Page configuration
    st.set_page_config(
        page_title="Scout AI Newsletter Generator v2.0",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .email-section {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #2196f3;
    }
    .delivery-options {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📧 Scout AI Newsletter Generator v2.0</h1>
        <p>Generate professional newsletters AND send them via email!</p>
        <small>🚀 NEW: Resend email delivery - developer-friendly!</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for instructions and features
    with st.sidebar:
        st.header("📋 How to Use Scout v2.0")
        st.markdown("""
        1. **Enter your newsletter topic** in the main area
        2. **Choose delivery method**: Download, Email, or Both
        3. **Add email address** (if sending via email)
        4. **Click 'Generate & Send'** to start AI research
        5. **Wait for processing** (usually 30-60 seconds)
        6. **Receive your newsletter** via your chosen method!
        """)
        
        st.header("✨ What's NEW in v2.0")
        st.markdown("""
        • **📧 Email Delivery** - Send directly to any email
        • **🎨 Beautiful HTML emails** - Professional formatting
        • **📱 Mobile-friendly** - Looks great on all devices
        • **⚡ Instant delivery** - Emails arrive in seconds
        • **🚀 Resend API** - Developer-friendly, no SMTP complexity
        • **📊 Delivery tracking** - Know when it's sent
        """)
        
        st.header("💡 Topic Ideas")
        if st.button("🤖 AI & Machine Learning"):
            st.session_state.suggested_topic = "Latest breakthroughs in artificial intelligence and machine learning"
        if st.button("🔬 Biotech & Health"):
            st.session_state.suggested_topic = "Recent developments in biotechnology and healthcare innovation"
        if st.button("🌱 Climate Tech"):
            st.session_state.suggested_topic = "Sustainable technology and climate change solutions"
        if st.button("💰 Fintech"):
            st.session_state.suggested_topic = "Financial technology trends and digital banking innovations"
        if st.button("🚀 Space Tech"):
            st.session_state.suggested_topic = "Space exploration and aerospace technology advances"
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Topic input with suggestion handling
        default_topic = st.session_state.get('suggested_topic', '')
        topic = st.text_input(
            "📝 Enter your newsletter topic:",
            value=default_topic,
            placeholder="e.g., AI breakthroughs, climate tech, fintech trends, robotics innovations",
            help="Be specific for better results. Examples: 'Latest developments in quantum computing' or 'Sustainable energy innovations 2025'"
        )
    
    with col2:
        st.markdown("### 🎯 Quick Tips")
        st.markdown("""
        - **Be specific**: "AI robotics in manufacturing" vs "AI"
        - **Include timeframe**: "Recent developments" or "2025 trends"
        - **Focus areas**: "market impact", "technical breakthroughs"
        """)
    
    # NEW: Email Section
    st.markdown("""
    <div class="email-section">
        <h3>📧 Delivery Options</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Delivery method selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        download_only = st.checkbox("📥 Download Newsletter", value=True)
    
    with col2:
        send_email = st.checkbox("📧 Send via Email", value=False)
    
    with col3:
        if send_email:
            st.success("✅ Email delivery enabled!")
        else:
            st.info("📄 Download only mode")
    
    # Email input (only show if email option is selected)
    recipient_email = ""
    if send_email:
        st.markdown("### 📬 Email Details")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            recipient_email = st.text_input(
                "📧 Send newsletter to:",
                placeholder="your-email@example.com",
                help="Enter the email address where you'd like to receive the newsletter"
            )
        
        with col2:
            if recipient_email:
                # Validate email format
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, recipient_email):
                    st.success("✅ Valid email")
                else:
                    st.error("❌ Invalid email format")
        
        # Email preview info
        if recipient_email and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', recipient_email):
            st.info(f"📧 Newsletter will be sent to: **{recipient_email}**")
    
    # Newsletter generation
    button_text = "🚀 Generate Newsletter"
    if send_email and recipient_email:
        button_text = "📧 Generate & Send Email"
    elif download_only:
        button_text = "📥 Generate & Download"
    
    if st.button(button_text, type="primary", use_container_width=True):
        if topic:
            # Clear any previous suggested topic
            if 'suggested_topic' in st.session_state:
                del st.session_state.suggested_topic
            
            # Validation
            if send_email and not recipient_email:
                st.error("⚠️ Please enter an email address to send the newsletter!")
                return
            
            if send_email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', recipient_email):
                st.error("⚠️ Please enter a valid email address!")
                return
            
            if not download_only and not send_email:
                st.error("⚠️ Please select at least one delivery method!")
                return
                
            # Progress tracking
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Research
                    status_text.markdown("🔍 **Researching your topic across multiple sources...**")
                    progress_bar.progress(20)
                    
                    search_results = get_latest_articles(topic)
                    progress_bar.progress(50)
                    
                    # Check if we got good results
                    if not search_results:
                        st.warning("⚠️ No high-quality content found for this topic. Try a different search term or check your API keys.")
                        return
                    
                    # Step 2: Generate
                    status_text.markdown("✍️ **Generating your newsletter with AI...**")
                    progress_bar.progress(70)
                    
                    newsletter = generate_newsletter(search_results, topic)
                    progress_bar.progress(85)
                    
                    # Step 3: Email sending (if requested)
                    email_success = False
                    email_message = ""
                    
                    if send_email:
                        status_text.markdown("📧 **Sending email...**")
                        progress_bar.progress(90)
                        
                        email_success, email_message = send_newsletter_email(recipient_email, newsletter, topic)
                        
                    # Step 4: Complete
                    progress_bar.progress(100)
                    status_text.markdown("✅ **Newsletter generated successfully!**")
                    
                    # Clear progress after a moment
                    import time
                    time.sleep(1)
                    progress_container.empty()
                    
                    # Display results based on delivery method
                    if send_email and email_success:
                        st.success(f"🎉 Newsletter sent successfully to **{recipient_email}**!")
                        st.balloons()  # Celebration animation!
                    elif send_email and not email_success:
                        st.error(f"❌ Email sending failed: {email_message}")
                        st.warning("💡 You can still download the newsletter below!")
                    
                    if download_only or not email_success:
                        st.success("🎉 Your newsletter is ready for download!")
                    
                    # Newsletter display with better formatting
                    st.markdown("### 📰 Your Newsletter:")
                    
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📖 Formatted View", "📝 Raw Markdown"])
                    
                    with tab1:
                        st.markdown(newsletter)
                    
                    with tab2:
                        st.code(newsletter, language="markdown")
                    
                    # Download and sharing options
                    st.markdown("### 💾 Delivery Summary")
                    
                    # Show delivery status
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if download_only:
                            st.success("📥 Download Ready")
                        else:
                            st.info("📥 Download Available")
                    
                    with col2:
                        if send_email:
                            if email_success:
                                st.success("📧 Email Sent ✅")
                            else:
                                st.error("📧 Email Failed ❌")
                        else:
                            st.info("📧 Email Not Requested")
                    
                    with col3:
                        sources_used = len(search_results)
                        st.metric("📊 Sources Used", sources_used)
                    
                    # Download options
                    st.markdown("### 📥 Download Options")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Generate filename
                        safe_topic = topic.replace(' ', '_').replace('/', '_')[:30]
                        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
                        filename = f"scout_newsletter_{safe_topic}_{timestamp}.md"
                        
                        st.download_button(
                            label="📥 Download Markdown",
                            data=newsletter,
                            file_name=filename,
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col2:
                        if send_email and email_success:
                            st.success("📧 Already in your inbox!")
                        else:
                            # Show email retry option if it failed
                            if send_email and not email_success:
                                if st.button("🔄 Retry Email", use_container_width=True):
                                    retry_success, retry_message = send_newsletter_email(recipient_email, newsletter, topic)
                                    if retry_success:
                                        st.success("📧 Email sent on retry!")
                                        st.balloons()
                                    else:
                                        st.error(f"❌ Retry failed: {retry_message}")
                            else:
                                st.info("📧 Email delivery\n*Available above*")
                    
                    with col3:
                        # Future: Add PDF option
                        st.info("📄 PDF export\n*Coming v2.1*")
                    
                    # Newsletter statistics
                    st.markdown("### 📊 Newsletter Stats")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        word_count = len(newsletter.split())
                        st.metric("Words", word_count)
                    
                    with col2:
                        char_count = len(newsletter)
                        st.metric("Characters", char_count)
                    
                    with col3:
                        sources_used = len(search_results)
                        st.metric("Sources", sources_used)
                    
                    with col4:
                        estimated_read_time = max(1, word_count // 200)
                        st.metric("Read Time", f"{estimated_read_time} min")
                    
                    # Email-specific stats (if email was sent)
                    if send_email and email_success:
                        st.markdown("### 📧 Email Delivery Stats")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("📧 Delivered To", "1 recipient")
                        
                        with col2:
                            delivery_time = datetime.datetime.now().strftime('%H:%M')
                            st.metric("🕐 Sent At", delivery_time)
                        
                        with col3:
                            st.metric("📱 Format", "HTML + Text")
                    
                    # Feedback section
                    st.markdown("### 💬 Feedback")
                    feedback_col1, feedback_col2 = st.columns(2)
                    
                    with feedback_col1:
                        if st.button("👍 Great newsletter!", use_container_width=True):
                            st.success("Thanks for the feedback! 🎉")
                    
                    with feedback_col2:
                        if st.button("💡 Suggest improvements", use_container_width=True):
                            st.info("Feature coming soon! For now, try different search terms for better results.")
                    
                except Exception as e:
                    progress_container.empty()
                    st.error(f"❌ **Error generating newsletter:** {str(e)}")
                    
                    # Helpful error messages based on common issues
                    if "API" in str(e) or "key" in str(e).lower():
                        st.markdown("""
                        **Possible solutions:**
                        - Check that your `.env` file exists with valid API keys
                        - Verify your TAVILY_API_KEY and OPENAI_API_KEY are correct
                        - Make sure you have sufficient API credits
                        """)
                    elif "resend" in str(e).lower() or "email" in str(e).lower():
                        st.markdown("""
                        **Email configuration needed:**
                        - Add RESEND_API_KEY to your .env file
                        - Get your free API key from resend.com
                        - Run: python test_resend.py to verify setup
                        - Check EMAIL_SETUP.md for step-by-step guide
                        """)
                    else:
                        st.markdown("""
                        **Try these steps:**
                        - Check your internet connection
                        - Try a different, more specific topic
                        - Wait a moment and try again
                        """)
                        
        else:
            st.error("⚠️ Please enter a topic to generate a newsletter!")
    
    # Footer with additional information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Scout AI Newsletter Generator v2.0</strong> • Built with ❤️ using Python</p>
        <p>Powered by Tavily Search & OpenAI • <a href='https://github.com' target='_blank'>View on GitHub</a></p>
        <p><em>🚀 v2.0: Now with email delivery! | 📥 v1.0: Download only</em></p>
        <p><strong>🎯 Day 2 of our 7-day web launch! Next: v3.0 with advanced AI!</strong></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 