import psycopg2
from config import config
from datetime import datetime

def generate_report(filename="report.txt"):
    # Connect to DB
    conn = psycopg2.connect(**config())
    cur = conn.cursor()

    ### DAILY REPORT ###
    daily_query = """
    SELECT
        c.name AS consultant_name,
        c.customer_name,
        te.report_date::date,
        SUM(te.end_time - te.start_time - te.lunch_break) AS total_worked
    FROM time_entries te
    JOIN consultants c ON te.consultant_id = c.id
    GROUP BY c.name, c.customer_name, te.report_date
    ORDER BY te.report_date, c.name;
    """
    cur.execute(daily_query)
    daily_rows = cur.fetchall()

    ### WEEKLY REPORT (per consultant and customer) ###
    weekly_query = """
    SELECT
        c.name AS consultant_name,
        c.customer_name,
        EXTRACT(YEAR FROM te.report_date) AS year,
        EXTRACT(WEEK FROM te.report_date) AS week,
        FLOOR(SUM(EXTRACT(EPOCH FROM (te.end_time - te.start_time - te.lunch_break)) / 3600)) AS hours,
        FLOOR(MOD(SUM(EXTRACT(EPOCH FROM (te.end_time - te.start_time - te.lunch_break)) / 60), 60)) AS minutes,
        COUNT(DISTINCT te.report_date) AS work_days,
        SUM(EXTRACT(EPOCH FROM (te.end_time - te.start_time - te.lunch_break)) / 3600) / COUNT(DISTINCT te.report_date) AS avg_hours_per_day
    FROM time_entries te
    JOIN consultants c ON te.consultant_id = c.id
    GROUP BY c.name, c.customer_name, year, week
    ORDER BY year, week, c.name;

    """
    cur.execute(weekly_query)
    weekly_rows = cur.fetchall()

    ### WEEKLY TOTALS BY CUSTOMER ###
    customer_weekly_query = """
    SELECT
        c.customer_name,
        EXTRACT(YEAR FROM te.report_date) AS year,
        EXTRACT(WEEK FROM te.report_date) AS week,
        FLOOR(SUM(EXTRACT(EPOCH FROM (te.end_time - te.start_time - te.lunch_break)) / 3600)) AS hours,
        FLOOR(MOD(SUM(EXTRACT(EPOCH FROM (te.end_time - te.start_time - te.lunch_break)) / 60), 60)) AS minutes
    FROM time_entries te
    JOIN consultants c ON te.consultant_id = c.id
    GROUP BY c.customer_name, year, week
    ORDER BY year, week, c.customer_name;
    """
    cur.execute(customer_weekly_query)
    customer_weekly_rows = cur.fetchall()

    ### WRITE REPORT ###
    with open(filename, "w") as f:
        f.write(f"Consultant Time Tracking Report (Generated {datetime.now():%Y-%m-%d %H:%M:%S})\n")
        f.write("=" * 80 + "\n\n")

        # Daily totals
        f.write("DAILY TOTALS:\n")
        f.write("-" * 80 + "\n")
        for row in daily_rows:
            consultant, customer, date, worked = row
            total_seconds = worked.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            f.write(f"{date} | {consultant:<15} | {customer:<20} | {hours:02d}:{minutes:02d}\n")

    # Weekly totals per consultant + customer with average hours/day
        f.write("\nWEEKLY TOTALS (PER CONSULTANT):\n")
        f.write("-" * 80 + "\n")
        for row in weekly_rows:
            consultant, customer, year, week, hours, minutes, work_days, avg_hours_per_day = row
    
    # Convert avg_hours_per_day (float) to HH:MM format
            avg_hours_int = int(avg_hours_per_day)
            avg_minutes = int(round((avg_hours_per_day - avg_hours_int) * 60))
            avg_str = f"{avg_hours_int:02d}:{avg_minutes:02d}"
    
            f.write(
                f"Week {int(week):02d}, {int(year)} | "
        f"{consultant:<15} | {customer:<17} | "
        f"{int(hours):02d}:{int(minutes):02d} | "
        f"Daily Average: {avg_str}\n"
)


        # Weekly totals per customer
        f.write("\nWEEKLY TOTALS (PER CUSTOMER):\n")
        f.write("-" * 80 + "\n")
        for row in customer_weekly_rows:
            customer, year, week, hours, minutes = row
            f.write(f"Week {int(week):02d}, {int(year)} | {customer:<15} | {int(hours):02d}:{int(minutes):02d}\n")

    cur.close()
    conn.close()
    print(f"Report written to {filename}")
