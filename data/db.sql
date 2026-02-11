/**********************************************************************************************************

** USER TODO LIST INPUT + DIVIDED INTO LINES **
TODOS: INPUT_ID, RAW_INPUT, CREATED_AT
TODO_LINE: TODO_LINE_ID(PK), INPUT_ID(FK), TODO_LINE, LINE_NUMBER

** TASK CATEGORIES **
CATEGORIES: CATEGORY_ID(PK), CATEGORY_NAME, POINTS_WEIGHT, COLOR, ICON

** GAME SESSIONS
GAME_RUNS: GAME_RUN_ID(PK), RUN_DATE, STARTED_AT, ENDED_AT, TOTAL_SCORE, STATUS

** PARENT TASKS AND THEIR SUBTASKS **
TASKS: TASK_ID(PK), GAME_RUN_ID(FK), TODO_LINE_ID(FK), CATEGORY_ID(FK), TITLE, TIME_ESTIMATE, 
        DEADLINE, IS_PARENT, CREATED_AT

TASK_LINE: TASK_LINE_ID(PK), TASK_ID(FK), TITLE. BASE_POINTS, STATUS, COMPLETED_AT, ORDER_NUMBER

** SCORING RECORDS **
SCORING: SCORE_ID(PK), GAME_RUN_ID(FK), COMPLETED_IN_RUN_ID(FK), TASK_LINE_ID(FK), 
            BONUS_POINTS, CREATED_AT
STREAKS: STREAK_ID, CATEGORY_ID, CURRENT_STREAK, LONGEST_STREAK, LAST_COMPLETED_DATE, 
            TOTAL_COMPLETIONS, UPDATED_AT

** LLM PROCESSING LOGS **
LLM_LOGS: LLM_LOG_ID(PK), TODO_LINE_ID(FK), RAW_RESPONSE, PARSED_JSON, SUCCESS, ERROR_MESSAGE, CREATED_AT 

************************************************************************************************************/


-- Drop tables in reverse order based on dependencies
DROP TABLE IF EXISTS SCORING;
DROP TABLE IF EXISTS TASK_LINES;
DROP TABLE IF EXISTS TASKS;
DROP TABLE IF EXISTS STREAKS;
DROP TABLE IF EXISTS LLM_LOGS;
DROP TABLE IF EXISTS GAME_RUNS;
DROP TABLE IF EXISTS TODO_LINES;
DROP TABLE IF EXISTS TODOS;
DROP TABLE IF EXISTS CATEGORIES;
-----------------------------------------------------------------------------------

-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Create TODOS table to store raw user input for TODO lists -- No dependencies
-- TODOS: INPUT_ID, RAW_INPUT, CREATED_AT 
CREATE TABLE TODOS(
    INPUT_ID            INTEGER         PRIMARY KEY AUTOINCREMENT,
    RAW_INPUT           TEXT            NOT NULL,
    CREATED_AT          TEXT            NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);

-- CATEGORIES: CATEGORY_ID(PK), CATEGORY_NAME, POINTS_WEIGHT, COLOR, ICON
-- Create CATEGORIES table to store task categories -- No dependencies, but other tables will reference this for categorizing tasks and applying point weights
CREATE TABLE CATEGORIES(
    CATEGORY_ID         INTEGER         PRIMARY KEY AUTOINCREMENT,
    CATEGORY_NAME       TEXT            NOT NULL UNIQUE,
    POINTS_WEIGHT       REAL            DEFAULT 1.0,
    IS_SYSTEM           INTEGER         DEFAULT 0 CHECK (IS_SYSTEM IN (0, 1)),
    COLOR               TEXT,
    ICON                TEXT
);

-- Create TODO_LINES table to store individual lines parsed from the raw input -- Dependency on TODOS to link lines to original input
-- TODO_LINE: TODO_LINE_ID(PK), INPUT_ID(FK), TODO_LINE, LINE_NUMBER
CREATE TABLE TODO_LINES(
    TODO_LINE_ID        INTEGER         PRIMARY KEY AUTOINCREMENT,
    INPUT_ID            INTEGER         NOT NULL,
    TODO_LINE           TEXT            NOT NULL,
    LINE_NUMBER         INTEGER         NOT NULL,
    CONSTRAINT TODO_LINES_TODOS_FK FOREIGN KEY (INPUT_ID) REFERENCES TODOS(INPUT_ID) ON DELETE CASCADE,
        UNIQUE (INPUT_ID, LINE_NUMBER)
);

-- GAME_RUNS: GAME_RUN_ID(PK), RUN_DATE, STARTED_AT, ENDED_AT, TOTAL_SCORE, STATUS
-- Create GAME_RUNS table to track individual game sessions -- No dependencies
CREATE TABLE GAME_RUNS(
    GAME_RUN_ID         INTEGER         PRIMARY KEY AUTOINCREMENT,
    RUN_DATE            TEXT            NOT NULL DEFAULT (datetime('now', 'localtime')),
    STARTED_AT          TEXT            NOT NULL DEFAULT (datetime('now', 'localtime')),
    ENDED_AT            TEXT,
    TOTAL_SCORE         INTEGER         DEFAULT 0,
    STATUS              TEXT            NOT NULL DEFAULT 'active' CHECK (STATUS IN ('active', 'completed', 'abandoned'))
);

-- Create LLM_LOGS table to track interactions with the language model -- Dependency on TODO_LINES to link logs to specific tasks
-- LLM_LOGS: LLM_LOG_ID(PK), TODO_LINE_ID(FK), RAW_RESPONSE, PARSED_JSON, SUCCESS, ERROR_MESSAGE, CREATED_AT 
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

-- TASKS: TASK_ID(PK), GAME_RUN_ID(FK), TODO_LINE_ID(FK), CATEGORY_ID(FK), TITLE, TIME_ESTIMATE, 
--        DEADLINE, IS_PARENT, CREATED_AT
-- Create TASKS table to store parent tasks 
-- Dependencies on GAME_RUNS, TODO_LINES, and CATEGORIES to link tasks to specific game sessions, original input lines, and categories
CREATE TABLE TASKS(
    TASK_ID             INTEGER         PRIMARY KEY AUTOINCREMENT,
    GAME_RUN_ID         INTEGER         NOT NULL,
    TODO_LINE_ID        INTEGER         NOT NULL,
    CATEGORY_ID         INTEGER         NOT NULL,
    TITLE               TEXT            NOT NULL,
    TIME_ESTIMATE       INTEGER,
    DEADLINE            TEXT,
    IS_PARENT           INTEGER         NOT NULL DEFAULT 0 CHECK (IS_PARENT IN (0, 1)),
    CREATED_AT          TEXT            NOT NULL DEFAULT (datetime('now', 'localtime')),
    CONSTRAINT TASKS_GAME_RUNS_FK FOREIGN KEY (GAME_RUN_ID) REFERENCES GAME_RUNS(GAME_RUN_ID) ON DELETE CASCADE,
    CONSTRAINT TASKS_TODO_LINES_FK FOREIGN KEY (TODO_LINE_ID) REFERENCES TODO_LINES(TODO_LINE_ID) ON DELETE RESTRICT,
    CONSTRAINT TASKS_CATEGORIES_FK FOREIGN KEY (CATEGORY_ID) REFERENCES CATEGORIES(CATEGORY_ID) ON DELETE RESTRICT
);

--TASK_LINE: TASK_LINE_ID(PK), TASK_ID(FK), TITLE. BASE_POINTS, STATUS, COMPLETED_AT, ORDER_NUMBER
-- Create TASK_LINES table to store subtasks for each parent task -- Dependency on TASKS to link subtasks to their parent tasks
CREATE TABLE TASK_LINES(
    TASK_LINE_ID        INTEGER         PRIMARY KEY AUTOINCREMENT,
    TASK_ID             INTEGER         NOT NULL,
    TITLE               TEXT            NOT NULL,
    BASE_POINTS         INTEGER         NOT NULL,
    STATUS              TEXT            NOT NULL DEFAULT 'active' CHECK (STATUS IN ('active', 'completed', 'abandoned')),
    COMPLETED_AT        TEXT,
    ORDER_NUMBER        INTEGER         NOT NULL,
    CONSTRAINT TASK_LINES_TASKS_FK FOREIGN KEY (TASK_ID) REFERENCES TASKS(TASK_ID) ON DELETE CASCADE,
    UNIQUE (TASK_ID, ORDER_NUMBER)
);

-- SCORING: SCORE_ID(PK), GAME_RUN_ID(FK), TASK_LINE_ID(FK), BONUS_POINTS, CREATED_AT
-- Create SCORING table to track points awarded for each completed task line -- Dependencies on GAME_RUNS and TASK_LINES to link scores to specific game sessions and tasks
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

-- Create STREAKS table to track user streaks for each category -- Dependency on CATEGORIES to link streaks to specific categories
-- STREAKS: STREAK_ID, CATEGORY_ID, CURRENT_STREAK, LONGEST_STREAK, LAST_COMPLETED_DATE, 
--            TOTAL_COMPLETIONS, UPDATED_AT
CREATE TABLE STREAKS(
    STREAK_ID           INTEGER         PRIMARY KEY AUTOINCREMENT,
    CATEGORY_ID         INTEGER         NOT NULL UNIQUE,
    CURRENT_STREAK      INTEGER         DEFAULT 0,
    LONGEST_STREAK      INTEGER         DEFAULT 0,
    LAST_COMPLETED_DATE TEXT,
    TOTAL_COMPLETIONS   INTEGER         DEFAULT 0,
    UPDATED_AT          TEXT            DEFAULT (datetime('now', 'localtime')),
    CONSTRAINT STREAKS_CATEGORIES_FK FOREIGN KEY (CATEGORY_ID) REFERENCES CATEGORIES(CATEGORY_ID) ON DELETE CASCADE
);

-- Triggers to enforce data integrity and business rules
CREATE TRIGGER enforce_scoring_game_run
BEFORE INSERT ON SCORING
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'GAME_RUN_ID must match task''s original game run')
    WHERE NEW.GAME_RUN_ID != (
        SELECT t.GAME_RUN_ID 
        FROM TASK_LINES tl
        JOIN TASKS t ON tl.TASK_ID = t.TASK_ID
        WHERE tl.TASK_LINE_ID = NEW.TASK_LINE_ID
    );
END;

-- Indexes to optimize query performance
CREATE INDEX idx_tasks_game_run ON TASKS(GAME_RUN_ID);
CREATE INDEX idx_tasks_category ON TASKS(CATEGORY_ID);
CREATE INDEX idx_task_lines_task ON TASK_LINES(TASK_ID);
CREATE INDEX idx_task_lines_status ON TASK_LINES(STATUS);
CREATE INDEX idx_scoring_game_run ON SCORING(GAME_RUN_ID);
CREATE INDEX idx_game_runs_date ON GAME_RUNS(RUN_DATE);
CREATE INDEX idx_streaks_category ON STREAKS(CATEGORY_ID);
CREATE INDEX idx_scoring_completed_run ON SCORING(COMPLETED_IN_RUN_ID);

-- View to aggregate scoring details for easier querying and reporting
CREATE VIEW SCORING_DETAILS AS
SELECT 
    s.SCORE_ID,
    s.GAME_RUN_ID,
    s.COMPLETED_IN_RUN_ID,
    s.TASK_LINE_ID,
    s.BONUS_POINTS,
    s.CREATED_AT,
    tl.BASE_POINTS,
    tl.BASE_POINTS + s.BONUS_POINTS AS TOTAL_POINTS,
    tl.TITLE AS SUBTASK_TITLE,
    tl.STATUS,
    t.TASK_ID,
    t.TITLE AS TASK_TITLE,
    t.CATEGORY_ID,
    c.CATEGORY_NAME,
    c.POINTS_WEIGHT,
    gr_created.RUN_DATE AS TASK_CREATED_DATE,
    gr_completed.RUN_DATE AS COMPLETED_DATE
FROM SCORING s
JOIN TASK_LINES tl ON s.TASK_LINE_ID = tl.TASK_LINE_ID
JOIN TASKS t ON tl.TASK_ID = t.TASK_ID
JOIN CATEGORIES c ON t.CATEGORY_ID = c.CATEGORY_ID
JOIN GAME_RUNS gr_created ON s.GAME_RUN_ID = gr_created.GAME_RUN_ID
JOIN GAME_RUNS gr_completed ON s.COMPLETED_IN_RUN_ID = gr_completed.GAME_RUN_ID;

-- Insert initial categories with appropriate point weights, colors, and icons
INSERT INTO CATEGORIES (CATEGORY_NAME, POINTS_WEIGHT, IS_SYSTEM, COLOR, ICON) VALUES 
('MAINTENANCE', 2.0, 1, '#006d8f', '../../../assets/maintenance.png'),
('ASSIGNMENT', 1.0, 1, '#ff6a00', '../../../assets/assignment.png'),
('FOCUS', 3.0, 1, '#7b219f', '../../../assets/focus.png'),
('WELLNESS', 1.2, 1, '#77bb41', '../../../assets/wellness.png'),
('ERRANDS', 1.2, 1, '#6f7608', '../../../assets/errands.png');
