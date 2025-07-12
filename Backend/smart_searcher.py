import json
from openai import OpenAI
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    """Get our AI helper"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Need your OpenAI key!")
    return OpenAI(api_key=api_key)

def smart_search_brain(topic):
    """
    This is like having a really smart librarian who knows exactly 
    where to look for different types of information!
    
    Instead of always searching the same way, this function figures out:
    - What TYPE of topic this is (news, science, business, etc.)
    - What are the BEST search angles for this topic
    - What WORDS will find the most interesting stuff
    """
    
    client = get_openai_client()
    
    # Get current date info
    now = datetime.now()
    current_date = now.strftime("%B %d, %Y")  # "January 15, 2025"
    current_year = now.year                   # 2025
    current_month = now.strftime("%B")        # "January"
    
    # Updated prompt with date awareness
    search_brain_prompt = f"""
    🧠 SMART SEARCH BRAIN 🧠
    
    CURRENT DATE: {current_date}
    CURRENT YEAR: {current_year}
    
    I need to research "{topic}" and write an awesome newsletter about it.
    
    Help me figure out the BEST way to search for this topic:
    
    1. First, tell me what TYPE of topic this is:
       - News/Current Events (like "AI regulation" or "election {current_year}")
       - Science/Technology (like "quantum computing" or "space exploration") 
       - Business/Finance (like "cryptocurrency" or "stock market")
       - Health/Lifestyle (like "fitness trends" or "mental health")
       - Entertainment/Culture (like "movies" or "music trends")
       - Other: [specify what type]
    
    2. Then create 5 PERFECT search queries that will find:
       - The most recent news (from {current_year})
       - Expert opinions/analysis  
       - Practical impact/implications
       - Interesting facts/data
       - Future predictions/trends
    
    Make the searches specific to THIS topic AND current timeframe ({current_year})!
    Use "{current_year}" in your search queries when looking for recent information.
    
    Give me back EXACTLY this format:
    {{
        "topic_type": "What type of topic this is",
        "why_this_type": "Brief explanation of why you chose this type",
        "search_queries": [
            "Specific search query 1 with {current_year} if relevant",
            "Specific search query 2", 
            "Specific search query 3",
            "Specific search query 4",
            "Specific search query 5"
        ],
        "search_strategy": "Brief explanation of your search strategy"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",  # Our smart search brain
            messages=[{"role": "user", "content": search_brain_prompt}],
            temperature=0.7  # Creative but focused
        )
        
        # Get the search strategy
        search_strategy = json.loads(response.choices[0].message.content)
        
        print(f"🧠 Smart Search Brain says:")
        print(f"   📂 Topic Type: {search_strategy['topic_type']}")
        print(f"   💡 Why: {search_strategy['why_this_type']}")
        print(f"   🎯 Strategy: {search_strategy['search_strategy']}")
        print(f"   🔍 Found {len(search_strategy['search_queries'])} smart searches!")
        
        return search_strategy
        
    except Exception as e:
        print(f"😵 Search brain got confused: {e}")
        # Fallback to basic searches if AI fails
        return {
            "topic_type": "General",
            "search_queries": [
                f"latest {topic} news 2025",
                f"{topic} expert analysis",
                f"{topic} trends and insights",
                f"{topic} future predictions",
                f"{topic} practical applications"
            ],
            "search_strategy": "Using basic search approach as backup"
        }


# print(smart_search_brain("Syria"))