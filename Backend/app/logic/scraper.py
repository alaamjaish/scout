# app/logic/scraper.py

from tavily import AsyncTavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# We still only want one client instance, so this part is fine.
tavily_client = None



def get_tavily_client():
    global tavily_client
    if tavily_client is None:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        # CHANGE 2: Create an instance of the Async client
        tavily_client = AsyncTavilyClient(api_key=api_key)
    return tavily_client


# This is an existing synchronous function, we can leave it as is.
def is_content_good(search_result, topic):
    # ... (no changes needed in this function)
    ai_summary = search_result.get('ai_summary', '')
    top_articles = search_result.get('top_articles', [])
    if ai_summary is None: ai_summary = ''
    if top_articles is None: top_articles = []
    if len(ai_summary) < 50: return False
    if "error" in ai_summary.lower() or "404" in ai_summary.lower(): return False
    if "could not" in ai_summary.lower() or "unable to" in ai_summary.lower(): return False
    print("   ✅ Quality check passed")
    return True


# --- The Main Change is Here ---
# We change 'def' to 'async def' to make the function asynchronous
async def get_latest_articles(topic, search_strategy=None):
    """
    Asynchronously searches the web using the Tavily API.
    """
    print(f"🔍 Searching for content about: {topic}")
    client = get_tavily_client()
    
    # Use the smart search queries if available, otherwise use defaults
    searches = search_strategy['search_queries'] if search_strategy and 'search_queries' in search_strategy else [
        f"latest {topic} news 2025", f"{topic} breakthroughs recent developments",
        f"{topic} industry trends analysis", f"{topic} expert opinions research",
        f"{topic} market impact business"
    ]
    
    all_content = []
    for search_query in searches:
        print(f"   Searching (async): {search_query}")
        
        # We 'await' the result of the search call. This is the "pause" point.
        # While our code waits for Tavily, the server can handle other requests.
        response = await client.search(
            query=search_query,
            search_depth="advanced",
            max_results=3,
            include_answer=True,
            time_range="w"
        )
        
        search_result = {
            'query': search_query,
            'ai_summary': response.get('answer', '') if response.get('answer') is not None else '',
            'top_articles': [r.get('content', '') for r in response.get('results', [])[:2] if r.get('content')]
        }
        
        if is_content_good(search_result, topic):
            all_content.append(search_result)
        else:
            print(f"   🗑️ Skipped low-quality result for: {search_query}")
    
    print(f"✅ Found {len(all_content)} high-quality results (after filtering)")
    return all_content