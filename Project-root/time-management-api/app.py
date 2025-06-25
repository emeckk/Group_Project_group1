from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Azure PostgreSQL connection
conn = psycopg2.connect(
    host="db-timereport.postgres.database.azure.com",
    database="timereport",
    user="ghostbusters",
    password="Kanyeisreal1",
    sslmode="require"
)

from datetime import datetime, timedelta

@app.route('/api/time-entry', methods=['POST'])
def add_time_entry():
    data = request.get_json()

    report_date = data['reportDate']           # e.g. "2025-06-25"
    start_time = data['startTime']             # e.g. "09:00:00"
    end_time = data['endTime']                 # e.g. "17:00:00"
    lunch_break = data['lunchBreak']           # e.g. "00:30:00"
    consultant_id = data['consultantId']
    customer_name = data['customerName']

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO time_entries (report_date, start_time, end_time, lunch_break, consultant_id, customer_name)
        VALUES (%s, %s, %s, %s::interval, %s, %s)
    """, (report_date, start_time, end_time, lunch_break, consultant_id, customer_name))

    # Calculate worked time = (end_time - start_time - lunch_break)
    # PostgreSQL can do this for you in SQL:
    cur.execute("""
    WITH latest_time_entry AS (
        SELECT start_time, end_time, lunch_break
        FROM time_entries
        WHERE consultant_id = %s
        ORDER BY id DESC
        LIMIT 1
    )
    UPDATE consultants
    SET total_balance = total_balance + (
        (latest_time_entry.end_time - latest_time_entry.start_time) - latest_time_entry.lunch_break
    )
    FROM latest_time_entry
    WHERE consultants.id = %s
""", (consultant_id, consultant_id))

    conn.commit()
    cur.close()

    return jsonify({"message": "Time entry added and balance updated"}), 201



@app.route('/api/consultant', methods=['POST'])
def add_consultant():
    data = request.get_json()
    consultant_name = data['consultantName']

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO consultants (name)
            VALUES (%s)
            RETURNING id
        """, (consultant_name,))
        consultant_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        return jsonify({
            "message": "Consultant added",
            "consultantId": consultant_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
