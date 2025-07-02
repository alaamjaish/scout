# main.py
from scraper import get_latest_articles
from llm import generate_newsletter

def run_core_logic():
    """
    Runs the main logic for the newsletter generation process.
    """
    print("🚀 Starting Scout Newsletter Generation...")
    print("="*50)
    
    # You can change this topic to anything you want!
    topic = "Breakthroughs in AGI development"
    print(f"📝 Topic: {topic}")
    print()
    
    # Get smart search results (no more messy HTML extraction!)
    search_results = get_latest_articles(topic)
    
    if search_results:
        print()
        newsletter_content = generate_newsletter(search_results, topic)
        
        # Print the final result
        print("\n" + "="*60)
        print("🎉 SCOUT NEWSLETTER GENERATED 🎉")
        print("="*60)
        print(newsletter_content)
        print("="*60)
        print("✅ Newsletter generation complete!")
    else:
        print("❌ Could not fetch search results. Check your API keys!")

if __name__ == "__main__":
    run_core_logic()