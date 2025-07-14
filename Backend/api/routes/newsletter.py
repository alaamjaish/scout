"""
Newsletter generation API routes.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import time
import asyncio
from typing import Dict, Any

# Import your existing core functions (NO CHANGES NEEDED!)
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
    ErrorResponse,
    QualityCheck,
    SearchStrategy,
    QualityScore
)

# Create router
router = APIRouter()

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
        specific_improvements=quality_check.get('specific_improvements', ''),
        confidence_level=quality_check.get('confidence_level', ''),
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

@router.post("/generate-newsletter", response_model=NewsletterResponse)
async def generate_newsletter_endpoint(request: NewsletterRequest):
    """
    Generate a professional newsletter using AI-powered research and quality control.
    
    This endpoint orchestrates the entire 5-stage pipeline:
    1. Smart Search Planning - AI analyzes topic and creates targeted search queries
    2. Web Research - Executes intelligent web searches with quality filtering
    3. Content Generation - Creates professional newsletter content
    4. Quality Assessment - Scores content using professional standards (0-50)
    5. Auto-Improvement - Automatically fixes content below quality threshold
    
    Returns a complete newsletter with quality metrics and processing details.
    """
    start_time = time.time()
    
    try:
        topic = request.topic.strip()
        
        if not topic:
            raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
        # Stage 1: Smart Search Planning
        # YOUR EXISTING FUNCTION - NO CHANGES!
        search_strategy = smart_search_brain(topic)
        
        # Stage 2: Web Research with Quality Filtering  
        # YOUR EXISTING FUNCTION - NO CHANGES!
        search_results = get_latest_articles(topic, search_strategy)
        
        if not search_results:
            raise HTTPException(
                status_code=404, 
                detail="No quality content found for the specified topic. Please try a different topic."
            )
        
        # Stage 3: Content Generation
        # YOUR EXISTING FUNCTION - NO CHANGES!
        newsletter = generate_newsletter(search_results, topic)
        
        # Stage 4: Quality Assessment
        # YOUR EXISTING FUNCTION - NO CHANGES!
        quality_check = smart_teacher_check(newsletter, topic)
        
        # Stage 5: Auto-Improvement
        # YOUR EXISTING FUNCTION - NO CHANGES!
        final_newsletter = fix_newsletter(newsletter, topic, quality_check)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Convert to API models
        quality_check_model = convert_quality_check_to_model(quality_check)
        search_strategy_model = convert_search_strategy_to_model(search_strategy)
        
        # Return structured response
        return NewsletterResponse(
            newsletter=final_newsletter,
            quality_score=quality_check.get('total_score', 0),
            quality_check=quality_check_model,
            search_strategy=search_strategy_model,
            processing_time=round(processing_time, 2)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Newsletter generation error: {str(e)}")
        
        # Return user-friendly error
        raise HTTPException(
            status_code=500,
            detail=f"Newsletter generation failed: {str(e)}"
        )

@router.get("/test-connection")
async def test_connection():
    """Test endpoint to verify API is working."""
    return {
        "status": "success",
        "message": "Newsletter API is working correctly",
        "version": "3.0.0",
        "endpoints": {
            "generate_newsletter": "/api/generate-newsletter",
            "test_connection": "/api/test-connection"
        }
    }

@router.post("/quality-check-only")
async def quality_check_only(content: str, topic: str):
    """
    Standalone quality check endpoint for testing the quality assessment system.
    """
    try:
        # YOUR EXISTING FUNCTION - NO CHANGES!
        quality_check = smart_teacher_check(content, topic)
        
        # Convert to API model
        quality_check_model = convert_quality_check_to_model(quality_check)
        
        return {
            "quality_score": quality_check.get('total_score', 0),
            "quality_check": quality_check_model
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quality check failed: {str(e)}"
        ) 