"""auth sessions and password reset tokens

Revision ID: 002_auth_sessions
Revises: 001_core_schema
Create Date: 2026-07-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002_auth_sessions'
down_revision: Union[str, None] = '001_core_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use String(36) for UUID to be compatible with both PostgreSQL and SQLite tests
    # In production PostgreSQL, UUID can be stored as String or UUID type; String(36) works universally
    op.create_table(
        'auth_sessions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_token_hash', sa.String(length=255), nullable=False),
        sa.Column('refresh_token_hash', sa.String(length=255), nullable=False),
        sa.Column('csrf_token_hash', sa.String(length=255), nullable=False),
        sa.Column('user_agent_hash', sa.String(length=255), nullable=True),
        sa.Column('ip_hash', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('refresh_expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('expires_at > created_at', name='ck_auth_sessions_expires_gt_created'),
        sa.CheckConstraint('refresh_expires_at > created_at', name='ck_auth_sessions_refresh_expires_gt_created'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('refresh_token_hash', name='uq_auth_sessions_refresh_token_hash'),
        sa.UniqueConstraint('session_token_hash', name='uq_auth_sessions_session_token_hash')
    )
    op.create_index(op.f('ix_auth_sessions_refresh_token_hash'), 'auth_sessions', ['refresh_token_hash'], unique=True)
    op.create_index(op.f('ix_auth_sessions_session_token_hash'), 'auth_sessions', ['session_token_hash'], unique=True)
    op.create_index(op.f('ix_auth_sessions_user_id'), 'auth_sessions', ['user_id'], unique=False)

    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('expires_at > created_at', name='ck_password_reset_expires_gt_created'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash', name='uq_password_reset_token_hash')
    )
    op.create_index(op.f('ix_password_reset_tokens_token_hash'), 'password_reset_tokens', ['token_hash'], unique=True)
    op.create_index(op.f('ix_password_reset_tokens_user_id'), 'password_reset_tokens', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_password_reset_tokens_user_id'), table_name='password_reset_tokens')
    op.drop_index(op.f('ix_password_reset_tokens_token_hash'), table_name='password_reset_tokens')
    op.drop_table('password_reset_tokens')
    op.drop_index(op.f('ix_auth_sessions_user_id'), table_name='auth_sessions')
    op.drop_index(op.f('ix_auth_sessions_session_token_hash'), table_name='auth_sessions')
    op.drop_index(op.f('ix_auth_sessions_refresh_token_hash'), table_name='auth_sessions')
    op.drop_table('auth_sessions')
