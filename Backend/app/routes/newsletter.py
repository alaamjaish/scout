# app/routes/newsletter.py

# 1. We import APIRouter instead of FastAPI
from fastapi import APIRouter, HTTPException

# All the specific imports this endpoint needs are now here
from ..models import NewsletterRequest, NewsletterResponse
from ..logic.smart_searcher import smart_search_brain
from ..logic.scraper import get_latest_articles
from ..logic.llm import generate_newsletter
from ..logic.quality_checker import smart_teacher_check
from ..logic.self_fixer import fix_newsletter

QUALITY_THRESHOLD = 35

# 2. We create a Router, which is like a "mini" FastAPI app
router = APIRouter()

# 3. We use @router.post instead of @app.post
@router.post("/generate-newsletter", response_model=NewsletterResponse)
async def generate_newsletter_endpoint(request: NewsletterRequest):
    """
    Receives a topic, generates a newsletter through a multi-step
    quality-controlled process, and returns the final result.
    """
    # NOTE: The entire function body is exactly the same as before!
    # No changes are needed to your core workflow.
    topic = request.topic
    print(f"🔥 [1/5] Received request for topic: {topic}")

    try:
        print("🧠 [2/5] Planning search strategy...")
        search_strategy = smart_search_brain(topic)

        print("📡 [3/5] Researching web content...")
        search_results = await get_latest_articles(topic, search_strategy)

        if not search_results:
            raise HTTPException(status_code=404, detail="Could not find enough high-quality content on this topic.")

        print("✍️ [4/5] Generating first draft...")
        newsletter_draft = await generate_newsletter(search_results, topic)

        print("📊 [5/5] Performing quality control...")
        quality_report = await smart_teacher_check(newsletter_draft, topic)
        print(f"  Initial quality score: {quality_report.get('total_score', 'N/A')}/50")

        final_newsletter = newsletter_draft
        if quality_report.get("total_score", 0) < QUALITY_THRESHOLD:
            print(f"⚠️ Quality score below {QUALITY_THRESHOLD}. Attempting to self-fix...")
            final_newsletter = await fix_newsletter(newsletter_draft, topic, quality_report)
            print("✅ Self-fix complete.")
        else:
            print("✅ Quality score is sufficient. No fixing needed.")
        
        return NewsletterResponse(
            topic=topic,
            final_newsletter=final_newsletter,
            quality_report={
                "total_score": quality_report.get("total_score", 0),
                "emoji": quality_report.get("emoji", "🤷‍♀️"),
                "harsh_verdict": quality_report.get("harsh_verdict", "N/A")
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")