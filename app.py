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
        <h1>📧 Scout AI Newsletter Generator</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for topic suggestions
    with st.sidebar:
        st.header("💡 Quick Topics")
        if st.button("🤖 AI & ML"):
            st.session_state.suggested_topic = "Latest breakthroughs in artificial intelligence"
        if st.button("🔬 Biotech"):
            st.session_state.suggested_topic = "Recent biotech innovations"
        if st.button("🌱 Climate Tech"):
            st.session_state.suggested_topic = "Climate technology solutions"
        if st.button("💰 Fintech"):
            st.session_state.suggested_topic = "Financial technology trends"
        if st.button("🚀 Space Tech"):
            st.session_state.suggested_topic = "Space technology advances"
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Topic input with suggestion handling
        default_topic = st.session_state.get('suggested_topic', '')
        topic = st.text_input(
            "📝 Newsletter topic:",
            value=default_topic,
            placeholder="e.g., AI breakthroughs, climate tech, fintech trends"
        )
    
    with col2:
        st.markdown("### 🎯 Tips")
        st.markdown("""
        - Be specific
        - Include timeframe  
        - Focus on recent trends
        """)
    
    st.markdown("### 📧 Delivery")
    
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
        col1, col2 = st.columns([2, 1])
        
        with col1:
            recipient_email = st.text_input(
                "📧 Email address:",
                placeholder="your-email@example.com"
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
            st.info(f"📧 Send to: **{recipient_email}**")
    
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
                st.error("⚠️ Enter email address")
                return
            
            if send_email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', recipient_email):
                st.error("⚠️ Invalid email")
                return
            
            if not download_only and not send_email:
                st.error("⚠️ Select delivery method")
                return
                
            # Progress tracking
            progress_container = st.container()
            
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Research
                    status_text.markdown("🔍 **Researching...**")
                    progress_bar.progress(20)
                    
                    search_results = get_latest_articles(topic)
                    progress_bar.progress(50)
                    
                    if not search_results:
                        st.warning("⚠️ No content found. Try a different topic.")
                        return
                    
                    # Generate
                    status_text.markdown("✍️ **Generating...**")
                    progress_bar.progress(70)
                    
                    newsletter = generate_newsletter(search_results, topic)
                    progress_bar.progress(85)
                    
                    # Email sending
                    email_success = False
                    email_message = ""
                    
                    if send_email:
                        status_text.markdown("📧 **Sending...**")
                        progress_bar.progress(90)
                        
                        email_success, email_message = send_newsletter_email(recipient_email, newsletter, topic)
                        
                    # Complete
                    progress_bar.progress(100)
                    status_text.markdown("✅ **Done!**")
                    
                    # Clear progress after a moment
                    import time
                    time.sleep(1)
                    progress_container.empty()
                    
                    # Display results
                    if send_email and email_success:
                        st.success(f"📧 Sent to **{recipient_email}**")
                    elif send_email and not email_success:
                        st.error(f"❌ Email failed: {email_message}")
                    
                    if download_only or not email_success:
                        st.success("✅ Newsletter ready")
                    
                    st.markdown("### 📰 Newsletter")
                    
                    tab1, tab2 = st.tabs(["📖 View", "📝 Raw"])
                    
                    with tab1:
                        st.markdown(newsletter)
                    
                    with tab2:
                        st.code(newsletter, language="markdown")
                    
                    # Download options
                    st.markdown("### 📥 Download")
                    
                    # Generate filename
                    safe_topic = topic.replace(' ', '_').replace('/', '_')[:30]
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
                    filename = f"scout_newsletter_{safe_topic}_{timestamp}.md"
                    
                    st.download_button(
                        label="📥 Download",
                        data=newsletter,
                        file_name=filename,
                        mime="text/markdown",
                        use_container_width=True
                    )
                    

                    
                except Exception as e:
                    progress_container.empty()
                    st.error(f"❌ Error: {str(e)}")
                    
                    # Quick error hints
                    if "API" in str(e) or "key" in str(e).lower():
                        st.error("Check your API keys in .env file")
                    elif "resend" in str(e).lower() or "email" in str(e).lower():
                        st.error("Email setup needed - check RESEND_API_KEY")
                    else:
                        st.error("Try again with a different topic")
                        
        else:
            st.error("⚠️ Enter a topic")
    


if __name__ == "__main__":
    main() 