"""
Education service — educational modules and quizzes content.
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable
from uuid import UUID, uuid4

from app.agent.quizzes.quizz_agent import LevelType, Module, QuizzAgent
from app.modules.education.repository import EducationRepository


class EducationService:
    def __init__(self, repository: EducationRepository, agent: QuizzAgent | None = None):
        self._agent = agent or QuizzAgent()
        self._repository = repository

    def list_modules(self) -> list[Module]:
        records = self._repository.list_modules()
        return [self._deserialize_module(record) for record in records]

    def get_module_by_slug(self, slug: str) -> Module | None:
        modules = self.list_modules()
        return next((module for module in modules if module.slug == slug), None)

    def get_module_by_id(self, module_id: str) -> Module | None:
        record = self._repository.get_module_by_id(UUID(module_id))
        if record is None:
            return None
        return self._deserialize_module(record)

    def get_progress_for_module(self, module_id: str, user_id: str | None) -> dict:
        progress = self._agent.get_default_progress(module_id=module_id, user_id=user_id)
        return self._agent.serialize_progress(progress)

    def generate_module(self, topic: str, level: str) -> Module:
        if level not in {"Principiante", "Intermedio", "Avanzado"}:
            raise ValueError("Invalid level")

        module = self._agent.generate_module_from_topic(
            topic=topic, level=level
        )
        module.id = str(uuid4())
        module.createdAt = datetime.utcnow()
        module.slug = module.slug or self._slugify(module.title)

        self._repository.create_module(module)
        return module

    def generate_modules(self, items: list[dict]) -> list[Module]:
        modules: list[Module] = []
        for item in items:
            topic = item.get("topic")
            level = item.get("level")
            if not topic or level not in {"Principiante", "Intermedio", "Avanzado"}:
                raise ValueError("Invalid topic or level")

            module = self._agent.generate_module_from_topic(topic=topic, level=level)
            module.id = str(uuid4())
            module.createdAt = datetime.utcnow()
            module.slug = module.slug or self._slugify(module.title)
            self._repository.create_module(module)
            modules.append(module)

        return modules

    def _deserialize_module(self, record) -> Module:
        if not record.content:
            raise ValueError("Educational module content is empty")
        return Module.parse_raw(record.content)

    def _slugify(self, value: str) -> str:
        import re

        slug = value.strip().lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"\s+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug

    def get_module_card_payload(self, modules: Iterable[Module]) -> list[dict]:
        return [
            {
                "id": module.id,
                "slug": module.slug,
                "title": module.title,
                "description": module.description,
                "level": module.level,
                "estimatedTimeMinutes": module.estimatedTimeMinutes,
                "topicsCount": module.topicsCount,
                "questionsCount": module.quiz.questionsCount,
                "category": module.category,
                "tags": module.tags,
            }
            for module in modules
        ]

    def get_module_detail_payload(self, module: Module) -> dict:
        return {
            "id": module.id,
            "slug": module.slug,
            "title": module.title,
            "description": module.description,
            "level": module.level,
            "estimatedTimeMinutes": module.estimatedTimeMinutes,
            "topicsCount": module.topicsCount,
            "category": module.category,
            "tags": module.tags,
            "createdAt": module.createdAt,
            "learningObjectives": module.learningObjectives,
            "content": module.content,
            "topics": module.topics,
            "quiz": {
                "id": module.quiz.id,
                "title": module.quiz.title,
                "questionsCount": module.quiz.questionsCount,
                "passingScore": module.quiz.passingScore,
                "questions": [
                    {
                        "id": question.id,
                        "type": question.type,
                        "question": question.question,
                        "options": question.options,
                        "explanation": question.explanation,
                    }
                    for question in module.quiz.questions
                ],
            },
        }
