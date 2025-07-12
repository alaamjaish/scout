import streamlit as st
from Backend.scraper import get_latest_articles  
from Backend.llm import generate_newsletter
from Backend.smart_searcher import smart_search_brain
from Backend.quality_checker import smart_teacher_check
from Backend.self_fixer import fix_newsletter


def main():
    st.title("Scout AI Newsletter Generator - Version 3.0")
    st.caption("Intelligent Research & Quality Control System")
    
    # Sidebar with Pipeline Visualization
    with st.sidebar:
        st.markdown("### 🔧 CurrentSystem Pipeline")
        st.markdown("---")
        
        # Visual Pipeline Flow
        st.markdown("""
        **INTELLIGENT PIPELINE FLOW**
        
        ```
        📝 USER INPUT
             ↓
        🧠 SMART SEARCHER LLM
        │  • OpenAI GPT-4.1 takes input
        │  • Topic Analysis
        │  • Writes Custom Queries
             ↓
        🌐 WEB SCRAPER  
        │  • Tavily API
        │  • 5x Targeted Searches
        │  • Content Filtering
             ↓
        ✍️ CONTENT GENERATOR LLM
        │  • OpenAI GPT-4.1
        │  • Multi-language content processing
        │  • Professional Formatting (will be customized)
             ↓
        📊 QUALITY CHECKER LLM
        │  • AI Scoring (0-50)
        │  • Professional Standards
        │  • Bias Detection
             ↓
        🔧 AUTO-FIXER LLM
        │  • Smart Improvements
        │  • Iterative Refinement
        │  • Quality Threshold
             ↓
        ✅ FINAL OUTPUT
        ```
        """)
        
        st.markdown("---")
        
        # Technology Stack
        st.markdown("""
        **TECH STACK**
        
        **🤖 AI Models:**
        • OpenAI GPT-4.1
        • Advanced reasoning
        
        **🔍 Research:**
        • Tavily Search API
        • Real-time web data
        
        **🏗️ Backend:**
        • Python 3.11+
        • Modular architecture
        
        **🖥️ Frontend:**
        • Streamlit framework
        • Responsive design
        
        **⚙️ Features:**
        • Dynamic search strategy
        • Quality assurance
        • Self-improvement
        • Multi-language support
        """)
        
        st.markdown("---")    
    # System Overview Section
    with st.expander("📋 Detailed System Architecture", expanded=False):
        st.markdown("""
        ### Technical Implementation Details
        
        **Core Technologies:**
        - **Frontend**: Streamlit (Python web framework)
        - **AI Models**: OpenAI GPT-4.1 for content generation & analysis
        - **Web Research**: Tavily API for intelligent web search
        - **Backend**: Python with modular component architecture
        
        **Intelligent Pipeline (5-Stage Process):**
        
        1. **Smart Search Planning** → AI analyzes topic type and creates targeted search queries
        2. **Web Research Execution** → Tavily API searches internet with custom queries  
        3. **Content Quality Filtering** → Filters low-quality/irrelevant content automatically
        4. **Newsletter Generation** → OpenAI generates professional newsletter from curated research
        5. **Quality Control & Auto-Improvement** → Scores content (0-50), auto-rewrites if score < 35
        
        **Key Differentiators:**
        - **Dynamic Search Strategy**: Unlike static search tools, AI customizes search approach per topic
        - **Quality Assurance**: Professional scoring system prevents low-quality outputs  
        - **Self-Improving**: Automatically detects and fixes poor content without human intervention
        - **Multi-language Support**: Detects input language and responds accordingly
        
        **Component Architecture:**
        ```
        app.py (Interface) → smart_searcher.py → scraper.py → llm.py → quality_checker.py → self_fixer.py
        ```
        """)
    
    # Main Application Interface
    st.markdown("---")
    
    # Simple topic input
    topic = st.text_input("Enter newsletter topic:")
    
    # Simple generate button
    if st.button("Generate Newsletter"):
        if topic:
            try:
                # Get articles
                st.write("🔍 Planning search strategy...")
                search_strategy = smart_search_brain(topic)  
                
                st.write("📡 Researching web content...")
                search_results = get_latest_articles(topic, search_strategy)   

                if not search_results:
                    st.error("No quality content found. Try a different topic.")
                    return
                
                # Generate newsletter
                st.write("✍️ Generating newsletter...")
                newsletter = generate_newsletter(search_results, topic)
                
                st.write("📊 Quality control check...")
                quality_check = smart_teacher_check(newsletter, topic)
                
                st.write("🔧 Auto-improvement processing...")
                final_newsletter = fix_newsletter(newsletter, topic, quality_check)
                
                # Display result
                st.success("Newsletter generated!")
                

                
                st.markdown("### Newsletter")
                st.markdown(final_newsletter)
                
            except Exception as e:
                st.error(f"System error: {str(e)}")
        else:
            st.error("Please enter a topic")

if __name__ == "__main__":
    main() 