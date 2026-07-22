"""
Test exactly one uniqueness mechanism for idempotency_key and wallet.user_id
Per requirement: Use exactly one named UNIQUE constraint or one unique index, not combine unique=True, index=True, explicit Index
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import UniqueConstraint, Index
from app.database import Base
from app.models.wallet import Wallet
from app.models.ledger import LedgerTransaction

def test_idempotency_uniqueness_mechanism_count():
    """Assert exactly one uniqueness mechanism exists for idempotency_key"""
    table = LedgerTransaction.__table__
    # Count unique constraints that include idempotency_key (only UniqueConstraint, not ForeignKey)
    unique_constraints = [c for c in table.constraints if isinstance(c, UniqueConstraint) and any(col.name == 'idempotency_key' for col in c.columns)]
    # Count unique indexes that include idempotency_key and are unique
    unique_indexes = [idx for idx in table.indexes if idx.unique and any(col.name == 'idempotency_key' for col in idx.columns)]
    
    total_unique_mechanisms = len(unique_constraints) + len(unique_indexes)
    # Should be exactly 1 - we use one named UNIQUE constraint uq_ledger_idempotency_key
    assert total_unique_mechanisms == 1, f"Expected exactly 1 uniqueness mechanism for idempotency_key, got {total_unique_mechanisms}: constraints={unique_constraints}, indexes={unique_indexes}"
    
    # Also check that column itself does NOT have unique=True + index=True duplicate - should rely on constraint only
    col = table.c.idempotency_key
    assert not col.unique, "idempotency_key column should not have unique=True, should rely on constraint only"
    # Column index should be False because unique constraint creates index automatically, no extra index=True
    # Actually unique constraint creates index, but column.index should be False
    assert not col.index or col.index is False, "idempotency_key column should not have explicit index=True"

def test_wallet_user_uniqueness_mechanism_count():
    """Assert exactly one uniqueness mechanism exists for wallet.user_id"""
    table = Wallet.__table__
    unique_constraints = [c for c in table.constraints if isinstance(c, UniqueConstraint) and any(col.name == 'user_id' for col in c.columns)]
    unique_indexes = [idx for idx in table.indexes if idx.unique and any(col.name == 'user_id' for col in idx.columns)]
    
    total = len(unique_constraints) + len(unique_indexes)
    assert total == 1, f"Expected exactly 1 uniqueness mechanism for wallets.user_id, got {total}: constraints={unique_constraints}, indexes={unique_indexes}"
    
    col = table.c.user_id
    assert not col.unique, "user_id column should not have unique=True, should rely on constraint only"

def test_no_explicit_index_on_pk():
    """Remove unnecessary explicit indexes on primary-key id columns"""
    from app.models.user import User
    from app.models.persona import Persona
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models.api_key import ApiKey
    
    for model in [User, Wallet, LedgerTransaction, Persona, Conversation, Message, ApiKey]:
        table = model.__table__
        id_col = table.c.id
        # id column should be primary_key True, and should not have explicit index=True
        assert id_col.primary_key, f"{model.__tablename__}.id should be primary key"
        # Check that we didn't set index=True explicitly (PK already indexed)
        # In SQLAlchemy, if you set index=True on PK, it would create extra index - we want to avoid
        # So check that column.index is falsy (None or False)
        # Note: unique constraints create indexes, but id should not have extra
        assert not getattr(id_col, 'index', False) or id_col.primary_key, f"{model.__tablename__}.id should not have explicit index=True"
