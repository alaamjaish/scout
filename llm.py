# llm.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Don't initialize client at import time - do it when needed
client = None

def get_openai_client():
    """Get OpenAI client, initializing it if needed"""
    global client
    if client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        client = OpenAI(api_key=api_key)
    return client

def generate_newsletter(all_content, topic):
    """
    Generates a newsletter using OpenAI's API from smart search results.
    """
    print("✍️ Generating newsletter with AI...")
    
    # Get client when needed (not at import time)
    openai_client = get_openai_client()
    
    # Build context from the smart search results
    content_summary = ""
    
    # NEW: Check if we have any content at all
    if not all_content:
        print("⚠️ No quality content found - generating with limited context")
        content_summary = f"Limited information available about {topic}. Please provide a brief overview based on general knowledge."
    else:
        for search_result in all_content:
            search_query = search_result['query']
            ai_summary = search_result['ai_summary']
            top_articles = search_result['top_articles']
            
            content_summary += f"SEARCH: {search_query}\n"
            content_summary += f"AI SUMMARY: {ai_summary}\n"
            content_summary += "TOP ARTICLES:\n"
            
            for i, article in enumerate(top_articles, 1):
                content_summary += f"  {i}. {article[:300]}...\n"
            
            content_summary += "\n---\n\n"

    prompt = f"""
You are an expert newsletter writer. Create an engaging newsletter about "{topic}".

CRITICAL LANGUAGE REQUIREMENT: 
- Analyze the language of the topic "{topic}"
- Write your ENTIRE response in the SAME language as the topic
- If topic is in Arabic, respond in Arabic
- If topic is in Spanish, respond in Spanish  
- If topic is in English, respond in English
- NEVER translate the topic - match its language exactly

You have been provided with AI-generated summaries and article excerpts from multiple search angles:

{content_summary}

Please generate a newsletter with:
1. A catchy, attention-grabbing title
2. A brief intro paragraph (2-3 sentences) that hooks the reader
3. 3-4 key insights with bullet points, each highlighting important developments
4. A short conclusion paragraph about what this means for the future

Keep it professional but exciting. Make it feel like insider knowledge.
REMEMBER: Write in the SAME language as "{topic}".
"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": 
                 """
                 You are a skilled newsletter writer who creates compelling, insightful newsletters from research summaries.
                 
                 CRITICAL LANGUAGE RULE:
                 - Always analyze the language of the user's topic
                 - Respond in the EXACT same language as the topic
                 - Never assume English - detect and match the language
                 
                 You are also a very smart newsletter writer, like the newsletter must be super amazing
                 also, try to mention dates and stats if the content is available, don't invent some stats if not available
                 try your best to make the newsletter as amazing as possible
                 """},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        print("✅ Newsletter generated.")
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error generating newsletter: {e}")
        return "Could not generate the newsletter at this time." 
    

# print(generate_newsletter([], "Syria"))