from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


'''
CREATE TABLE SCORING(
    SCORE_ID            INTEGER         PRIMARY KEY AUTOINCREMENT,
    GAME_RUN_ID         INTEGER         NOT NULL,
    COMPLETED_IN_RUN_ID INTEGER         NOT NULL,
    TASK_LINE_ID        INTEGER         NOT NULL,
    BONUS_POINTS        INTEGER         DEFAULT 0,
    CREATED_AT          TEXT            NOT NULL DEFAULT (datetime('now', 'localtime')),
    CONSTRAINT SCORING_GAME_RUNS_FK FOREIGN KEY (GAME_RUN_ID) REFERENCES GAME_RUNS(GAME_RUN_ID) ON DELETE CASCADE,
    CONSTRAINT SCORING_TASK_LINES_FK FOREIGN KEY (TASK_LINE_ID) REFERENCES TASK_LINES(TASK_LINE_ID) ON DELETE CASCADE,
    CONSTRAINT SCORING_COMPLETED_RUN_FK FOREIGN KEY (COMPLETED_IN_RUN_ID) REFERENCES GAME_RUNS(GAME_RUN_ID) ON DELETE CASCADE,
    UNIQUE (TASK_LINE_ID)
);
'''
class Scoring(Base):
    __tablename__ = "SCORING"

    score_id = Column("SCORE_ID", Integer, primary_key=True, autoincrement=True)
    game_run_id = Column("GAME_RUN_ID", Integer, ForeignKey("GAME_RUNS.GAME_RUN_ID", ondelete="CASCADE"), nullable=False)
    completed_in_run_id = Column("COMPLETED_IN_RUN_ID", Integer, ForeignKey("GAME_RUNS.GAME_RUN_ID", ondelete="CASCADE"), nullable=False)
    task_line_id = Column("TASK_LINE_ID", Integer, ForeignKey("TASK_LINES.TASK_LINE_ID", ondelete="CASCADE"), nullable=False)
    bonus_points = Column("BONUS_POINTS", Integer, nullable=False, server_default="0")
    created_at = Column("CREATED_AT", Text, nullable=False, server_default="(datetime('now', 'localtime'))")

    __table_args__ = (
        UniqueConstraint("TASK_LINE_ID", name="uq_scoring_task_line_id"),
        )

    task_line = relationship("TaskLines", back_populates="scoring")
    game_run = relationship("GameRuns", foreign_keys=[game_run_id], back_populates="scoring_records")
    completed_in_run = relationship("GameRuns", foreign_keys=[completed_in_run_id], back_populates="completed_scorings")
    