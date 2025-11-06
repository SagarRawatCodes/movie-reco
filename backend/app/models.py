# This is the database code you provided originally.
# It saves the recommendations to a SQLite database.
from .database import recommendations, SessionLocal
from sqlalchemy import insert, select
import json

def save_recommendation(user_input: str, movies: list):
    session = SessionLocal()
    try:
        stmt = insert(recommendations).values(
            user_input=user_input,
            recommended_movies=json.dumps(movies)
        )
        session.execute(stmt)
        session.commit()
    finally:
        session.close()

def get_all_recommendations():
    session = SessionLocal()
    try:
        stmt = select(recommendations)
        rows = session.execute(stmt).fetchall()
        result = []
        for row in rows:
            rec = dict(row._mapping)
            rec["recommended_movies"] = json.loads(rec["recommended_movies"])
            result.append(rec)
        return result
    finally:
        session.close()
