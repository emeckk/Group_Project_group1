from flask import Flask, request, jsonify
import psycopg2
from config import config

app = Flask(__name__) # Create a Flask application instance

#For adding a new row in time_entry via POSTMAN
@app.route('/api/time-entry', methods=['POST'])
def add_time_entry():
    params = config()
    conn = psycopg2.connect(**params) #connect to the db
    data = request.get_json() #Parse JSON data from the post request

    report_date = data['reportDate'] #Timestamp       
    start_time = data['startTime'] #Time         
    end_time = data['endTime'] #Time           
    lunch_break = data['lunchBreak'] #Interval
    consultant_id = data['consultantId'] #foreign key id that connects the entry to consultants table
    customer_name = data['customerName'] #Teeext

    #Insert the data into the time_entries table
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO time_entries (report_date, start_time, end_time, lunch_break, consultant_id, customer_name)
        VALUES (%s, %s, %s, %s::interval, %s, %s)
    """, (report_date, start_time, end_time, lunch_break, consultant_id, customer_name))

    #Calculate the working time, start_time to end_time - the lunch break time and
    #update the said consultants time_balance based on this value
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


@app.route('/api/time-entry', methods=['GET'])
def get_time_entry():
    params = config()
    conn = psycopg2.connect(**params) #connect to the db
    data = request.get_json() #Parse JSON data from the post request

    #Get the data from the time_entries table
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM time_entries)
    """,)

    conn.commit()
    cur.close()

    return jsonify({"message": "Current state of time_entries table"}), 201

#For adding a new row in consultant via POSTMAN
#name TEXT and time_balance, time balance is 0 to start of with for new consultants
@app.route('/api/consultant', methods=['POST'])
def add_consultant():
    params = config()
    conn = psycopg2.connect(**params) #connect to the db

    data = request.get_json() #parse JSON data from the post request
    consultant_name = data['consultantName']

    #Insert the data into the consultants table
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

@app.route('/api/consultant', methods=['GET'])
def get_consultants():
    params = config()
    conn = psycopg2.connect(**params) #connect to the db
    data = request.get_json() #Parse JSON data from the post request

    #Get the data from the time_entries table
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM consultants
    """,)

    conn.commit()
    cur.close()

    return jsonify({"message": "Current state of consultants table"}), 201

if __name__ == "__main__":
    app.run(debug=True)
