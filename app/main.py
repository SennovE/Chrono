from fastapi import FastAPI
from app.db import DeclarativeBase

app = FastAPI()

DeclarativeBase.metadata.create_all()