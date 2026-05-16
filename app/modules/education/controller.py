"""
Education controller — HTTP endpoint layer.

Endpoints:
    - GET /v1/education/modules
    - GET /v1/education/modules/{slug}
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.modules.education.dto import (
    GenerateModulesRequestDTO,
    GenerateModulesResponseDTO,
    ModuleDetailResponseDTO,
    ModulesListResponseDTO,
)
from app.modules.education.repository import EducationRepository
from app.modules.education.service import EducationService
from app.shared.database import get_db

router = APIRouter(prefix="/v1/education", tags=["Education"])


def _get_education_service(db: Session = Depends(get_db)) -> EducationService:
    repository = EducationRepository(db)
    return EducationService(repository=repository)


@router.get(
    "/modules",
    response_model=ModulesListResponseDTO,
    summary="Listar modulos educativos",
    description="Devuelve el catalogo de modulos educativos disponibles.",
)
def list_modules(
    service: EducationService = Depends(_get_education_service),
) -> ModulesListResponseDTO:
    modules = service.list_modules()
    return {
        "totalCount": len(modules),
        "modules": service.get_module_card_payload(modules),
    }


@router.post(
    "/modules/generate",
    response_model=GenerateModulesResponseDTO,
    summary="Generar modulo educativo con agente",
    description="Genera un modulo usando Tavily + Groq y devuelve el detalle.",
    status_code=status.HTTP_201_CREATED,
)
def generate_module(
    payload: GenerateModulesRequestDTO,
    service: EducationService = Depends(_get_education_service),
) -> GenerateModulesResponseDTO:
    modules = service.generate_modules(
        items=[item.model_dump() for item in payload.items]
    )
    return {
        "items": [
            {
                "module": service.get_module_detail_payload(module),
                "progress": service.get_progress_for_module(
                    module_id=module.id, user_id=None
                ),
            }
            for module in modules
        ]
    }


@router.get(
    "/modules/{slug}",
    response_model=ModuleDetailResponseDTO,
    summary="Obtener detalle de modulo educativo",
    description="Devuelve el contenido completo del modulo y progreso del usuario.",
    responses={
        404: {"description": "Modulo no encontrado"},
    },
)
def get_module_detail(
    slug: str,
    user_id: str | None = Query(default=None, description="ID del usuario"),
    service: EducationService = Depends(_get_education_service),
) -> ModuleDetailResponseDTO:
    module = service.get_module_by_slug(slug)
    if module is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Modulo no encontrado",
        )

    progress = service.get_progress_for_module(module_id=module.id, user_id=user_id)
    return {
        "module": service.get_module_detail_payload(module),
        "progress": progress,
    }
