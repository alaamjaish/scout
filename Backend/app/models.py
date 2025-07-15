# app/models.py

from pydantic import BaseModel

# --- The WHY behind this class ---
# We are defining a "data model". Think of it as a blueprint or a contract.
# By creating this class, we are stating: "Any request to generate a newsletter
# MUST have a body that contains a JSON key called 'topic', and the value
# of that key MUST be a string."
#
# pydantic.BaseModel gives our class superpowers for data validation.
class NewsletterRequest(BaseModel):
    topic: str




# --- New, more detailed model for the quality report ---
class QualityReportModel(BaseModel):
    total_score: int
    emoji: str
    harsh_verdict: str



# --- The WHY behind this new class ---
# We are defining the blueprint for our API's response (OUTPUT).
# This tells the frontend developer: "If your request is successful, I
# guarantee you will get a JSON object back that has a key called
# 'final_newsletter', and its value will be a string."
# This also shows up automatically in the /docs!
class NewsletterResponse(BaseModel):
    final_newsletter: str
    quality_report: QualityReportModel
    topic: str


