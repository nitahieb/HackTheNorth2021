from sqlalchemy import Column, Integer, String, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(String, primary_key=True)
    username = Column(String)
    birthdate = Column(String)
    email = Column(String)
    pass_hash = Column(String)
    completed_surveys = Column(JSON)
    tags = Column(JSON)

class Survey(Base):
    __tablename__ = 'surveys'
    id = Column(String, primary_key=True)
    description = Column(String)
    title = Column(String)
    creator = Column(String)
    completed_people= Column(JSON)
    tags = Column(JSON)
    questions = Column(JSON)
    responses = Column(JSON)