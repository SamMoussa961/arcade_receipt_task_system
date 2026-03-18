from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db_tools.db import initialize_db
from src.models import SessionLocal, Categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield

app = FastAPI(lifespan=lifespan)
   

@app.get("/health")
async def root():
   return {"message": "I'm Okay!!"}

@app.get("/categories")
async def get_data():
   db = SessionLocal()
   categories = db.query(Categories).all()
   result = [
      {
         "category_id": cat.category_id,
         "category_name": cat.category_name,
         "points_weight": cat.points_weight,
         "is_system": cat.is_system,
         "color": cat.color,
         "icon": cat.icon,
      }
      for cat in categories
   ]
   db.close()
   return result