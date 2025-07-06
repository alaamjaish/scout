# main.py
import argparse
import os
from datetime import datetime
from scraper import get_latest_articles
from llm import generate_newsletter

def check_api_keys():
    """Verify that required API keys are available"""
    missing_keys = []
    
    if not os.environ.get("TAVILY_API_KEY"):
        missing_keys.append("TAVILY_API_KEY")
    if not os.environ.get("OPENAI_API_KEY"):
        missing_keys.append("OPENAI_API_KEY")
    
    if missing_keys:
        print("❌ Missing required API keys in .env file:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\n💡 Create a .env file with your API keys!")
        return False
    return True

def save_newsletter(content, topic):
    """Save newsletter to file with timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"newsletter_{topic.replace(' ', '_').replace('/', '_')}_{timestamp}.md"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Newsletter saved as: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving newsletter: {e}")
        return None

def run_core_logic(topic=None):
    """
    Runs the main logic for the newsletter generation process.
    """
    print("🚀 Starting Scout Newsletter Generation...")
    print("="*50)
    
    # Check API keys first
    if not check_api_keys():
        return None
    
    # Get topic from CLI or user input
    if not topic:
        topic = input("Enter a topic: ")
    
    print(f"📝 Topic: {topic}")
    print()
    
    try:
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
            
            # Save to file
            saved_file = save_newsletter(newsletter_content, topic)
            if saved_file:
                print(f"✅ Newsletter generation complete! Saved to: {saved_file}")
            else:
                print("✅ Newsletter generation complete!")
                
            return newsletter_content
        else:
            print("❌ Could not fetch search results. Check your API keys and internet connection!")
            return None
            
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        print("🔧 Please check your API keys and try again")
        return None

def main():
    """Main entry point with CLI argument support"""
    parser = argparse.ArgumentParser(description='Scout AI Newsletter Generator')
    parser.add_argument('--topic', '-t', type=str, help='Newsletter topic')
    parser.add_argument('--version', action='version', version='Scout v1.0')
    
    args = parser.parse_args()
    
    # Run the core logic
    result = run_core_logic(args.topic)
    
    if result is None:
        exit(1)  # Exit with error code if failed

if __name__ == "__main__":
    main()

