import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('myapi.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables:", tables)
        
        cursor.execute("PRAGMA table_info(question);")
        columns = cursor.fetchall()
        print("Question columns:", columns)
        
        conn.close()
    except Exception as e:
        print(f"DB check failed: {e}")

if __name__ == "__main__":
    check_db()
