import os, psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST","localhost"), port=os.getenv("DB_PORT","5432"),
        database=os.getenv("DB_NAME","agent_db"), user=os.getenv("DB_USER","postgres"),
        password=os.getenv("DB_PASSWORD",""))

def get_today_post():
    c=get_connection()
    try:
        with c.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id,title,content,published_date FROM posts WHERE DATE(published_date)=CURRENT_DATE ORDER BY published_date DESC LIMIT 1")
            return cur.fetchone()
    finally: c.close()

def insert_mcqs(post_id, mcqs):
    c=get_connection()
    try:
        with c.cursor() as cur:
            for m in mcqs:
                cur.execute("""INSERT INTO mcqs(post_id,question,option_a,option_b,option_c,option_d,correct_answer,explanation)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                (post_id,m["question"],m["option_a"],m["option_b"],m["option_c"],m["option_d"],m["correct_answer"],m.get("explanation","")))
        c.commit()
    finally: c.close()
