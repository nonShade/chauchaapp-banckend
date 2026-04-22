"""
News service — business logic layer.
"""

from app.modules.news.dto import TopicResponseDTO
from app.modules.news.repository import NewsRepository


class NewsService:
    """Business logic for news entities."""

    def __init__(self, repository: NewsRepository):
        self._repository = repository

    def get_news_topics(self) -> list[TopicResponseDTO]:
        """Get all available news topics.
        
        Returns:
            List of news topics.
        """
        topics = self._repository.get_all_news_tags()
        return [
            TopicResponseDTO(id=t.tag_id, name=t.name, description=t.description)
            for t in topics
        ]
