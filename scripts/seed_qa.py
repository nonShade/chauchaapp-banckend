"""
ChauchaApp QA Seed Script (Python).

Generates test data for the QA environment using SQLAlchemy ORM.
Focuses on user data needed for authentication testing.

Usage:
    python -m scripts.seed_qa

Default test password: TestPass123!
"""

import os
import sys
import uuid
from datetime import date
from decimal import Decimal

import bcrypt
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import all entities to register them with SQLAlchemy
import app.modules  # noqa: F401
from app.shared.database import Base
from app.modules.users.entities import IncomeType, User
from app.modules.transactions.entities import (
    TransactionType,
    TransactionFrequency,
    TransactionCategory,
)
from app.modules.notifications.entities import NotificationType, NotificationStatus
from app.modules.education.entities import EducationalTopic


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/chauchaapp_db_qa",
)
TEST_PASSWORD = "TestPass123!"


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_lookup_tables(session):
    """Seed all lookup tables with initial values."""

    # Income Types
    income_types = [
        IncomeType(name="salaried", description="Trabajador dependiente con sueldo fijo"),
        IncomeType(name="independent", description="Trabajador independiente o freelance"),
        IncomeType(name="mixed", description="Combinación de ingresos dependientes e independientes"),
        IncomeType(name="other", description="Otro tipo de ingreso"),
    ]
    for it in income_types:
        existing = session.query(IncomeType).filter_by(name=it.name).first()
        if not existing:
            session.add(it)

    # Transaction Types
    transaction_types_data = [
        ("income", "Ingreso de dinero"),
        ("expense", "Gasto de dinero"),
    ]
    for name, desc in transaction_types_data:
        if not session.query(TransactionType).filter_by(name=name).first():
            session.add(TransactionType(name=name, description=desc))

    session.flush()  # Flush to get IDs for FK references

    # Transaction Frequencies
    frequencies_data = [
        ("one_time", "Transacción única, no recurrente"),
        ("monthly", "Se repite mensualmente"),
        ("weekly", "Se repite semanalmente"),
    ]
    for name, desc in frequencies_data:
        if not session.query(TransactionFrequency).filter_by(name=name).first():
            session.add(TransactionFrequency(name=name, description=desc))

    # Transaction Categories
    expense_type = session.query(TransactionType).filter_by(name="expense").first()
    income_type = session.query(TransactionType).filter_by(name="income").first()

    expense_categories = [
        ("alimentacion", "Gastos en comida y supermercado"),
        ("transporte", "Gastos en transporte público, combustible, etc."),
        ("salud", "Gastos médicos, farmacia, seguros de salud"),
        ("educacion", "Gastos en educación, cursos, materiales"),
        ("entretenimiento", "Gastos en ocio, entretenimiento, suscripciones"),
        ("vivienda", "Arriendo, dividendo, mantención del hogar"),
        ("servicios_basicos", "Agua, luz, gas, internet, teléfono"),
        ("otros_gastos", "Otros gastos no categorizados"),
    ]
    for name, desc in expense_categories:
        if not session.query(TransactionCategory).filter_by(name=name).first():
            session.add(TransactionCategory(
                name=name, description=desc,
                transaction_type_id=expense_type.transaction_type_id if expense_type else None,
            ))

    income_categories = [
        ("sueldo", "Sueldo mensual de trabajo dependiente"),
        ("freelance", "Ingresos por trabajos independientes"),
        ("inversiones", "Retornos de inversiones"),
        ("otros_ingresos", "Otros ingresos no categorizados"),
    ]
    for name, desc in income_categories:
        if not session.query(TransactionCategory).filter_by(name=name).first():
            session.add(TransactionCategory(
                name=name, description=desc,
                transaction_type_id=income_type.transaction_type_id if income_type else None,
            ))

    # Notification Types
    notification_types = [
        ("group_join_request", "Solicitud de un usuario para unirse a tu grupo familiar"),
        ("group_join_accepted", "Tu solicitud para unirse a un grupo fue aceptada"),
        ("group_join_rejected", "Tu solicitud para unirse a un grupo fue rechazada"),
        ("transaction_reminder", "Recordatorio de una transacción programada"),
        ("system_info", "Notificación informativa del sistema"),
        ("educational_reminder", "Recordatorio de progreso en módulo educativo"),
    ]
    for name, desc in notification_types:
        if not session.query(NotificationType).filter_by(name=name).first():
            session.add(NotificationType(name=name, description=desc))

    # Notification Statuses
    notification_statuses = [
        ("pending", "Notificación pendiente de envío"),
        ("sent", "Notificación enviada al usuario"),
        ("read", "Notificación leída por el usuario"),
        ("dismissed", "Notificación descartada por el usuario"),
    ]
    for name, desc in notification_statuses:
        if not session.query(NotificationStatus).filter_by(name=name).first():
            session.add(NotificationStatus(name=name, description=desc))

    # Educational Topics
    topics = [
        ("ahorro", "Estrategias y técnicas de ahorro personal"),
        ("inversion", "Conceptos de inversión y mercados financieros"),
        ("presupuesto", "Planificación y gestión de presupuesto personal"),
        ("deudas", "Manejo y estrategias para salir de deudas"),
        ("impuestos", "Educación tributaria y declaración de impuestos"),
        ("seguros", "Tipos de seguros y protección financiera"),
        ("jubilacion", "Planificación para la jubilación y AFP"),
        ("emprendimiento", "Finanzas para emprendedores"),
    ]
    for name, desc in topics:
        if not session.query(EducationalTopic).filter_by(name=name).first():
            session.add(EducationalTopic(name=name, description=desc))

    session.flush()
    print("  ✓ Lookup tables seeded")


def seed_users(session):
    """Seed test users for authentication testing."""

    hashed_pw = hash_password(TEST_PASSWORD)

    # Get income type references
    salaried = session.query(IncomeType).filter_by(name="salaried").first()
    independent = session.query(IncomeType).filter_by(name="independent").first()
    mixed = session.query(IncomeType).filter_by(name="mixed").first()
    other = session.query(IncomeType).filter_by(name="other").first()

    test_users = [
        # Auth test users
        User(
            first_name="Test", last_name="Login",
            email="test_login@chauchaapp.cl", password=hashed_pw,
            birth_date=date(1990, 5, 15),
            income_type_id=salaried.income_type_id if salaried else None,
            monthly_income=Decimal("850000.00"), monthly_expenses=Decimal("620000.00"),
        ),
        User(
            first_name="Test", last_name="Register",
            email="test_register@chauchaapp.cl", password=hashed_pw,
            birth_date=date(1995, 8, 22),
            income_type_id=independent.income_type_id if independent else None,
            monthly_income=Decimal("1200000.00"), monthly_expenses=Decimal("780000.00"),
        ),
        # Diverse users
        User(
            first_name="María", last_name="González",
            email="maria.gonzalez@test.cl", password=hashed_pw,
            birth_date=date(1988, 3, 10),
            income_type_id=salaried.income_type_id if salaried else None,
            monthly_income=Decimal("1500000.00"), monthly_expenses=Decimal("980000.00"),
        ),
        User(
            first_name="Carlos", last_name="Muñoz",
            email="carlos.munoz@test.cl", password=hashed_pw,
            birth_date=date(1992, 11, 28),
            income_type_id=independent.income_type_id if independent else None,
            monthly_income=Decimal("2000000.00"), monthly_expenses=Decimal("1350000.00"),
        ),
        User(
            first_name="Valentina", last_name="Rojas",
            email="valentina.rojas@test.cl", password=hashed_pw,
            birth_date=date(1985, 7, 3),
            income_type_id=mixed.income_type_id if mixed else None,
            monthly_income=Decimal("1800000.00"), monthly_expenses=Decimal("1100000.00"),
        ),
        User(
            first_name="Andrés", last_name="Silva",
            email="andres.silva@test.cl", password=hashed_pw,
            birth_date=date(1998, 1, 20),
            income_type_id=salaried.income_type_id if salaried else None,
            monthly_income=Decimal("650000.00"), monthly_expenses=Decimal("520000.00"),
        ),
        User(
            first_name="Camila", last_name="Torres",
            email="camila.torres@test.cl", password=hashed_pw,
            birth_date=date(1993, 9, 14),
            income_type_id=other.income_type_id if other else None,
            monthly_income=Decimal("900000.00"), monthly_expenses=Decimal("670000.00"),
        ),
        User(
            first_name="Diego", last_name="Fernández",
            email="diego.fernandez@test.cl", password=hashed_pw,
            birth_date=date(1987, 12, 5),
            income_type_id=salaried.income_type_id if salaried else None,
            monthly_income=Decimal("2500000.00"), monthly_expenses=Decimal("1800000.00"),
        ),
        User(
            first_name="Javiera", last_name="López",
            email="javiera.lopez@test.cl", password=hashed_pw,
            birth_date=date(1996, 4, 18),
            income_type_id=independent.income_type_id if independent else None,
            monthly_income=Decimal("1100000.00"), monthly_expenses=Decimal("850000.00"),
        ),
        User(
            first_name="Felipe", last_name="Martínez",
            email="felipe.martinez@test.cl", password=hashed_pw,
            birth_date=date(1991, 6, 30),
            income_type_id=mixed.income_type_id if mixed else None,
            monthly_income=Decimal("3000000.00"), monthly_expenses=Decimal("2100000.00"),
        ),
    ]

    for user in test_users:
        existing = session.query(User).filter_by(email=user.email).first()
        if not existing:
            session.add(user)

    session.flush()
    print("  ✓ Test users seeded (10 users)")


def main():
    """Run the QA seed process."""
    print(f"\n{'='*60}")
    print("ChauchaApp QA Seed Script")
    print(f"{'='*60}")
    print(f"Database: {DATABASE_URL}")
    print(f"Test password: {TEST_PASSWORD}")
    print(f"{'='*60}\n")

    engine = create_engine(DATABASE_URL, echo=False)

    # Create tables if they don't exist (for local development)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        print("Seeding lookup tables...")
        seed_lookup_tables(session)

        print("Seeding test users...")
        seed_users(session)

        session.commit()
        print(f"\n{'='*60}")
        print("✅ QA seed completed successfully!")
        print(f"{'='*60}")
        print("\nTest credentials:")
        print(f"  Email: test_login@chauchaapp.cl")
        print(f"  Password: {TEST_PASSWORD}")
        print(f"{'='*60}\n")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Seed failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
