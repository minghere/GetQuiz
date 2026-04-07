from sqlmodel import SQLModel, create_engine, Session
from core.config import settings

#Create engine: display SQL code from database to Terminal display
engine = create_engine(settings.DATABASE_URL, echo=True)

#Provide session for saving data to database request
def get_session():
    with Session(engine) as session:
        yield session