"""
Quizzes module entities.

Tables:
    - quiz: Quizzes linked to educational modules.
    - question: Questions within a quiz.
    - answer_option: Possible answers for a question.
    - quiz_result: User attempt results for a quiz.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base_entity import AuditMixin
from app.shared.database import Base


class Quiz(Base, AuditMixin):
    """Quiz associated with an educational module."""

    __tablename__ = "quiz"

    quiz_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    educational_module_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("educational_module.educational_module_id"),
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    educational_module: Mapped["EducationalModule"] = relationship(
        back_populates="quizzes"
    )
    questions: Mapped[list["Question"]] = relationship(back_populates="quiz")
    results: Mapped[list["QuizResult"]] = relationship(back_populates="quiz")


class Question(Base, AuditMixin):
    """Question within a quiz."""

    __tablename__ = "question"

    question_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("quiz.quiz_id"),
        nullable=False,
    )
    question_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    quiz: Mapped["Quiz"] = relationship(back_populates="questions")
    answer_options: Mapped[list["AnswerOption"]] = relationship(
        back_populates="question"
    )


class AnswerOption(Base, AuditMixin):
    """Possible answer for a quiz question."""

    __tablename__ = "answer_option"

    answer_option_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("question.question_id"),
        nullable=False,
    )
    answer_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Relationships
    question: Mapped["Question"] = relationship(back_populates="answer_options")


class QuizResult(Base, AuditMixin):
    """Result of a user's quiz attempt."""

    __tablename__ = "quiz_result"

    quiz_result_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
    )
    quiz_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("quiz.quiz_id"),
        nullable=False,
    )
    attempt_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    correct_answer: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_questions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="quiz_results")
    quiz: Mapped["Quiz"] = relationship(back_populates="results")
