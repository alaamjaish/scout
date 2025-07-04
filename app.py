import streamlit as st
from scraper import get_latest_articles  
from llm import generate_newsletter
import datetime

def main():
    # Page configuration
    st.set_page_config(
        page_title="Scout AI Newsletter Generator",
        page_icon="🚀",
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
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Scout AI Newsletter Generator</h1>
        <p>Generate professional newsletters on any topic using AI-powered research</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for instructions and features
    with st.sidebar:
        st.header("📋 How to Use Scout")
        st.markdown("""
        1. **Enter your newsletter topic** in the main area
        2. **Click 'Generate Newsletter'** to start AI research
        3. **Wait for processing** (usually 30-60 seconds)
        4. **Read and download** your professional newsletter
        """)
        
        st.header("✨ What Scout Does")
        st.markdown("""
        • **Multi-angle search**: 5 different search perspectives
        • **Quality filtering**: Removes low-quality content automatically
        • **Expert insights**: Includes real data and expert opinions
        • **Professional format**: Ready-to-share newsletter structure
        • **Cost-effective**: ~$0.10-0.20 per high-quality newsletter
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
    
    # Newsletter generation
    if st.button("🚀 Generate Newsletter", type="primary", use_container_width=True):
        if topic:
            # Clear any previous suggested topic
            if 'suggested_topic' in st.session_state:
                del st.session_state.suggested_topic
                
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
                    progress_bar.progress(60)
                    
                    # Check if we got good results
                    if not search_results:
                        st.warning("⚠️ No high-quality content found for this topic. Try a different search term or check your API keys.")
                        return
                    
                    # Step 2: Generate
                    status_text.markdown("✍️ **Generating your newsletter with AI...**")
                    progress_bar.progress(80)
                    
                    newsletter = generate_newsletter(search_results, topic)
                    
                    # Step 3: Complete
                    progress_bar.progress(100)
                    status_text.markdown("✅ **Newsletter generated successfully!**")
                    
                    # Clear progress after a moment
                    import time
                    time.sleep(1)
                    progress_container.empty()
                    
                    # Display results
                    st.success("🎉 Your newsletter is ready!")
                    
                    # Newsletter display with better formatting
                    st.markdown("### 📰 Your Newsletter:")
                    
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📖 Formatted View", "📝 Raw Markdown"])
                    
                    with tab1:
                        st.markdown(newsletter)
                    
                    with tab2:
                        st.code(newsletter, language="markdown")
                    
                    # Download and sharing options
                    st.markdown("### 💾 Download Options")
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
                        # Future: Add email option here (Day 2)
                        st.info("📧 Email delivery\n*Coming Day 2*")
                    
                    with col3:
                        # Future: Add PDF option
                        st.info("📄 PDF export\n*Coming soon*")
                    
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
        <p><strong>Scout AI Newsletter Generator</strong> • Built with ❤️ using Python</p>
        <p>Powered by Tavily Search & OpenAI • <a href='https://github.com' target='_blank'>View on GitHub</a></p>
        <p><em>Day 1 of our 7-day web launch! 🚀</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 