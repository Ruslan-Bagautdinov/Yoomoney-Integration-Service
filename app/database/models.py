from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    access_token = Column(String, unique=True, index=True, nullable=True)
    client_id = Column(String, unique=True, index=True, nullable=True)
    user_redirect_uri = Column(String, nullable=True)

