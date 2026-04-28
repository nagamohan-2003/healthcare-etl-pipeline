import csv
import psycopg2

def load_data():
    print("🚀 Loading data into PostgreSQL")

    file_path = "/opt/airflow/data/output/suspicious_claims.csv"

    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )

    cursor = conn.cursor()

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute("""
                INSERT INTO claims (
                    claim_id, patient_id, claim_date,
                    claim_amount, hospital_id, status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                row["claim_id"],
                row["patient_id"],
                row["claim_date"],
                float(row["claim_amount"]),
                row["hospital_id"],
                "SUSPICIOUS"
            ))

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Data loaded into PostgreSQL")
