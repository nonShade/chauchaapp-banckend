from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_, select

from app.modules.daily_tips.entities import DailyTip


class DailyTipRepository:
    """Repositorio para acceder y gestionar consejos diarios en la base de datos."""

    def __init__(self, db: Session):
        """Inicializar con sesión de base de datos."""
        self.db = db

    def create(self, tip: DailyTip) -> DailyTip:
        """Crear un nuevo consejo diario."""
        self.db.add(tip)
        self.db.flush()
        return tip

    def create_batch(self, tips: list[DailyTip]) -> list[DailyTip]:
        """Crear múltiples consejos diarios en una transacción."""
        self.db.add_all(tips)
        self.db.flush()
        return tips

    def get_by_id(self, daily_tip_id: UUID) -> DailyTip | None:
        """Obtener un consejo diario por ID."""
        return self.db.query(DailyTip).filter(
            DailyTip.daily_tip_id == daily_tip_id
        ).first()

    def get_by_day(self, day_of_week: int, is_active: bool = True) -> DailyTip | None:
        """Obtener el consejo activo para un día específico de la semana."""
        return self.db.query(DailyTip).filter(
            and_(
                DailyTip.day_of_week == day_of_week,
                DailyTip.is_active == is_active,
            )
        ).first()

    def get_all_active(self) -> list[DailyTip]:
        """Obtener todos los consejos activos (lote actual)."""
        return self.db.query(DailyTip).filter(
            DailyTip.is_active == True
        ).order_by(DailyTip.day_of_week).all()

    def get_today_tip(self, today_day_of_week: int) -> DailyTip | None:
        """Obtener el consejo de hoy basado en el día de la semana."""
        return self.get_by_day(today_day_of_week, is_active=True)

    def deactivate_all(self) -> int:
        """Desactivar todos los consejos (usado antes de generar nuevo lote)."""
        result = self.db.query(DailyTip).filter(
            DailyTip.is_active == True
        ).update({DailyTip.is_active: False})
        self.db.flush()
        return result

    def get_latest_generation_date(self) -> datetime | None:
        """Obtener la fecha cuando se generó el lote actual."""
        result = self.db.query(DailyTip.generated_at).filter(
            DailyTip.is_active == True
        ).order_by(DailyTip.generated_at.desc()).first()
        return result[0] if result else None

    def update(self, daily_tip_id: UUID, updates: dict) -> DailyTip | None:
        """Actualizar un consejo diario."""
        tip = self.get_by_id(daily_tip_id)
        if not tip:
            return None

        for key, value in updates.items():
            if value is not None and hasattr(tip, key):
                setattr(tip, key, value)

        self.db.flush()
        return tip

    def delete(self, daily_tip_id: UUID) -> bool:
        """Eliminar un consejo diario."""
        tip = self.get_by_id(daily_tip_id)
        if not tip:
            return False

        self.db.delete(tip)
        self.db.flush()
        return True

    def delete_all_inactive(self) -> int:
        """Eliminar todos los consejos inactivos (limpiar lotes antiguos)."""
        result = self.db.query(DailyTip).filter(
            DailyTip.is_active == False
        ).delete()
        self.db.flush()
        return result
