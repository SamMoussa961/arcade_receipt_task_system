from sqlalchemy import Column, Integer, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base


class GameRuns(Base):
    __tablename__ = "GAME_RUNS"

    game_run_id = Column("GAME_RUN_ID", Integer, primary_key=True, autoincrement=True)
    run_date = Column("RUN_DATE", Text, nullable=False, server_default="(datetime('now', 'localtime'))")
    started_at = Column("STARTED_AT", Text, nullable=False, server_default="(datetime('now', 'localtime'))")
    ended_at = Column("ENDED_AT", Text, nullable=True)
    total_score = Column("TOTAL_SCORE", Integer, server_default="0")
    status = Column("STATUS", Text, nullable=False, server_default="active")

    __table_args__ = (
        CheckConstraint("STATUS IN ('active', 'completed', 'abandoned')", name="ck_game_runs_status"),
    )

    tasks = relationship("Tasks", back_populates="game_run", cascade="all, delete-orphan")
    scoring_records = relationship("Scoring", foreign_keys="Scoring.game_run_id", back_populates="game_run")
    completed_scorings = relationship("Scoring", foreign_keys="Scoring.completed_in_run_id", back_populates="completed_in_run")