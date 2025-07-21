# app.py
import streamlit as st
from Logic.scraper import get_latest_articles
from Logic.llm import generate_newsletter
from Logic.smart_searcher import smart_search_brain
from Logic.quality_checker import run_editorial_review # <-- Renamed function
from Logic.self_fixer import run_final_edit # <-- Renamed function

def main():
    st.title("Scout AI Newsletter Generator - Version 6.0")
    st.caption("Editorial Loop: Research → Draft → Review → Fact-Check → Finalize")

    # --- Sidebar remains the same, you can update the text to reflect the new flow ---
    with st.sidebar:
        st.markdown("### 🔧 CurrentSystem Pipeline (V6)")
        st.markdown("---")
        st.markdown("""
        **EDITORIAL LOOP FLOW**
        ```
        📝 USER INPUT
              ↓
        🧠 SMART SEARCHER
              ↓
        🌐 WEB SCRAPER (Pass 1)
              ↓
        ✍️ CONTENT GENERATOR
         (Creates First Draft)
              ↓
        🕵️ AI EDITOR
         (Finds Factual Gaps)
         (Generates New Queries)
              │
              ├─[Good? Done!]
              ↓
        🌐 WEB SCRAPER (Pass 2)
         (Finds Missing Facts)
              ↓
        ✨ FINAL EDITOR
         (Integrates New Facts)
              ↓
        ✅ FINAL OUTPUT
        ```
        """)

    # --- Main Application Interface ---
    st.markdown("---")
    topic = st.text_input("Enter newsletter topic:")

    if st.button("Generate Newsletter"):
        if not topic:
            st.error("Please enter a topic")
            return

        final_newsletter = ""
        new_research = None

        with st.spinner("Running intelligent pipeline... This may take a moment."):
            try:
                # === STAGE 1: DRAFTING PASS ===
                st.write("🧠 Planning initial research strategy...")
                search_strategy = smart_search_brain(topic)
                
                st.write("📡 Performing initial web research (Pass 1)...")
                initial_research = get_latest_articles(topic, search_strategy)

                if not initial_research:
                    st.error("No quality content found in initial search. Try a different topic.")
                    return

                st.write("✍️ Generating first draft...")
                first_draft = generate_newsletter(initial_research, topic)

                # === STAGE 2: EDITORIAL REVIEW PASS ===
                st.write("🕵️ Performing editorial review to find factual gaps...")
                editorial_review = run_editorial_review(first_draft, topic)
                
                st.info(f"**Editor's Verdict:** {editorial_review.get('editorial_summary')} (Score: {editorial_review.get('quality_score')}/50)")

                # === STAGE 3: CONDITIONAL FACT-FINDING PASS ===
                if editorial_review.get("requires_more_research"):
                    st.write("📡 Performing targeted fact-finding (Pass 2)...")
                    gap_queries = [item['new_search_query'] for item in editorial_review.get("gap_analysis", [])]
                    
                    # Create a temporary search strategy for the second pass
                    fact_finding_strategy = {"search_queries": gap_queries}
                    new_research = get_latest_articles(topic, fact_finding_strategy)
                    st.success(f"Found {len(new_research)} new sources to fill gaps.")
                else:
                    st.write("✅ Draft passed editorial review. No fact-finding needed.")


                # === STAGE 4: FINAL EDIT PASS ===
                st.write("✨ Performing final edit...")
                final_newsletter = run_final_edit(first_draft, editorial_review, new_research, topic)

                # Display result
                st.success("Newsletter generation complete!")

            except Exception as e:
                st.error(f"System error: {str(e)}")
                return # Stop execution on error

        st.markdown("---")
        st.markdown("### Final Newsletter")
        st.markdown(final_newsletter)

if __name__ == "__main__":
    main()