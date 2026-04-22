"""
News controller — HTTP endpoint layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.news.dto import TopicResponseDTO
from app.modules.news.repository import NewsRepository
from app.modules.news.service import NewsService
from app.shared.database import get_db

router = APIRouter(prefix="/v1/news", tags=["News"])


def _get_news_service(db: Session = Depends(get_db)) -> NewsService:
    """Dependency to build news service with its database repository."""
    repository = NewsRepository(db)
    return NewsService(repository)


@router.get(
    "/topics",
    response_model=list[TopicResponseDTO],
    summary="Obtener tópicos de noticias",
    description="Devuelve el catálogo de tópicos de noticias para elegir intereses.",
)
def get_news_topics(service: NewsService = Depends(_get_news_service)):
    """Retrieve all available news tags (topics)."""
    return service.get_news_topics()
