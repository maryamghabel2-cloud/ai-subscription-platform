"""payment intents - Phase 1 Part 3A wallet, ledger, payment intents

Revision ID: 003_payment_intents
Revises: 002_auth_sessions
Create Date: 2026-07-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003_payment_intents'
down_revision: Union[str, None] = '002_auth_sessions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'payment_intents',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('amount_toman', sa.Integer(), nullable=True),
        sa.Column('amount_usd', sa.Integer(), nullable=True),
        sa.Column('amount_crypto', sa.String(length=50), nullable=True),
        sa.Column('crypto_currency', sa.String(length=20), nullable=True),
        sa.Column('crypto_network', sa.String(length=20), nullable=True),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('provider_reference', sa.String(length=255), nullable=True),
        sa.Column('wallet_address', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('idempotency_key', sa.String(length=255), nullable=False),
        sa.Column('exchange_rate_snapshot', sa.Integer(), nullable=True),
        sa.Column('credits_to_add', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('verification_data', postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), 'sqlite'), nullable=True),
        sa.Column('failure_reason', sa.String(length=500), nullable=True),
        sa.CheckConstraint('expires_at > created_at', name='ck_payment_intents_expires_gt_created'),
        sa.CheckConstraint('credits_to_add > 0', name='ck_payment_intents_credits_positive'),
        sa.CheckConstraint("status IN ('pending', 'processing', 'completed', 'failed', 'expired', 'refunded')", name='ck_payment_intents_status_valid'),
        sa.CheckConstraint("provider IN ('zarinpal', 'crypto_trc20', 'crypto_ton', 'sandbox_mock')", name='ck_payment_intents_provider_valid'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('idempotency_key', name='uq_payment_intents_idempotency_key')
    )
    op.create_index('ix_payment_intents_user_id', 'payment_intents', ['user_id'], unique=False)
    op.create_index('ix_payment_intents_status', 'payment_intents', ['status'], unique=False)
    op.create_index('ix_payment_intents_provider', 'payment_intents', ['provider'], unique=False)
    op.create_index('ix_payment_intents_idempotency_key', 'payment_intents', ['idempotency_key'], unique=True)
    op.create_index('ix_payment_intents_created_at', 'payment_intents', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_payment_intents_created_at', table_name='payment_intents')
    op.drop_index('ix_payment_intents_idempotency_key', table_name='payment_intents')
    op.drop_index('ix_payment_intents_provider', table_name='payment_intents')
    op.drop_index('ix_payment_intents_status', table_name='payment_intents')
    op.drop_index('ix_payment_intents_user_id', table_name='payment_intents')
    op.drop_table('payment_intents')
