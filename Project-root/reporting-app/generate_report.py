import psycopg2

conn = psycopg2.connect(
    host="your_postgres_server",
    database="your_db",
    user="your_user",
    password="your_password",
    port=5432
)
cur = conn.cursor()

query = """
SELECT consultant_name, customer_name, SUM(hours) as total_hours, date_trunc('week', work_date) as week_start
FROM time_tracking
GROUP BY consultant_name, customer_name, week_start
ORDER BY week_start;
"""

cur.execute(query)
rows = cur.fetchall()

with open("report.txt", "w") as f:
    for row in rows:
        f.write(f"{row[0]} worked {row[2]} hours for {row[1]} in week starting {row[3]}\n")

cur.close()
conn.close()
