from sqlalchemy import Column, Integer, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base

'''
CREATE TABLE LLM_LOGS(
    LLM_LOG_ID          INTEGER         PRIMARY KEY AUTOINCREMENT,
    TODO_LINE_ID        INTEGER         NOT NULL,
    MODEL_NAME          TEXT,
    RAW_PROMPT          TEXT            NOT NULL,
    RAW_RESPONSE        TEXT            NOT NULL,
    PARSED_JSON         TEXT,
    SUCCESS             INTEGER         NOT NULL DEFAULT 0 CHECK (SUCCESS IN (0, 1)),
    ERROR_MESSAGE       TEXT,
    PROCESSING_TIME_MS  INTEGER,
    CREATED_AT          TEXT            NOT NULL DEFAULT (datetime('now', 'localtime')),
    CONSTRAINT LLM_LOGS_TODO_LINES_FK FOREIGN KEY (TODO_LINE_ID) REFERENCES TODO_LINES(TODO_LINE_ID) ON DELETE RESTRICT
);
'''
class LlmLogs(Base):
    __tablename__ = "LLM_LOGS"

    llm_log_id = Column("LLM_LOG_ID", Integer, primary_key=True, autoincrement=True)
    todo_line_id = Column("TODO_LINE_ID", Integer, ForeignKey("TODO_LINES.TODO_LINE_ID", ondelete="RESTRICT"), nullable=False)
    model_name = Column("MODEL_NAME", Text, nullable=True)
    raw_prompt = Column("RAW_PROMPT", Text, nullable=False)
    raw_response = Column("RAW_RESPONSE", Text, nullable=False)
    parsed_json = Column("PARSED_JSON", Text, nullable=True)
    success = Column("SUCCESS", Integer, nullable=False, server_default="0")
    error_message = Column("ERROR_MESSAGE", Text, nullable=True)
    processing_time_ms = Column("PROCESSING_TIME_MS", Integer, nullable=True)
    created_at = Column("CREATED_AT", Text, nullable=False, server_default="(datetime('now', 'localtime'))")

    __table_args__ = (
        CheckConstraint("SUCCESS IN (0, 1)", name="ck_llm_logs_success"),
    )

    todo_line = relationship("TodoLines", back_populates="llm_logs")