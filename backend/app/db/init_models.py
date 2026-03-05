# Import all models here so Alembic can discover them
from app.models.user import User  # noqa: F401
from app.models.agent_profile import AgentProfile  # noqa: F401
from app.models.verification_request import VerificationRequest  # noqa: F401
from app.models.broadcast import Broadcast  # noqa: F401
from app.models.broadcast_response import BroadcastResponse  # noqa: F401
from app.models.notification import Notification  # noqa: F401
