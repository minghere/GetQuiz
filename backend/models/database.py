from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
import uuid
import enum
import sqlalchemy
from sqlalchemy import Enum as SAEnum

#CREATE TABLE USERS QUOTAS
class UserQuotas(SQLModel, table=True):
    __tablename__ = "user_quotas"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key="users.id")
    quota_remaining: int = Field(default=50)
    reset_time: Optional[datetime] = Field(default=None)

    user: Optional["Users"] = Relationship(back_populates="user_quota")
    
#CREATETABLE USERS
class Users(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[str] = Field(default=None, primary_key=True)
    email: Optional[str] = Field(max_length=225, default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    user_quota: Optional["UserQuotas"] = Relationship(back_populates="user")
    attempt: List["Attempts"] = Relationship(back_populates="user")
    quiz: List["Quizzes"] = Relationship(back_populates="user")

#CREATE TABLE QUIZZES
class QuizDifficulties(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    SUPERHARD = "superhard"

class Quizzes(SQLModel, table=True):
    __tablename__ = "quizzes"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key="users.id")
    title: str = Field(max_length=255)
    difficulty: QuizDifficulties = Field(
        default = QuizDifficulties.EASY,
        sa_column=sqlalchemy.Column(SAEnum(QuizDifficulties))
    )
    created_time: datetime = Field(default_factory=datetime.now)
    user: Optional["Users"] = Relationship(back_populates="quiz")
    question: List["Questions"] = Relationship(
        back_populates="quiz",
        sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    attempt: List["Attempts"] = Relationship(back_populates="quiz")

#CREATE TABLE QUESTIONS
class Questions(SQLModel, table=True):
    __tablename__ = "questions"
    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_id: uuid.UUID = Field(foreign_key="quizzes.id")
    content: str 
    explanation: str 

    quiz: Optional["Quizzes"] = Relationship(back_populates="question")
    option: List["Options"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade":"all, delete-orphan"})
    user_answer_history: List["UserAnswerHistory"] = Relationship(back_populates="question")

#CREATE TABLE OPTIONS
class Options(SQLModel, table=True):
    __tablename__ = "options"
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: Optional[int] = Field(default=None, foreign_key="questions.id")
    content: str
    is_correct: bool = Field(default=False)
    
    question: Optional["Questions"] = Relationship(back_populates="option")
    user_answer_history: List["UserAnswerHistory"] = Relationship(back_populates="option")

#CREATE TABLE ATTEMPTS
class AttemptStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class Attempts(SQLModel, table=True):
    __tablename__ = "attempts"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key="users.id")
    quiz_id: uuid.UUID = Field(foreign_key="quizzes.id")
    score: Optional[int] = Field(default=None)
    starting_time: datetime = Field(default_factory=datetime.now)
    ending_time: Optional[datetime] = Field(default=None)
    status: AttemptStatus = Field(
        default=AttemptStatus.IN_PROGRESS,
        sa_column=sqlalchemy.Column(SAEnum(AttemptStatus))
    )

    user: Optional["Users"] = Relationship(back_populates="attempt")
    quiz: Optional["Quizzes"] = Relationship(back_populates="attempt")
    user_answer_history: List["UserAnswerHistory"] = Relationship(back_populates="attempt")

#CREATE TABLE USER_ANSWER_HISTORY
class UserAnswerHistory(SQLModel, table=True):
    __tablename__ = "user_answer_history"
    id: Optional[int] = Field(default=None, primary_key=True)
    attempt_id: uuid.UUID = Field(foreign_key="attempts.id")
    question_id: Optional[int] = Field(default=None, foreign_key="questions.id")
    option_id: Optional[int] = Field(default=None, foreign_key="options.id")

    attempt: Optional[Attempts] = Relationship(back_populates="user_answer_history")
    question: Optional[Questions] = Relationship(back_populates="user_answer_history")
    option: Optional[Options] = Relationship(back_populates="user_answer_history")


