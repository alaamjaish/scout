import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from Backend.quality_checker import smart_teacher_check, print_report_card

load_dotenv()

def get_openai_client():
    """Get our AI helper"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Need your OpenAI key!")
    return OpenAI(api_key=api_key)

def fix_newsletter(bad_newsletter, topic, teacher_feedback):
    """
    Takes a bad newsletter and teacher feedback, returns improved version
    """
    client = get_openai_client()
    
    # PROFESSIONAL NEWSLETTER REWRITE PROMPT
    fixer_prompt = f"""
You are a senior newsletter editor for a professional publication like The Economist or Wall Street Journal.

CRITICAL LANGUAGE REQUIREMENT:
- The topic "{topic}" is in a specific language
- Detect that language and write your ENTIRE response in the SAME language
- If "{topic}" is Arabic, respond in Arabic
- If "{topic}" is Spanish, respond in Spanish
- NEVER change the language - maintain consistency

TASK: Rewrite this newsletter about "{topic}" to meet professional journalism standards.

ORIGINAL NEWSLETTER:
{bad_newsletter}

CRITICAL FEEDBACK TO ADDRESS:
- Score: {teacher_feedback.get('total_score', 0)}/50
- Critical Analysis: {teacher_feedback.get('critical_analysis', 'Issues found')}
- Professional Verdict: {teacher_feedback.get('harsh_verdict', 'Needs improvement')}
- Required Improvements: {teacher_feedback.get('specific_improvements', 'Fix issues')}

PROFESSIONAL REWRITE REQUIREMENTS:

1. LANGUAGE CONSISTENCY: 
   - Write in the SAME language as "{topic}"
   - Use professional journalism terms in that language

2. FACTUAL RIGOR:
- Include specific numbers, dates, company names, studies
- NO vague statements like "many experts" - name them
- Replace "imagine" and "could" with concrete examples

3. PROFESSIONAL TONE:
- NO exclamation points except quotes
- NO words like "exciting", "amazing", "incredible" 
- NO "Welcome to..." or "dive into" openings
- Write like The Economist: crisp, factual, slightly dry

4. STRUCTURE:
- Start with hard news/data point, not fluff
- 2-3 specific examples with numbers
- End with concrete implications, not cheerleading

5. BANNED AI PHRASES:
- "Welcome to a new chapter"
- "isn't just a buzzword"  
- "more exciting than ever"
- "the future is now"
- "imagine a world where"
- "stay curious"

6. REQUIRED ELEMENTS:
- At least 3 specific statistics or dates
- Names of real companies/researchers
- Concrete financial or impact numbers

Write a professional newsletter that sounds like it was written by a human journalist, not marketing AI.
FINAL REMINDER: Respond in the SAME language as "{topic}".
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": fixer_prompt}],
            temperature=0.2  # Lower temperature for more professional output
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Newsletter fixer failed: {e}")
        return bad_newsletter
