# Logic/quality_checker.py
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

def run_editorial_review(newsletter_content, topic):
    """
    Acts as an AI Editor to find factual gaps and generate new search queries.
    """
    client = get_openai_client()
    current_year = datetime.now().year

    editor_prompt = f"""
    You are a meticulous, demanding editor for a top-tier publication like The Economist or Wall Street Journal. Your goal is to find specific, actionable factual gaps in a newsletter draft about "{topic}". Do not just grade it; improve it by identifying what's missing.

    NEWSLETTER DRAFT:
    ---
    {newsletter_content}
    ---
    today's date is {datetime.now().strftime("%Y-%m-%d")}
    Your task is to perform a critical editorial review:

    1.  **Identify Factual Gaps**: Read the draft and find 2-3 specific points that are too vague, lack data, or mention something without providing a concrete example.
        - BAD: "The article is too general."
        - GOOD: "The bullet point mentions 'significant growth' but lacks a specific percentage or dollar amount from {current_year}."
        - GOOD: "It mentions a 'key player' in the industry but fails to name the company."

    2.  **Generate Specific Search Queries**: For EACH factual gap you identify, create one highly targeted search query that a researcher could use to find that exact piece of missing information. The queries should be precise.
        - GAP: "Missing the name of the new AI model." -> QUERY: "OpenAI latest language model name announced {current_year}"
        - GAP: "Lacks specific data on market size." -> QUERY: "global AI market size forecast {current_year} report"

    3.  **Provide a Quality Score**: As a secondary task, provide a standard quality score out of 50 based on the draft's current state. Be harsh.

    Produce your response in a single, valid JSON object. Do NOT include any text outside of the JSON.

    REQUIRED JSON FORMAT:
    {{
      "quality_score": <integer from 0-50>,
      "editorial_summary": "A one-sentence summary of the draft's main weakness.",
      "requires_more_research": <true or false>,
      "gap_analysis": [
        {{
          "gap_description": "Specific description of the first factual gap.",
          "new_search_query": "Targeted search query to find the first missing piece of info."
        }},
        {{
          "gap_description": "Specific description of the second factual gap.",
          "new_search_query": "Targeted search query to find the second missing piece of info."
        }}
      ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[{"role": "user", "content": editor_prompt}],
            temperature=0.2,
            response_format={"type": "json_object"} # Enforce JSON output
        )

        editorial_review = json.loads(response.choices[0].message.content)

        # Simple logic to determine if more research is needed
        if editorial_review.get("quality_score", 50) < 40 and len(editorial_review.get("gap_analysis", [])) > 0:
            editorial_review["requires_more_research"] = True
        else:
            editorial_review["requires_more_research"] = False
            editorial_review["gap_analysis"] = [] # Clear this if no research is needed

        print(f"🕵️ Editorial Review Complete. Score: {editorial_review.get('quality_score')}")
        if editorial_review["requires_more_research"]:
            print(f"   - Identified {len(editorial_review.get('gap_analysis', []))} factual gaps. Needs more research.")
        else:
            print("   - Draft is good. No new research required.")

        return editorial_review

    except Exception as e:
        print(f"😵 Editorial Review failed: {e}")
        return {
            "quality_score": 0,
            "editorial_summary": "Editor AI failed to process.",
            "requires_more_research": False,
            "gap_analysis": []
        }


test_content = """
النشرة التقنية الأسبوعية – تحليل معمق: آفاق هاتف iPhone 17 وتوجهات آبل المستقبلية

أعلنت شركة آبل في تقاريرها المالية للربع الثاني من عام 2024 عن انخفاض مبيعات هواتف iPhone بنسبة 2.4% مقارنة بالفترة نفسها من العام الماضي، وفقاً لبيانات بلومبرغ. في هذا السياق، تتزايد التسريبات حول هاتف iPhone 17 المتوقع إطلاقه في سبتمبر 2025، وسط تساؤلات حول قدرة الشركة على استعادة زخمها في سوق يشهد منافسة متصاعدة من شركات مثل سامسونغ وهواوي.

مواصفات متوقعة مدعومة بمصادر صناعية

وفقاً لتحليل نشرته صحيفة Nikkei Asia في مايو 2024، تعمل آبل على تطوير تصميم أنحف لهاتف iPhone 17، مع تقليص سعة البطارية إلى أقل من 3000 مللي أمبير/ساعة، مقارنة بـ 3274 مللي أمبير/ساعة في iPhone 15. وذكرت شركة Display Supply Chain Consultants (DSCC) أن آبل تجري اختبارات على شاشات قابلة للطي، إلا أن مصادر داخلية في سامسونغ أكدت لموقع The Elec أن الإنتاج التجاري لهذه الشاشات لن يبدأ قبل 2026.

فيما يتعلق بالكاميرا، أفاد المحلل مينغ-تشي كو أن آبل تعتزم رفع دقة الكاميرا الأمامية إلى 24 ميجابكسل، مقارنة بـ 12 ميجابكسل في الطرازات الحالية، مع تحسينات في نظام التصوير الليلي. أما من ناحية الألوان، فقد أشار تقرير صادر عن MacRumors إلى نية الشركة طرح لون نحاسي جديد، في خطوة تهدف إلى استهداف شرائح عمرية أصغر.

مقارنة مع المنافسين وتأثيرات السوق

تأتي هذه التحسينات في ظل استمرار سامسونغ في تطوير هواتفها القابلة للطي، حيث بلغت مبيعات سلسلة Galaxy Z Fold أكثر من 10 ملايين وحدة في 2023، بحسب بيانات Statista. في المقابل، لم تصدر آبل حتى الآن أي هاتف قابل للطي، ما يضعها أمام تحديات تقنية وتسويقية واضحة.

من الناحية المالية، تعتمد آبل على هواتف iPhone في تحقيق أكثر من 50% من إيراداتها السنوية، وفقاً لتقريرها السنوي لعام 2023. أي تغيير جوهري في التصميم أو المواصفات سيؤثر بشكل مباشر على أداء الشركة في الأسواق الرئيسية مثل الولايات المتحدة والصين.

دلالات للمستخدمين والمستثمرين

تشير هذه التطورات إلى أن آبل تركز حالياً على تحسين الكفاءة الطاقية والتصميم، مع تأجيل الابتكارات الجذرية مثل الشاشة القابلة للطي إلى ما بعد 2025. بالنسبة للمستخدمين، قد يعني ذلك دورة تحديث أبطأ ومنافسة أشد من الشركات الآسيوية. أما المستثمرون، فعليهم مراقبة استجابة السوق لهذه التغييرات، خاصة في ظل تباطؤ نمو قطاع الهواتف الذكية عالمياً.

للمزيد من التحليلات المعمقة حول قطاع التكنولوجيا، تابعوا تقاريرنا الأسبوعية المدعومة بالبيانات والمصادر.
"""
test_topic = "هواتف iPhone"
print(run_editorial_review(test_content, test_topic))