"""
News module DTOs.

Handles data transfer formatting for endpoints in the News module.
"""

from uuid import UUID

from pydantic import BaseModel


class TopicResponseDTO(BaseModel):
    """Details of a news/educational topic available for selection."""

    id: UUID
    name: str
    description: str

    model_config = {"from_attributes": True}
