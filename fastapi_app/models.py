# =================================================================================
# SQLAlchemy Database Models
# =================================================================================
# This file defines the structure of your database tables as Python classes.
# SQLAlchemy's ORM (Object-Relational Mapper) will map these classes to tables
# in the PostgreSQL database.
# =================================================================================

from sqlalchemy import Column, Integer, String
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)