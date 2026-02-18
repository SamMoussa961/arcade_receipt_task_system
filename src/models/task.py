from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Tasks(Base):
    __tablename__ = "TASKS"

    task_id = Column("TASK_ID", Integer, primary_key=True, autoincrement=True)
    game_run_id = Column("GAME_RUN_ID", Integer, ForeignKey("GAME_RUNS.GAME_RUN_ID", ondelete="CASCADE"), nullable=False)
    todo_line_id = Column("TODO_LINE_ID", Integer, ForeignKey("TODO_LINES.TODO_LINE_ID", ondelete="RESTRICT"), nullable=False)
    category_id = Column("CATEGORY_ID", Integer, ForeignKey("CATEGORIES.CATEGORY_ID", ondelete="RESTRICT"), nullable=False)
    title = Column("TITLE", Text, nullable=False)
    time_estimate = Column("TIME_ESTIMATE", Integer, nullable=True)
    deadline = Column("DEADLINE", Text, nullable=True)
    is_parent = Column("IS_PARENT", Integer, nullable=False, server_default="0")
    created_at = Column("CREATED_AT", Text, nullable=False, server_default="(datetime('now', 'localtime'))")

    __table_args__ = (
        CheckConstraint("IS_PARENT IN (0, 1)", name="ck_tasks_is_parent"),
    )

    todo_line = relationship("TodoLines", back_populates="tasks")
    category = relationship("Categories", back_populates="tasks")
    game_run = relationship("GameRuns", back_populates="tasks")
    subtasks = relationship("TaskLines", back_populates="task", cascade="all, delete-orphan")



class TaskLines(Base):
    __tablename__ = "TASK_LINES"

    task_line_id = Column("TASK_LINE_ID", Integer, primary_key=True, autoincrement=True)
    task_id = Column("TASK_ID", Integer, ForeignKey("TASKS.TASK_ID", ondelete="CASCADE"), nullable=False)
    title = Column("TITLE", Text, nullable=False)
    base_points = Column("BASE_POINTS", Integer, nullable=False)
    status = Column("STATUS", Text, nullable=False, server_default="active")
    completed_at = Column("COMPLETED_AT", Text, nullable=True)
    order_number = Column("ORDER_NUMBER", Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("TASK_ID", "ORDER_NUMBER", name="uq_task_order_number"),
        CheckConstraint("STATUS IN ('active', 'completed', 'abandoned')", name="ck_task_lines_status"),
    )

    task = relationship("Tasks", back_populates="subtasks")
    scoring = relationship("Scoring", back_populates="task_line", uselist=False)

