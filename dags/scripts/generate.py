import csv
import random
import os
from datetime import datetime, timedelta


def generate_data():
    print("🔥 RUNNING NEW CODE VERSION 🔥")

    BASE_PATH = "/opt/airflow/data"

    input_file = os.path.join(BASE_PATH, "input", "insurance.csv")
    output_file = os.path.join(BASE_PATH, "output", "claims.csv")

    # ✅ Ensure output folder exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    start_date = datetime(2024, 1, 1)

    def generate_date():
        return (start_date + timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")

    def generate_patient_id(index):
        return f"P{str(index % 20).zfill(3)}"

    def generate_hospital_id(region):
        mapping = {
            "southwest": "H01",
            "southeast": "H02",
            "northwest": "H03",
            "northeast": "H04"
        }
        return mapping.get(region, "H00")

    # ❌ Fail fast if input missing (good practice)
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.DictReader(infile)

        fieldnames = ["claim_id", "patient_id", "claim_date", "claim_amount", "hospital_id"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(reader, start=1):
            writer.writerow({
                "claim_id": f"C{str(i).zfill(3)}",
                "patient_id": generate_patient_id(i),
                "claim_date": generate_date(),
                "claim_amount": row["charges"],
                "hospital_id": generate_hospital_id(row["region"])
            })

    print(f"✅ Claims generated successfully at {output_file}")