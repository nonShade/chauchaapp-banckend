"""
News module DTOs.

Handles data transfer formatting for endpoints in the News module.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class TopicResponseDTO(BaseModel):
    """Details of a news/educational topic available for selection."""

    id: UUID
    name: str
    description: str

    model_config = {"from_attributes": True}


class NewsAnalysisItemDTO(BaseModel):
    """DTO para un análisis individual de noticia (respuesta de análisis completo)."""

    news_id: str | None = Field(None, description="ID de la noticia en DB")
    titulo: str = Field(..., description="Título de la noticia")
    resumen: str = Field(..., description="Resumen de la noticia")
    analisis: str = Field(..., description="Análisis financiero detallado")
    impacto_personal: str = Field(..., description="Impacto personalizado según perfil financiero")
    recomendacion: str = Field(..., description="Recomendación de acción concreta")
    nivel_urgencia: str = Field(..., description="Nivel de urgencia: 'bajo', 'medio' o 'alto'")
    etiquetas: list[str] = Field(..., description="Categorías relevantes de la noticia")
    fuente_url: str | None = Field(None, description="URL de la fuente original")

    model_config = {"from_attributes": True}


class NewsFullAnalysisResponseDTO(BaseModel):
    """DTO para la respuesta del análisis completo (RSS → DB).
    
    Este endpoint hace TODO:
    1. Obtiene RSS
    2. Analiza con perfil completo
    3. Guarda en DB
    4. Retorna resultados
    """

    success: bool = Field(..., description="Indicador de éxito")
    analyzed_count: int = Field(..., description="Número de noticias analizadas")
    user_profile_summary: dict = Field(..., description="Resumen del perfil usado")
    analyses: list[NewsAnalysisItemDTO] = Field(..., description="Lista de análisis generados")
    message: str | None = Field(None, description="Mensaje informativo")

    model_config = {"from_attributes": True}


class AnalyzedNewsItemDTO(BaseModel):
    """DTO para una noticia YA analizada guardada en DB."""

    news_id: str | None = Field(None, description="ID de la noticia")
    titulo: str = Field(..., description="Título de la noticia")
    summary: str = Field(..., description="Resumen de la noticia")
    source_url: str | None = Field(None, description="URL fuente")
    published_at: str | None = Field(None, description="Fecha de publicación")
    analisis: str = Field(..., description="Análisis financiero")
    impacto_personal: str = Field(..., description="Impacto personalizado")
    recomendacion: str = Field(..., description="Recomendación")
    nivel_urgencia: str = Field(..., description="Nivel de urgencia")
    etiquetas: list[str] = Field(..., description="Categorías")
    analizado_el: str | None = Field(None, description="Fecha del análisis")

    model_config = {"from_attributes": True}


class AnalyzedNewsListResponseDTO(BaseModel):
    """DTO para obtener TODAS las noticias YA analizadas del usuario.
    
    Este endpoint NO analiza nada nuevo.
    Solo retorna lo que YA está guardado en la base de datos.
    """

    success: bool = Field(..., description="Indicador de éxito")
    total_count: int = Field(..., description="Total de noticias analizadas")
    analyses: list[AnalyzedNewsItemDTO] = Field(..., description="Noticias ya analizadas")

    model_config = {"from_attributes": True}
