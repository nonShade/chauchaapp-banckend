"""
Controlador para Daily Tips endpoints.

Routes:
    - GET  /tips/today       - Obtener los tips del dia
    - GET  /tips/all         - Obtener todos los tips activos
    - POST /tips/generate   - Generar 7 tips
"""

from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.modules.daily_tips.service import DailyTipService
from app.modules.daily_tips.dto import (
    DailyTipCreate,
    DailyTipResponse,
    DailyTipBatchResponse,
)
from app.agent.daily_tips_agent import daily_tips_agent

router = APIRouter(prefix="/tips", tags=["daily-tips"])


@router.get(
    "/today",
    response_model=DailyTipResponse,
    summary="Obtener el consejo financiero de hoy",
    description="Devuelve el consejo correspondiente al día de la semana actual",
)
def get_today_tip(db: Session = Depends(get_db)) -> DailyTipResponse:
    """
    Obtener el consejo financiero de hoy.
    El consejo se selecciona basándose en el día actual de la semana (0=Lunes, ..., 6=Domingo).
    """
    service = DailyTipService(db)

    # Obtener el día de la semana actual (0 = Lunes)
    today_day = date.today().weekday()

    tip = service.get_today_tip(today_day)
    if not tip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay consejo disponible para hoy. Por favor genera un nuevo lote.",
        )

    return tip


@router.get(
    "/all",
    response_model=DailyTipBatchResponse,
    summary="Obtener todos los consejos activos",
    description="Devuelve los 7 consejos del lote actual",
)
def get_all_tips(db: Session = Depends(get_db)) -> DailyTipBatchResponse:
    """
    Obtener todos los consejos activos del lote actual.
    """
    service = DailyTipService(db)
    batch = service.get_all_active()

    if batch.total_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay consejos disponibles. Por favor genera un nuevo lote.",
        )

    return batch


@router.post(
    "/generate",
    response_model=DailyTipBatchResponse,
    summary="Generar nuevo lote de consejos",
    description="Genera 7 nuevos consejos financieros",
    status_code=status.HTTP_201_CREATED,
)
def generate_tips_batch(db: Session = Depends(get_db)) -> DailyTipBatchResponse:
    """
    Generar un nuevo lote de 7 consejos diarios usando el agente de IA.

    Este endpoint:
    1. Llama a la IA una vez para generar 7 consejos
    2. Los guarda en la base de datos
    3. Desactiva el lote anterior
    4. Devuelve el nuevo lote
    """
    try:
        tips_data = daily_tips_agent.generate_weekly_tips_batch()

        tips_create = [
            DailyTipCreate(
                title=tip.titulo,
                text=tip.texto,
                category=tip.categoria,
                day_of_week=tip.day_of_week if tip.day_of_week is not None else 0,
            )
            for tip in tips_data
        ]

        service = DailyTipService(db)
        batch = service.create_batch(tips_create)

        return batch
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando consejos: {str(e)}",
        )


@router.get(
    "/latest-generation",
    response_model=dict,
    summary="Obtener la fecha de la última generación",
    description="Devuelve cuándo se generó el lote actual",
)
def get_latest_generation(db: Session = Depends(get_db)) -> dict:
    """
    Obtener la fecha de generación del lote actual de consejos.
    """
    service = DailyTipService(db)
    generation_date = service.get_latest_generation_date()

    if not generation_date:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aún no se ha generado ningún lote.",
        )

    return {
        "generated_at": generation_date,
        "days_since_generation": (datetime.utcnow() - generation_date).days,
    }
