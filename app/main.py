from fastapi import FastAPI
from app.db import DeclarativeBase
from app.db.connection import *


app = FastAPI()

DeclarativeBase.metadata.create_all(bind=get_session())

session = SessionManager()


def get_db():
    db = session.get_session_maker()
    yield db

