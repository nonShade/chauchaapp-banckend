"""
News service — business logic layer.
"""

import asyncio
import httpx
from datetime import datetime
from typing import Optional

from app.modules.news.dto import NewsAnalysisItemDTO
from app.modules.news.entities import News, NewsTag, NewsTagMap
from app.modules.news.repository import NewsRepository
from app.external_apis.rss.rss_client import fetch_feed
from app.external_apis.rss.rss_sources import FEEDS
from app.external_apis.rss.rss_mapper import map_entry
from app.agent.news_agent import news_analysis_agent


class NewsService:
    """Business logic for news entities."""

    def __init__(self, repository: NewsRepository):
        self._repository = repository

    def get_news_topics(self) -> list[NewsTag]:
        """Get all available news topics.

        Returns:
            List of news topics.
        """
        topics = self._repository.get_all_news_tags()
        return topics

    async def get_latest_news(self):
        """Obtiene las últimas noticias desde RSS feeds.

        Returns:
            Lista de noticias ordenadas por fecha de publicación.
        """
        async with httpx.AsyncClient() as client:
            tasks = [fetch_feed(client, url) for url in FEEDS]
            feeds = await asyncio.gather(*tasks, return_exceptions=True)

        news = []

        for feed in feeds:
            if isinstance(feed, Exception):
                continue

            source = feed.feed.get("title", "desconocida")

            for entry in feed.entries:
                news.append(map_entry(entry, source))

        news.sort(key=lambda x: x.get("published") or 0, reverse=True)

        unique = {n.get("link"): n for n in news if n.get("link")}

        return list(unique.values())[:50]

    async def analyze_news_for_user(
        self,
        user_profile: dict,
        news_ids: Optional[list] = None,
        limit: int = 10,
        batch_size: int = 3
    ) -> dict:
        """Analiza noticias y genera recomendaciones personalizadas para el usuario.

        Este método:
        1. Obtiene noticias (via RSS o desde la base de datos)
        2. Analiza el impacto financiero considerando el perfil del usuario
        3. Genera recomendaciones accionables

        Args:
            user_profile: Diccionario con el perfil financiero del usuario
            news_ids: IDs específicos de noticias a analizar (opcional)
            limit: Número máximo de noticias a obtener
            batch_size: Tamaño del lote para análisis (máximo 3)

        Returns:
            Diccionario con los análisis generados
        """
        # Obtener noticias
        if news_ids:
            # Obtener desde la base de datos
            news_items = await self._get_news_by_ids(news_ids)
        else:
            # Obtener desde RSS
            news_items = await news_analysis_agent.get_latest_news_with_rss(limit)

        if not news_items:
            return {
                "analisis": [],
                "total_count": 0,
                "analizado_por": "NewsAnalysisAgent",
                "mensaje": "No se encontraron noticias para analizar"
            }

        # Analizar noticias
        analyses = await news_analysis_agent.analyze_news_batch(
            news_items[:batch_size],
            user_profile
        )

        # Convertir a DTO
        analysis_dtos = [
            NewsAnalysisItemDTO(
                titulo=analysis.titulo,
                resumen=analysis.resumen,
                analisis=analysis.analisis,
                impacto_personal=analysis.impacto_personal,
                recomendacion=analysis.recomendacion,
                nivel_urgencia=analysis.nivel_urgencia,
                etiquetas=analysis.etiquetas,
                fuente_url=analysis.fuente_url
            )
            for analysis in analyses
        ]

        return {
            "analisis": analysis_dtos,
            "total_count": len(analysis_dtos),
            "analizado_por": "NewsAnalysisAgent"
        }

    async def _get_news_by_ids(self, news_ids: list) -> list[dict]:
        """Obtiene noticias específicas desde la base de datos.

        Args:
            news_ids: Lista de IDs de noticias

        Returns:
            Lista de noticias
        """
        news_items = self._repository._session.query(News).filter(
            News.news_id.in_(news_ids)
        ).all()

        return [
            {
                "news_id": str(news.news_id),
                "title": news.title,
                "summary": news.summary,
                "content_text": news.content_text,
                "source_url": news.source_url,
                "published_at": news.published_at,
            }
            for news in news_items
        ]

    async def get_latest_news_with_analysis(
        self,
        user_profile: dict,
        limit: int = 5
    ) -> list[dict]:
        """Obtiene noticias recientes con análisis básico.

        Este método combina la obtención de noticias via RSS
        con un análisis básico para el usuario.

        Args:
            user_profile: Perfil del usuario para personalización
            limit: Número máximo de noticias

        Returns:
            Lista de noticias con análisis
        """
        news_items = await self.get_latest_news()
        
        if not news_items:
            return []

        # Tomar solo las primeras 'limit' noticias
        selected_news = news_items[:limit]
        
        # Analizar en un solo lote
        analyses = await news_analysis_agent.analyze_news_batch(
            selected_news,
            user_profile
        )

        # Combinar noticias con análisis
        result = []
        for news, analysis in zip(selected_news, analyses):
            result.append({
                **news,
                "analisis": analysis
            })

        return result
