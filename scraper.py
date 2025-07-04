from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

def is_content_good(search_result, topic):
    """Check if search result is high quality and relevant"""
    ai_summary = search_result.get('ai_summary', '')
    top_articles = search_result.get('top_articles', [])
    
    # Handle None values
    if ai_summary is None:
        ai_summary = ''
    if top_articles is None:
        top_articles = []
    
    # Filter out bad content
    if len(ai_summary) < 50:  # Too short
        print("   ❌ Filtered: Summary too short")
        return False
        
    if "error" in ai_summary.lower() or "404" in ai_summary.lower():  # Has errors
        print("   ❌ Filtered: Contains errors")
        return False
        
    if "could not" in ai_summary.lower() or "unable to" in ai_summary.lower():  # Failed to process
        print("   ❌ Filtered: Failed to process")
        return False
    
    # Check topic relevance (simple word matching)
    topic_words = topic.lower().split()
    summary_lower = ai_summary.lower()
    
    matches = sum(1 for word in topic_words if word in summary_lower)
    if matches == 0:  # No topic words found
        print("   ❌ Filtered: Not relevant to topic")
        return False
    
    print("   ✅ Quality check passed")
    return True

# Don't initialize client at import time - do it when needed
tavily_client = None

def get_tavily_client():
    """Get Tavily client, initializing it if needed"""
    global tavily_client
    if tavily_client is None:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        tavily_client = TavilyClient(api_key=api_key)
    return tavily_client

def search_synthesis_approach(topic):
    """Let the search engine do the heavy lifting"""
    
    print(f"🔍 Searching for content about: {topic}")
    
    # Get client when needed (not at import time)
    client = get_tavily_client()
    
    # 1. Multiple targeted searches with diverse angles
    searches = [
        f"latest {topic} news 2025",
        f"{topic} breakthroughs recent developments", 
        f"{topic} industry trends analysis",
        f"{topic} expert opinions research",
        f"{topic} market impact business"
    ]
    
    all_content = []
    for search_query in searches:
        print(f"   Searching: {search_query}")
        
        response = client.search(
            query=search_query,
            search_depth="advanced",
            max_results=3,
            include_answer=True,  # This is KEY - Tavily's AI summary
            time_range="w"
        )
        
        # Create the search result first
        search_result = {
            'query': search_query,
            'ai_summary': response.get('answer', '') if response.get('answer') is not None else '',
            'top_articles': [r.get('content', '') for r in response.get('results', [])[:2] if r.get('content')]
        }
        
        # Only add if it passes quality check
        if is_content_good(search_result, topic):
            all_content.append(search_result)
        else:
            print(f"   🗑️ Skipped low-quality result for: {search_query}")
    
    print(f"✅ Found {len(all_content)} high-quality results (after filtering)")
    return all_content

# Simple wrapper function to match your existing main.py
def get_latest_articles(topic):
    """Simple wrapper that returns the new smart search results"""
    return search_synthesis_approach(topic)

