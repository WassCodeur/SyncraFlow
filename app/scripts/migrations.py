import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.core.config import settings
import uuid
from datetime import datetime, timezone


DATABASE_URL = settings.db_url

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    username = Column(String(120), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    tier = Column(String(50), nullable=False, default="free")
    role = Column(String(50), default="USER", nullable=False)
    name = Column(String(100))
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    workflows = relationship("Workflow", back_populates="user")
    credentials = relationship("Credential", back_populates="user")


class Workflow(Base):
    __tablename__ = 'workflows'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=False)
    trigger_slug = Column(String(50), unique=True)
    user = relationship("User", back_populates="workflows")
    steps = relationship("Step", back_populates="workflow",
                         cascade="all, delete-orphan")
    edges = relationship("Edge", back_populates="workflow",
                         cascade="all, delete-orphan")


class Credential(Base):
    __tablename__ = 'credentials'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    service = Column(String(50))
    data = Column(JSON)
    user = relationship("User", back_populates="credentials")


class Step(Base):
    __tablename__ = 'steps'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    # user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('workflows.id'))
    type = Column(String(50))
    config = Column(JSONB)
    order = Column(Integer)
    workflow = relationship("Workflow", back_populates="steps")
    # user = relationship("User", back_populates="steps")


class Execution(Base):
    __tablename__ = 'executions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('workflows.id'))
    status = Column(String(20))
    payload_received = Column(JSON)
    executed_at = Column(DateTime, default=datetime.now(timezone.utc))


def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("👤 Gestion des utilisateurs ajoutée. SyncraFlow est prêt pour le multi-comptes !")


if __name__ == "__main__":
    init_db()
