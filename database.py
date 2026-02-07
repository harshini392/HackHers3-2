import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hackhers3"
    )

def insert_review(brand, review, language, sentiment):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)

    sql = """
    INSERT INTO reviews (brand, review, language, sentiment)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (brand, review, language, sentiment))

    conn.commit()
    cursor.close()
    conn.close()

def fetch_all_reviews():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM reviews ORDER BY created_at ASC")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows