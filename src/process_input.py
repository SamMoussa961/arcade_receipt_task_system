from pathlib import Path
from db_tools.db import initialize_db, get_connection

#BASE_DIR = Path(__file__).resolve().parent

#INPUTS_DIR = BASE_DIR / "inputs"
#TODO_LIST_PATH = _DIR / "todo.txt"

def process_input(file_path: str = "todo.txt"):

    initialize_db()


    with open(file_path, encoding="utf-8") as f:
        raw_input = f.read();

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO TODOS (RAW_INPUT) VALUES (?)", (raw_input,))
        

        input_id = cursor.lastrowid

        lines = [line.strip() for line in raw_input.split('\n') if line.strip()]

        for line_number, todo_line in enumerate(lines, start=1):
            cursor.execute("""
            INSERT INTO TODO_LINES (INPUT_ID, TODO_LINE, LINE_NUMBER)
            VALUES (?, ?, ?)
            """, (input_id, todo_line, line_number))

        conn.commit()
        print(f"Processed {len(lines)} todos (INPUT_ID: {input_id})")
        return input_id

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        raise
    
    finally:
        conn.close()