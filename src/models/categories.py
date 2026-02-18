from sqlalchemy import Column, Integer, Text, REAL, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


'''
CREATE TABLE CATEGORIES(
    CATEGORY_ID         INTEGER         PRIMARY KEY AUTOINCREMENT,
    CATEGORY_NAME       TEXT            NOT NULL UNIQUE,
    POINTS_WEIGHT       REAL            DEFAULT 1.0,
    IS_SYSTEM           INTEGER         DEFAULT 0 CHECK (IS_SYSTEM IN (0, 1)),
    COLOR               TEXT,
    ICON                TEXT
);
'''
class Categories(Base):
    __tablename__ = "CATEGORIES"

    category_id = Column("CATEGORY_ID", Integer, primary_key=True, autoincrement=True)
    category_name = Column("CATEGORY_NAME", Text, nullable=False, unique=True)
    points_weight = Column("POINTS_WEIGHT", REAL, nullable=False, server_default="1.0")
    is_system = Column("IS_SYSTEM", Integer, nullable=False, server_default="0")
    color = Column("COLOR", Text, nullable=True)
    icon = Column("ICON", Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "IS_SYSTEM IN (0, 1)", name="ck_categories_is_system"),
 
    )

    tasks = relationship("Tasks", back_populates="category")
    streak = relationship("Streaks", back_populates="category", uselist=False)