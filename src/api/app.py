from src.models import SessionLocal, Categories
   
db = SessionLocal()
categories = db.query(Categories).all()
for cat in categories:
   print(f"{cat.category_name}: {cat.points_weight}")
db.close()