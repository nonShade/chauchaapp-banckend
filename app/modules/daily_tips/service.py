from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.daily_tips.entities import DailyTip
from app.modules.daily_tips.repository import DailyTipRepository
from app.modules.daily_tips.dto import (
    DailyTipCreate,
    DailyTipResponse,
    DailyTipBatchResponse,
)


class DailyTipService:
    """Servicio para gestionar consejos diarios."""

    def __init__(self, db: Session):
        """Inicializar servicio con sesión de base de datos."""
        self.db = db
        self.repository = DailyTipRepository(db)

    def create_tip(self, tip_create: DailyTipCreate) -> DailyTipResponse:
        """Crear un solo consejo diario."""
        tip = DailyTip(
            title=tip_create.title,
            text=tip_create.text,
            category=tip_create.category,
            day_of_week=tip_create.day_of_week,
        )
        created_tip = self.repository.create(tip)
        self.db.commit()
        return DailyTipResponse.model_validate(created_tip)

    def create_batch(self, tips_data: list[DailyTipCreate]) -> DailyTipBatchResponse:
        """
        Crear un nuevo lote de consejos, desactivando los antiguos.
        Esto se llama una vez a la semana por el agente.
        """
        self.repository.deactivate_all()

        new_tips = [
            DailyTip(
                title=tip.title,
                text=tip.text,
                category=tip.category,
                day_of_week=tip.day_of_week,
            )
            for tip in tips_data
        ]
        created_tips = self.repository.create_batch(new_tips)
        self.db.commit()

        # Limpiar consejos inactivos antiguos
        self.repository.delete_all_inactive()
        self.db.commit()

        return DailyTipBatchResponse(
            tips=[DailyTipResponse.model_validate(tip) for tip in created_tips],
            total_count=len(created_tips),
            generated_at=datetime.utcnow(),
        )

    def get_all_active(self) -> DailyTipBatchResponse:
        """Obtener todos los consejos activos del lote actual."""
        tips = self.repository.get_all_active()
        return DailyTipBatchResponse(
            tips=[DailyTipResponse.model_validate(tip) for tip in tips],
            total_count=len(tips),
            generated_at=tips[0].generated_at if tips else datetime.utcnow(),
        )

    def get_today_tip(self, day_of_week: int) -> DailyTipResponse | None:
        """Obtener el consejo de hoy basado en el día de la semana (0=Lunes, 7=Domingo)."""
        tip = self.repository.get_today_tip(day_of_week)
        if not tip:
            return None
        return DailyTipResponse.model_validate(tip)

    def get_by_id(self, daily_tip_id: UUID) -> DailyTipResponse | None:
        """Obtener un consejo por ID."""
        tip = self.repository.get_by_id(daily_tip_id)
        if not tip:
            return None
        return DailyTipResponse.model_validate(tip)

    def get_latest_generation_date(self) -> datetime | None:
        """Obtener cuando se generó el lote actual."""
        return self.repository.get_latest_generation_date()
