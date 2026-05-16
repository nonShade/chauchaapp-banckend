from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.education.entities import EducationalModule


class EducationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_modules(self) -> list[EducationalModule]:
        return self.db.query(EducationalModule).order_by(
            EducationalModule.created_at.desc()
        ).all()

    def get_module_by_id(self, module_id: UUID) -> EducationalModule | None:
        return self.db.query(EducationalModule).filter(
            EducationalModule.educational_module_id == module_id
        ).first()

    def create_module(self, module) -> EducationalModule:
        record = EducationalModule(
            educational_module_id=UUID(module.id),
            title=module.title,
            description=module.description,
            content=module.json(),
            duration=module.estimatedTimeMinutes,
            difficulty=module.level,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
