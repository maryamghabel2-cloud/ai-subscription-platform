"""core schema - Phase 1 Part 1 - append-only signed credit ledger

Revision ID: 001_core_schema
Revises: 
Create Date: 2026-07-19

Decision notes:
- Persona.version kept as semantic-version String (v1.0.0) explicit decision, not integer, for flexibility (draft versions like v0.1.0-draft)
- ApiKey.scopes uses PostgreSQL JSONB for MVP, acceptable per spec
- ApiKey renamed rate_limit -> rate_limit_per_minute + added key_prefix non-secret for lookup
- User.email case-insensitive unique via normalized_email field (lowercased) unique, plus email unique - registration logic will normalize to lower in Part 2
- Ledger is append-only signed credit ledger, not double-entry - balance_credits is cached/materialized, Part 3 must update wallet balance and ledger insert atomically, reconciliation SUM(ledger.amount) vs wallet balance
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_core_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users - with normalized_email and role check
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('normalized_email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("role IN ('user', 'admin')", name='ck_users_role_valid'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email', name='uq_users_email'),
        sa.UniqueConstraint('normalized_email', name='uq_users_normalized_email')
    )

    # personas - semantic-version String decision documented
    op.create_table(
        'personas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('name_fa', sa.String(length=255), nullable=False),
        sa.Column('role_definition', sa.Text(), nullable=False),
        sa.Column('tone', sa.String(length=100), nullable=True),
        sa.Column('risk_level', sa.String(length=20), nullable=False, server_default='low'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='draft'),
        sa.Column('version', sa.String(length=20), nullable=False, server_default='v1.0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("risk_level IN ('low', 'medium', 'high')", name='ck_personas_risk_level_valid'),
        sa.CheckConstraint("status IN ('draft', 'active', 'deprecated')", name='ck_personas_status_valid'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug', name='uq_personas_slug')
    )

    # wallets - exactly one named UNIQUE constraint for user_id, no redundant unique index
    op.create_table(
        'wallets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('balance_credits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('balance_credits >= 0', name='ck_wallets_balance_non_negative'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_wallets_user_id')
    )

    # conversations - explicit deletion may delete messages policy
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('persona_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['persona_id'], ['personas.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )

    # ledger_transactions - append-only signed credit ledger (not double-entry), exactly one uniqueness mechanism for idempotency_key
    op.create_table(
        'ledger_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wallet_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('reference_id', sa.String(length=255), nullable=True),
        sa.Column('idempotency_key', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('amount <> 0', name='ck_ledger_amount_nonzero'),
        sa.ForeignKeyConstraint(['wallet_id'], ['wallets.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('idempotency_key', name='uq_ledger_idempotency_key')
    )
    op.create_index('ix_ledger_wallet_id', 'ledger_transactions', ['wallet_id'], unique=False)
    op.create_index('ix_ledger_type', 'ledger_transactions', ['type'], unique=False)
    op.create_index('ix_ledger_created_at', 'ledger_transactions', ['created_at'], unique=False)

    # messages - role check, FK CASCADE for explicit conversation deletion may delete messages
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('enhanced_prompt', sa.Text(), nullable=True),
        sa.Column('provider_used', sa.String(length=100), nullable=True),
        sa.Column('cost_credits', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("role IN ('user', 'assistant', 'system')", name='ck_messages_role_valid'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # api_keys - JSONB scopes, key_prefix non-secret, rate_limit_per_minute check
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('key_prefix', sa.String(length=20), nullable=False),
        sa.Column('key_hash', sa.String(length=255), nullable=False),
        sa.Column('scopes', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('rate_limit_per_minute', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('rate_limit_per_minute > 0', name='ck_api_keys_rate_limit_positive'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key_hash', name='uq_api_keys_key_hash')
    )


def downgrade() -> None:
    op.drop_table('api_keys')
    op.drop_table('messages')
    op.drop_table('ledger_transactions')
    op.drop_table('conversations')
    op.drop_table('wallets')
    op.drop_table('personas')
    op.drop_table('users')
