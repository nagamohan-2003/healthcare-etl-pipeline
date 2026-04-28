import csv
import random
from datetime import datetime, timedelta

input_file = "insurance.csv"
output_file = "claims.csv"

start_date = datetime(2024, 1, 1)

def generate_date():
    return (start_date + timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")

def generate_patient_id(index):
    return f"P{str(index % 20).zfill(3)}"  # repeat patients

def generate_hospital_id(region):
    mapping = {
        "southwest": "H01",
        "southeast": "H02",
        "northwest": "H03",
        "northeast": "H04"
    }
    return mapping.get(region, "H00")

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    
    fieldnames = ["claim_id", "patient_id", "claim_date", "claim_amount", "hospital_id"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for i, row in enumerate(reader, start=1):
        new_row = {
            "claim_id": f"C{str(i).zfill(3)}",
            "patient_id": generate_patient_id(i),
            "claim_date": generate_date(),
            "claim_amount": row["charges"],
            "hospital_id": generate_hospital_id(row["region"])
        }
        writer.writerow(new_row)

print("claims.csv created successfully!")
