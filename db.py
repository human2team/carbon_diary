import pymysql
from config import DB_CONFIG

# DB 연결 함수
def get_connection():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor      # 결과를 dict 형태로 반환
    )

# 새로운 기록 추가
def insert_entry(meal, transport, computer_hours, emissions):
    """ 하루 데이터 저장 """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO diary (entry_date, meal, transport, computer_hours, emissions)
            VALUES (CURDATE(), %s, %s, %Ss, %s)
            """
            cursor.execute(sql, (meal, transport, computer_hours, emissions))
        conn.commit()
    finally:
        conn.close()

# 최근 기록 1개 불러오기
def get_latest_entry():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM diary ORDER BY id DESC LIMIT 1")
            return cursor.fetchone()
    finally:
        conn.close()

# 전체 기록 불러오기
def get_all_entries():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM diary ORDER BY entry_date DESC")
            return cursor.fetchall()
    finally:
        conn.close()

# 기록 삭제
def delete_entry_from_db(entry_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM diary WHERE id = %s"
            cursor.execute(sql, (entry_id,))
        conn.commit()
    finally:
        conn.close()
