"""
Pydantic models for API data validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class NewsletterRequest(BaseModel):
    """Request model for newsletter generation."""
    topic: str = Field(..., min_length=1, max_length=200, description="Topic for newsletter generation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Artificial Intelligence trends 2025"
            }
        }


class QualityScore(BaseModel):
    """Quality assessment scores."""
    topic_relevance: int = Field(..., ge=0, le=10)
    engagement: int = Field(..., ge=0, le=10)
    information_value: int = Field(..., ge=0, le=10)
    writing_quality: int = Field(..., ge=0, le=10)
    credibility: int = Field(..., ge=0, le=10)


class QualityCheck(BaseModel):
    """Quality check result."""
    total_score: int = Field(..., ge=0, le=50)
    scores: QualityScore
    critical_analysis: str
    harsh_verdict: str
    specific_improvements: str
    confidence_level: str
    emoji: str


class SearchStrategy(BaseModel):
    """Search strategy details."""
    topic_type: str
    why_this_type: str
    search_queries: List[str]
    search_strategy: str


class NewsletterResponse(BaseModel):
    """Response model for newsletter generation."""
    newsletter: str = Field(..., description="Generated newsletter content")
    quality_score: int = Field(..., ge=0, le=50, description="Quality score out of 50")
    quality_check: QualityCheck = Field(..., description="Detailed quality assessment")
    search_strategy: SearchStrategy = Field(..., description="Search strategy used")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "newsletter": "**AI Revolution: The Future is Now**\n\nArtificial Intelligence continues to reshape...",
                "quality_score": 42,
                "quality_check": {
                    "total_score": 42,
                    "scores": {
                        "topic_relevance": 9,
                        "engagement": 8,
                        "information_value": 9,
                        "writing_quality": 8,
                        "credibility": 8
                    },
                    "critical_analysis": "Strong technical content with good examples",
                    "harsh_verdict": "Solid professional newsletter",
                    "specific_improvements": "Add more recent statistics",
                    "confidence_level": "High",
                    "emoji": "✅ SOLID"
                },
                "search_strategy": {
                    "topic_type": "Technology",
                    "why_this_type": "AI is a rapidly evolving technology field",
                    "search_queries": ["AI trends 2025", "machine learning breakthroughs"],
                    "search_strategy": "Focus on recent developments and expert opinions"
                },
                "processing_time": 15.2,
                "timestamp": "2025-01-15T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Newsletter generation failed",
                "detail": "OpenAI API key is invalid",
                "timestamp": "2025-01-15T10:30:00Z"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(default_factory=datetime.now)
    services: Dict[str, str] = Field(..., description="Service health status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "3.0.0",
                "timestamp": "2025-01-15T10:30:00Z",
                "services": {
                    "openai": "healthy",
                    "tavily": "healthy",
                    "core_modules": "healthy"
                }
            }
        } 