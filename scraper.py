from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Tavily client
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

def search_synthesis_approach(topic):
    """Let the search engine do the heavy lifting"""
    
    print(f"🔍 Searching for content about: {topic}")
    
    # 1. Multiple targeted searches 
    searches = [
        f"latest {topic} news 2024",
        f"{topic} breakthroughs recent developments", 
        f"{topic} industry trends analysis"
    ]
    
    all_content = []
    for search_query in searches:
        print(f"   Searching: {search_query}")
        
        response = tavily_client.search(
            query=search_query,
            search_depth="advanced",
            max_results=3,
            include_answer=True,  # This is KEY - Tavily's AI summary
            time_range="w"
        )
        
        # Collect Tavily's AI-generated answers + top article summaries
        all_content.append({
            'query': search_query,
            'ai_summary': response.get('answer', ''),
            'top_articles': [r['content'] for r in response['results'][:2]]
        })
    
    print(f"✅ Found content from {len(all_content)} search angles")
    return all_content

# Simple wrapper function to match your existing main.py
def get_latest_articles(topic):
    """Simple wrapper that returns the new smart search results"""
    return search_synthesis_approach(topic)