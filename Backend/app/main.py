# app/main.py

from fastapi import FastAPI, HTTPException

# Import our new model from the models.py file
from .models import NewsletterRequest

# Import our first logic function
from .logic.smart_searcher import smart_search_brain

app = FastAPI(title="Scout Newsletter API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Scout Newsletter API! The server is running."}


# --- The WHY behind this new endpoint ---
# This is the core endpoint for our app.
#
# @app.post: We use POST instead of GET. WHY?
#   - GET is for retrieving data (like viewing a web page).
#   - POST is for sending data to the server to create a new resource or
#     trigger a process. Since we are asking the server to DO something
#     (generate a newsletter), POST is the correct HTTP method.
#
# request: NewsletterRequest: This is the magic link to Part 1. We tell FastAPI
#   that the body of this POST request should be validated against our
#   NewsletterRequest model. If the frontend sends invalid data (e.g., no topic,
#   or the topic is a number), FastAPI will AUTOMATICALLY reject it with a
#   clear error message. This saves us from writing tons of validation code.
#
@app.post("/generate-newsletter")
def generate_newsletter_endpoint(request: NewsletterRequest):
    """
    Receives a topic, generates a newsletter, and returns it.
    This is the main workflow of the Scout app.
    """
    topic = request.topic
    print(f"🔥 Received request to generate newsletter for topic: {topic}")

    try:
        # --- The WHY behind this 'try...except' block ---
        # Our logic might fail (e.g., an API key is invalid, a website is down).
        # If we don't "try" to catch these errors, our whole server will crash.
        # This block ensures that we handle failures gracefully and send a
        # proper error message back to the frontend instead of just dying.

        # 1. First, we call our smart search brain, just like in your old script.
        search_strategy = smart_search_brain(topic)
        
        # For now, we'll just return this strategy to prove it's working.
        # In the next step, we'll pass this to the scraper.
        print("✅ Smart search strategy generated successfully.")
        return search_strategy

    except Exception as e:
        # If anything in the 'try' block fails, we land here.
        print(f"❌ An error occurred: {e}")
        # HTTPException is a special FastAPI error that sends a properly
        # formatted HTTP error response (in this case, a 500 Internal Server Error).
        raise HTTPException(status_code=500, detail=str(e))