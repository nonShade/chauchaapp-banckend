"""
News repository — data access layer.
"""

from sqlalchemy.orm import Session

from app.modules.news.entities import NewsTag


class NewsRepository:
    """Data access for news topics and entries."""

    def __init__(self, session: Session):
        self._session = session

    def get_all_news_tags(self) -> list[NewsTag]:
        """Get all available news tags (topics).

        Returns:
            A list of NewsTag entities.
        """
        return self._session.query(NewsTag).all()
