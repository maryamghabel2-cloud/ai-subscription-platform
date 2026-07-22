from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .api import auth
from .models.user import User
from .models.wallet import Wallet
from .models.ledger import LedgerTransaction
from .models.persona import Persona
from .models.conversation import Conversation
from .models.message import Message
from .models.api_key import ApiKey
from .models.auth_session import AuthSession
from .models.password_reset_token import PasswordResetToken

# Create tables if not exist via create_all for dev, but production uses alembic
# For safety, we create all in this minimal app for local dev, but migration is preferred
# Comment out in production and use alembic upgrade head
# Base.metadata.create_all(bind=engine) - removed per seed fix, assume migrations run

app = FastAPI(
    title="Persian AI Workspace - Auth MVP",
    description="Phase 1 Part 2 secure cookie-based authentication - no AI providers yet",
    version="1.0.0",
)

# CORS - allow frontend localhost:3000 with credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Persian AI Workspace - Auth MVP Part 2", "phase": "Phase 1 Part 2 adds backend authentication; no AI providers yet."}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Include auth router
app.include_router(auth.router)
