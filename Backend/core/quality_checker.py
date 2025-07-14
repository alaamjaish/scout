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

def smart_teacher_check(newsletter_content, topic):
    """
    CRITICAL NEWSLETTER EVALUATOR - Uses evidence-based techniques to avoid positivity bias
    
    Implements:
    - Convergent thinking prompts
    - Adversarial self-critique 
    - Professional standards
    - Temporal context awareness
    """
    
    client = get_openai_client()
    
    # Get current date for context
    now = datetime.now()
    current_date = now.strftime("%B %d, %Y")
    current_year = now.year
    
    # EVIDENCE-BASED CRITICAL EVALUATION PROMPT
    teacher_prompt = f"""
    🔍 CRITICAL NEWSLETTER EVALUATION SYSTEM 🔍
    
    CURRENT DATE: {current_date}
    
    You are a PROFESSIONAL newsletter editor with 10+ years experience. Your job is to CRITICALLY evaluate content against industry standards. You are known for being TOUGH but FAIR.
    
    EVALUATION TARGET: Newsletter about "{topic}"
    
    NEWSLETTER CONTENT:
    {newsletter_content}
    
    === CRITICAL EVALUATION PROTOCOL ===
    
    STEP 1 - ADVERSARIAL ANALYSIS:
    First, actively look for PROBLEMS. What would a harsh critic say about this newsletter?
    - What's missing or weak?
    - What claims lack evidence?
    - What would bore readers?
    - What feels generic or AI-generated?
    
    STEP 2 - PROFESSIONAL STANDARDS CHECK:
    Compare against {current_year} newsletter best practices:
    - Topic Relevance (0-10): Is this TRULY about {topic}? Deduct points for tangents, filler content, or vague connections.
    - Engagement Quality (0-10): Would busy professionals actually READ this? Be harsh - most newsletters are skipped.
    - Information Value (0-10): Does this teach something NEW and USEFUL? Generic information = low score.
    - Writing Quality (0-10): Is this crisp, clear, and compelling? Punish wordiness, clichés, or weak transitions.
    - Credibility (0-10): Are claims backed by recent data, sources, or expert opinions? Speculation = point deduction.
    
    STEP 3 - CONVERGENT SCORING:
    Think step-by-step about EACH dimension. What specific evidence supports each score?
    
    === HARSH SCORING GUIDELINES ===
    • 9-10 points: EXCEPTIONAL - Top 5% of newsletters you've seen
    • 7-8 points: SOLID - Good enough for professional publication  
    • 5-6 points: MEDIOCRE - Needs significant improvement
    • 3-4 points: POOR - Major problems, would not publish
    • 0-2 points: UNACCEPTABLE - Complete rewrite needed
    
    DEFAULT ASSUMPTION: Most AI-generated content scores 5-6/10. Prove it deserves higher.
    
    REQUIRED OUTPUT FORMAT (JSON only):
    {{
        "critical_analysis": "What are the main weaknesses you found?",
        "scores": {{
            "topic_relevance": X,
            "engagement": X,
            "information_value": X,
            "writing_quality": X,
            "credibility": X
        }},
        "total_score": X,
        "confidence_level": "How confident are you in this assessment? (Low/Medium/High)",
        "harsh_verdict": "Your brutally honest professional opinion",
        "specific_improvements": "3 specific, actionable fixes needed"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": teacher_prompt}],
            temperature=0.1  # Low temperature for consistent critical evaluation
        )
        
        # Get the critical feedback
        teacher_feedback = json.loads(response.choices[0].message.content)
        
        # Add harsh grading emoji based on score
        total_score = teacher_feedback["total_score"]
        if total_score >= 45:
            teacher_feedback["emoji"] = "🏆 EXCEPTIONAL"
        elif total_score >= 35:
            teacher_feedback["emoji"] = "✅ SOLID"
        elif total_score >= 25:
            teacher_feedback["emoji"] = "⚠️ MEDIOCRE"
        elif total_score >= 15:
            teacher_feedback["emoji"] = "❌ POOR"
        else:
            teacher_feedback["emoji"] = "💀 UNACCEPTABLE"
            
        return teacher_feedback
        
    except Exception as e:
        print(f"😵 Critical evaluator failed: {e}")
        return {
            "total_score": 20,  # Harsh default - assume problems
            "harsh_verdict": "Evaluation system failed - assume content needs work",
            "emoji": "🤷‍♀️ SYSTEM ERROR"
        }

def print_report_card(feedback):
    """Print the critical evaluation report"""
    print("\n🔍 CRITICAL NEWSLETTER EVALUATION 🔍")
    print("=" * 50)
    print(f"📊 TOTAL SCORE: {feedback['total_score']}/50")
    print(f"🎯 VERDICT: {feedback['emoji']}")
    
    if 'confidence_level' in feedback:
        print(f"📈 CONFIDENCE: {feedback['confidence_level']}")
    
    if 'critical_analysis' in feedback:
        print(f"\n🔍 CRITICAL ANALYSIS:")
        print(f"   {feedback['critical_analysis']}")
    
    if 'harsh_verdict' in feedback:
        print(f"\n💭 PROFESSIONAL VERDICT:")
        print(f"   {feedback['harsh_verdict']}")
    
    if 'specific_improvements' in feedback:
        print(f"\n🛠️ REQUIRED IMPROVEMENTS:")
        print(f"   {feedback['specific_improvements']}")
    
    # Show detailed scores if available
    if 'scores' in feedback:
        print(f"\n📋 DETAILED BREAKDOWN:")
        for category, score in feedback['scores'].items():
            print(f"   {category.replace('_', ' ').title()}: {score}/10")
    
    print("=" * 50)


# x = """
# **Syria Unveiled: Navigating the Crossroads of Conflict and Hope**

# Syria remains one of the most complex and compelling stories of the 21st century. From its ancient heritage to modern-day struggles, understanding Syria is key to grasping broader geopolitical shifts and humanitarian challenges shaping the Middle East today.

# **Key Insights into Syria’s Current Landscape:**

# - **Ongoing Conflict and Fragile Ceasefires:** Despite multiple ceasefire agreements since 2018, pockets of violence persist across Syria, especially in the northwest region of Idlib. The delicate balance between government forces, opposition groups, and foreign actors continues to define the country’s security dynamics.

# - **Humanitarian Crisis at Scale:** Over 13 million Syrians—more than half the population—remain in dire need of humanitarian aid as of early 2024. Displacement, food insecurity, and access to healthcare are critical concerns, with international agencies striving to deliver assistance amid logistical and political hurdles.

# - **Reconstruction Efforts and Economic Struggles:** Syria’s infrastructure has suffered immense damage, with estimates suggesting that over $400 billion is needed for full reconstruction. Economic sanctions, inflation, and limited foreign investment are major obstacles hindering recovery and stabilization efforts.

# - **Geopolitical Chessboard:** Syria remains a hotspot for regional and global powers, including Russia, Iran, Turkey, and the United States, each pursuing strategic interests. This intricate web of alliances and rivalries continues to influence peace negotiations and the broader Middle Eastern balance of power.

# **Looking Ahead:**

# Syria stands at a pivotal juncture—where the interplay of diplomacy, humanitarian aid, and reconstruction will determine whether it can transition from protracted conflict to sustainable peace. The coming years will be crucial in shaping not only Syria’s future but also the stability of the entire region. Staying informed and engaged is essential as this multifaceted story unfolds.
# """

# test_newsletter = smart_teacher_check(x, "Syria")
# print_report_card(test_newsletter)