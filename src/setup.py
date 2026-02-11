from db_tools.db import initialize_db, get_connection

initialize_db()

with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT CATEGORY_NAME FROM CATEGORIES WHERE IS_SYSTEM=1")
    print(cursor.fetchall())
