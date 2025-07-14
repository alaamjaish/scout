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