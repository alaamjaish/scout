# app/main.py

from fastapi import FastAPI, HTTPException

# Import our data models
from .models import NewsletterRequest, NewsletterResponse
from fastapi.middleware.cors import CORSMiddleware

# This is a constant from your master reference. Good practice to define it here.
QUALITY_THRESHOLD = 35  # This is the minimum score for a newsletter to be considered good

# --- The WHY behind these imports ---
# We are now importing ALL the necessary functions (our "tools")
# from our logic folder so we can use them in our endpoint.
from .logic.smart_searcher import smart_search_brain
from .logic.scraper import get_latest_articles
from .logic.llm import generate_newsletter
from .logic.quality_checker import smart_teacher_check
from .logic.self_fixer import fix_newsletter

# 1. Create our FastAPI application.
app = FastAPI(title="Scout Newsletter API")

# 2. Define the origins that are allowed to connect.
#    For development, we'll allow our future React app's default port.
#    This is a security feature that prevents other websites from making requests to our API.
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# 3. Add the CORS middleware to our application.
#    This piece of code acts as a gatekeeper for all incoming requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

# 4. Define our first endpoint.
#    This is a simple GET request that returns a welcome message.
#    It's a good way to test if our server is running.
@app.get("/")
def read_root():
    return {"message": "Welcome to the Scout Newsletter API! The server is running."}


# --- The WHY behind "response_model=NewsletterResponse" ---
# This is another FastAPI superpower. We are telling our endpoint: "After all
# your logic is done, the final object you return MUST conform to the
# 'NewsletterResponse' model." If our function accidentally returns extra
# data, FastAPI will automatically filter it out, ensuring the frontend
# only ever receives the clean, expected output.
@app.post("/generate-newsletter", response_model=NewsletterResponse)
async def generate_newsletter_endpoint(request: NewsletterRequest):
    """
    Receives a topic, generates a newsletter through a multi-step
    quality-controlled process, and returns the final result.
    """
    topic = request.topic
    print(f"🔥 [1/5] Received request for topic: {topic}")

    try:
        # --- The Full Assembly Line ---
        # Each step calls a function from our logic folder, printing its
        # progress to the console.

        print("🧠 [2/5] Planning search strategy...")
        search_strategy = smart_search_brain(topic)

        print("📡 [3/5] Researching web content...")
        search_results = await get_latest_articles(topic, search_strategy)

        if not search_results:
            print("❌ No quality content found. Aborting.")
            # We raise a specific, user-friendly error.
            raise HTTPException(status_code=404, detail="Could not find enough high-quality content on this topic. Please try another topic.")

        print("✍️ [4/5] Generating first draft...")
        newsletter_draft = await generate_newsletter(search_results, topic)

        print("📊 [5/5] Performing quality control...")
        quality_report = await smart_teacher_check(newsletter_draft, topic)
        print(f"  Initial quality score: {quality_report.get('total_score', 'N/A')}/50")

        final_newsletter = newsletter_draft
        # This is the conditional logic from your original plan
        if quality_report.get("total_score", 0) < QUALITY_THRESHOLD:
            print(f"⚠️ Quality score below {QUALITY_THRESHOLD}. Attempting to self-fix...")
            final_newsletter = await fix_newsletter(newsletter_draft, topic, quality_report)
            print("✅ Self-fix complete.")
        else:
            print("✅ Quality score is sufficient. No fixing needed.")

        # Finally, we return the data in the shape of our response model.
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
        # Re-raise HTTP exceptions directly so FastAPI handles them
        raise e
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")