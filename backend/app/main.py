from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .api import auth, wallet, payments, admin
from .models.user import User
from .models.wallet import Wallet
from .models.ledger import LedgerTransaction
from .models.persona import Persona
from .models.conversation import Conversation
from .models.message import Message
from .models.api_key import ApiKey
from .models.auth_session import AuthSession
from .models.password_reset_token import PasswordResetToken
from .models.payment_intent import PaymentIntent

app = FastAPI(
    title="Persian AI Workspace - Wallet & Payments MVP",
    description="Phase 1 Part 3A wallet, ledger, payment intents - sandbox mock provider only, no real payment gateway",
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
    return {"message": "Persian AI Workspace - Wallet & Payments MVP Part 3A", "phase": "Phase 1 Part 3A adds wallet, ledger, payment intents - sandbox mock only, no real gateway"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Include routers
app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(payments.router)
app.include_router(admin.router)
