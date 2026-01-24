from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from Infrastructure.Db.database import Base
from Domain.Enums.InterviewStatus import InterviewStatus


def generate_uuid():
    return str(uuid.uuid4())


class InterviewModel(Base):
    
    __tablename__ = "interviews"
    
    interview_id = Column(String, primary_key=True, default=generate_uuid)
    topic = Column(String, nullable=False)
    status = Column(String, nullable=False, default=InterviewStatus.NOT_STARTED.value)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    questions = relationship("QuestionModel", back_populates="interview", cascade="all, delete-orphan")
    answers = relationship("AnswerModel", back_populates="interview", cascade="all, delete-orphan")
    summary = relationship("InterviewSummaryModel", back_populates="interview", uselist=False, cascade="all, delete-orphan")


class QuestionModel(Base):
    
    __tablename__ = "questions"
    
    question_id = Column(String, primary_key=True, default=generate_uuid)
    text = Column(Text, nullable=False)
    interview_id = Column(String, ForeignKey("interviews.interview_id"), nullable=False)
    question_order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    interview = relationship("InterviewModel", back_populates="questions")
    answers = relationship("AnswerModel", back_populates="question", cascade="all, delete-orphan")


class AnswerModel(Base):
    
    __tablename__ = "answers"
    
    answer_id = Column(String, primary_key=True, default=generate_uuid)
    text = Column(Text, nullable=False)
    question_id = Column(String, ForeignKey("questions.question_id"), nullable=False)
    interview_id = Column(String, ForeignKey("interviews.interview_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    question = relationship("QuestionModel", back_populates="answers")
    interview = relationship("InterviewModel", back_populates="answers")


class InterviewSummaryModel(Base):
    
    __tablename__ = "interview_summaries"
    
    summary_id = Column(String, primary_key=True, default=generate_uuid)
    interview_id = Column(String, ForeignKey("interviews.interview_id"), nullable=False, unique=True)
    themes = Column(JSON, nullable=False)
    key_points = Column(JSON, nullable=False)
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)
    full_summary_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    interview = relationship("InterviewModel", back_populates="summary")
