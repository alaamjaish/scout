"""
Newsletter generation API routes.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import time
import asyncio
import json
from typing import Dict, Any

# Import your existing core functions (NO CHANGES NEEDED IN CORE FILES!)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.smart_searcher import smart_search_brain
from core.scraper import get_latest_articles
from core.llm import generate_newsletter
from core.quality_checker import smart_teacher_check
from core.self_fixer import fix_newsletter

# Import API models
from ..models.schemas import (
    NewsletterRequest, 
    NewsletterResponse, 
    QualityCheck,
    SearchStrategy,
    QualityScore
)

router = APIRouter()

# --- Helper functions to convert your pipeline's output to Pydantic models ---
def convert_quality_check_to_model(quality_check: Dict[str, Any]) -> QualityCheck:
    """Convert quality check dict to Pydantic model."""
    scores_dict = quality_check.get('scores', {})
    
    return QualityCheck(
        total_score=quality_check.get('total_score', 0),
        scores=QualityScore(
            topic_relevance=scores_dict.get('topic_relevance', 0),
            engagement=scores_dict.get('engagement', 0),
            information_value=scores_dict.get('information_value', 0),
            writing_quality=scores_dict.get('writing_quality', 0),
            credibility=scores_dict.get('credibility', 0)
        ),
        critical_analysis=quality_check.get('critical_analysis', ''),
        harsh_verdict=quality_check.get('harsh_verdict', ''),
        specific_improvements=quality_check.get('specific_improvements', ''),  # Fixed field name
        confidence_level=quality_check.get('confidence_level', ''),           # Added missing field
        emoji=quality_check.get('emoji', '')
    )

def convert_search_strategy_to_model(strategy: Dict[str, Any]) -> SearchStrategy:
    """Convert search strategy dict to Pydantic model."""
    return SearchStrategy(
        topic_type=strategy.get('topic_type', ''),
        why_this_type=strategy.get('why_this_type', ''),
        search_queries=strategy.get('search_queries', []),
        search_strategy=strategy.get('search_strategy', '')
    )

# --- This is the new async generator for streaming real-time updates ---
async def stream_newsletter_generation(topic: str):
    """
    This generator function executes the 5-stage pipeline and yields
    real-time progress updates in Server-Sent Events (SSE) format.
    """
    start_time = time.time()
    
    async def send_event(event_type: str, data: dict):
        """Helper to format and yield SSE messages."""
        event_data = json.dumps({"type": event_type, "data": data})
        yield f"data: {event_data}\n\n"
        await asyncio.sleep(0.1) # Give a moment for the event to send

    try:
        # Stage 1: Smart Search Planning
        yield await anext(send_event("update", {"stage": 0, "status": "processing"}))
        search_strategy = smart_search_brain(topic)
        yield await anext(send_event("update", {"stage": 0, "status": "completed"}))
        
        # Stage 2: Web Research
        yield await anext(send_event("update", {"stage": 1, "status": "processing"}))
        search_results = get_latest_articles(topic, search_strategy)
        if not search_results:
            raise ValueError("No quality content found for the specified topic.")
        yield await anext(send_event("update", {"stage": 1, "status": "completed"}))

        # Stage 3: Content Generation
        yield await anext(send_event("update", {"stage": 2, "status": "processing"}))
        newsletter = generate_newsletter(search_results, topic)
        yield await anext(send_event("update", {"stage": 2, "status": "completed"}))

        # Stage 4: Quality Assessment
        yield await anext(send_event("update", {"stage": 3, "status": "processing"}))
        quality_check = smart_teacher_check(newsletter, topic)
        yield await anext(send_event("update", {"stage": 3, "status": "completed"}))

        # Stage 5: Auto-Improvement
        yield await anext(send_event("update", {"stage": 4, "status": "processing"}))
        final_newsletter = fix_newsletter(newsletter, topic, quality_check)
        yield await anext(send_event("update", {"stage": 4, "status": "completed"}))

        # All stages complete, prepare and send the final response
        processing_time = time.time() - start_time
        quality_check_model = convert_quality_check_to_model(quality_check)
        search_strategy_model = convert_search_strategy_to_model(search_strategy)

        final_response_data = NewsletterResponse(
            newsletter=final_newsletter,
            quality_score=quality_check.get('total_score', 0),
            quality_check=quality_check_model,
            search_strategy=search_strategy_model,
            processing_time=round(processing_time, 2)
        )
        # Use .model_dump_json() for Pydantic v2
        yield await anext(send_event("final", json.loads(final_response_data.model_dump_json())))

    except Exception as e:
        # If any error occurs, send an error event
        error_data = {"message": f"An error occurred: {str(e)}"}
        yield await anext(send_event("error", error_data))


@router.post("/generate-newsletter")
async def generate_newsletter_endpoint(request: NewsletterRequest):
    """
    Generate a newsletter by streaming real-time updates of the 5-stage pipeline.
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    return StreamingResponse(
        stream_newsletter_generation(request.topic.strip()), 
        media_type="text/event-stream"
    )

# Keep other endpoints like test-connection as they are
@router.get("/test-connection")
async def test_connection():
    return {"status": "success", "message": "API connection is healthy."}