from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Streaks(Base):
    __tablename__ = "STREAKS"

    streak_id = Column("STREAK_ID", Integer, primary_key=True, autoincrement=True)
    category_id = Column("CATEGORY_ID", Integer, ForeignKey("CATEGORIES.CATEGORY_ID", ondelete="CASCADE"), nullable=False)
    current_streak = Column("CURRENT_STREAK", Integer, server_default="0")
    longest_streak = Column("LONGEST_STREAK", Integer, server_default="0")
    last_completed_date = Column("LAST_COMPLETED_DATE", Text, nullable=True)
    total_completions = Column("TOTAL_COMPLETIONS", Integer, server_default="0")
    updated_at = Column("UPDATED_AT", Text, server_default="(datetime('now', 'localtime'))")

    __table_args__ = (
        UniqueConstraint("CATEGORY_ID", name="uq_streak_category_id"),
    )

    # Relationships
    category = relationship("Categories", back_populates="streak")