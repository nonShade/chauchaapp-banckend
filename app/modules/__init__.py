"""
Central entity registry — imports all ORM entities to ensure
SQLAlchemy registers them with the Base metadata.

Import this module before calling Base.metadata.create_all()
or running Alembic migrations.
"""

# Users module
from app.modules.users.entities import IncomeType, User  # noqa: F401

# Groups module
from app.modules.groups.entities import (  # noqa: F401
    FamilyGroup,
    GroupJoinRequest,
    GroupMember,
)

# Financial data module
from app.modules.financial_data.entities import Bank, CreditProduct  # noqa: F401

# Transactions module
from app.modules.transactions.entities import (  # noqa: F401
    Transaction,
    TransactionCategory,
    TransactionFrequency,
    TransactionType,
)

# News module
from app.modules.news.entities import (  # noqa: F401
    News,
    NewsTag,
    NewsTagMap,
    PersonalizedAnalysisNews,
    UserInterest,
)

# Education module
from app.modules.education.entities import (  # noqa: F401
    EducationalModule,
    EducationalModuleTopic,
    EducationalTopic,
    UserProgress,
)

# Quizzes module
from app.modules.quizzes.entities import (  # noqa: F401
    AnswerOption,
    Question,
    Quiz,
    QuizResult,
)

# Notifications module
from app.modules.notifications.entities import (  # noqa: F401
    Notification,
    NotificationStatus,
    NotificationType,
)
