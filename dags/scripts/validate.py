import csv
import os

def validate_data():
    BASE_PATH = "/opt/airflow/data"

    input_file = os.path.join(BASE_PATH, "output", "claims.csv")
    output_file = os.path.join(BASE_PATH, "output", "claims_with_issues.csv")

    valid_hospitals = ["H01", "H02", "H03", "H04"]

    with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["error"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            errors = []

            if not row["patient_id"]:
                errors.append("Missing patient_id")

            if float(row["claim_amount"]) <= 0:
                errors.append("Invalid claim_amount")

            if row["hospital_id"] not in valid_hospitals:
                errors.append("Invalid hospital_id")

            row["error"] = "; ".join(errors)
            writer.writerow(row)

    print("Validation complete")