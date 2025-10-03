import pymysql
from config import DB_CONFIG

def get_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_entry(meal, transport, computer_hours, emissions):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO diary (entry_date, meal, transport, computer_hours, emissions)
            VALUES (CURDATE(), %s, %s, %s, %s)
            """
            cursor.execute(sql, (meal, transport, computer_hours, emissions))
        conn.commit()
    finally:
        conn.close()

def get_latest_entry():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM diary ORDER BY id DESC LIMIT 1")
            return cursor.fetchone()
    finally:
        conn.close()

def get_all_entries():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM diary ORDER BY entry_date DESC")
            return cursor.fetchall()
    finally:
        conn.close()
