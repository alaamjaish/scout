# Logic/self_fixer.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    """Get our AI helper"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Need your OpenAI key!")
    return OpenAI(api_key=api_key)

def run_final_edit(original_draft, editorial_review, new_research_content, topic):
    """
    Performs the final edit by integrating new research to fill factual gaps.
    """
    # If the draft was good enough and no new research was fetched, just return the original.
    if not editorial_review.get("requires_more_research", False) or not new_research_content:
        print("✅ No final edit required. Original draft is sufficient.")
        return original_draft

    client = get_openai_client()

    # Format the new research and feedback for the prompt
    gaps_to_fix = "\n".join([f"- GAP: {item['gap_description']}\n  - FOCUSED SEARCH: {item['new_search_query']}" for item in editorial_review.get("gap_analysis", [])])
    new_data = "\n".join([f"- SOURCE: {res['query']}\n  - CONTENT: {res['ai_summary']}" for res in new_research_content])

    final_editor_prompt = f"""
    You are a Senior Editor performing the final rewrite of a newsletter about "{topic}".
    Your task is to create a new, definitive version of the draft by integrating new, targeted research to fill specific factual gaps.

    You have been provided with three pieces of information:

    1.  **THE ORIGINAL DRAFT:**
        ---
        {original_draft}
        ---

    2.  **THE EDITOR'S REQUIRED FIXES (Gaps to Fill):**
        ---
        {gaps_to_fix}
        ---

    3.  **THE NEW RESEARCH (Fact-Finding Results to Integrate):**
        ---
        {new_data}
        ---

    **YOUR INSTRUCTIONS:**

    -   Rewrite the **ENTIRE** newsletter from scratch.
    -   Seamlessly **weave the information from the NEW RESEARCH** into the text to fix the gaps identified by the editor.
    -   **DO NOT** just append the new facts. Integrate them naturally into the narrative.
    -   The final output must be polished, factually dense, and written in a professional tone.
    -   Ensure the final newsletter respects the language of the topic: "{topic}".
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": final_editor_prompt}],
            temperature=0.4 # A bit more creativity for a good rewrite
        )
        final_newsletter = response.choices[0].message.content
        print("✅ Final edit complete. Newsletter has been enriched with new facts.")
        return final_newsletter

    except Exception as e:
        print(f"😵 Final Editor failed: {e}")
        # Return the original draft as a fallback
        return original_draft