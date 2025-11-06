from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recommendations.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata = MetaData() # We define this here

recommendations = Table(
    "recommendations",
    metadata, # We associate the table with the metadata
    Column("id", Integer, primary_key=True, index=True),
    Column("user_input", Text, nullable=False),
    Column("recommended_movies", Text, nullable=False),
    Column("timestamp", DateTime, server_default=func.now())
)

# This was the problem line. We are moving it to main.py
# metadata.create_all(engine) 

# This line is now guaranteed to be reached
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)