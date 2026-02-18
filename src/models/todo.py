from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


'''
CREATE TABLE TODOS(
    INPUT_ID            INTEGER         PRIMARY KEY AUTOINCREMENT,
    RAW_INPUT           TEXT            NOT NULL,
    CREATED_AT          TEXT            NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);

CREATE TABLE TODO_LINES(
    TODO_LINE_ID        INTEGER         PRIMARY KEY AUTOINCREMENT,
    INPUT_ID            INTEGER         NOT NULL,
    TODO_LINE           TEXT            NOT NULL,
    LINE_NUMBER         INTEGER         NOT NULL,
    CONSTRAINT TODO_LINES_TODOS_FK FOREIGN KEY (INPUT_ID) REFERENCES TODOS(INPUT_ID) ON DELETE CASCADE,
        UNIQUE (INPUT_ID, LINE_NUMBER)
);
'''
class Todos(Base):
    __tablename__ = "TODOS"

    input_id = Column("INPUT_ID", Integer, primary_key=True, autoincrement=True)
    raw_input = Column("RAW_INPUT", Text, nullable=False)
    created_at = Column("CREATED_AT", Text, nullable=False, server_default="(datetime('now', 'localtime'))")

    # Relationships one->many
    lines = relationship("TodoLines", back_populates="todo", cascade="all, delete-orphan")

class TodoLines(Base):
    __tablename__ = "TODO_LINES"

    todo_line_id = Column("TODO_LINE_ID", Integer, primary_key=True, autoincrement=True)
    input_id = Column("INPUT_ID", Integer, ForeignKey("TODOS.INPUT_ID", ondelete="CASCADE"), nullable=False)
    todo_line = Column("TODO_LINE", Text, nullable=False)
    line_number = Column("LINE_NUMBER", Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("INPUT_ID", "LINE_NUMBER", name="uq_todo_line_number"),
    )


    todo = relationship("Todos", back_populates="lines")
    tasks = relationship("Tasks", back_populates="todo_line")
    llm_logs = relationship("LlmLogs", back_populates="todo_line")
