import csv
import os
from collections import defaultdict

def classify_data():
    BASE_PATH = "/opt/airflow/data"

    input_file = os.path.join(BASE_PATH, "output", "claims_with_issues.csv")

    valid, invalid, suspicious = [], [], []
    patient_date_map = defaultdict(int)

    with open(input_file, "r") as f:
        rows = list(csv.DictReader(f))

    # Count same-day claims
    for row in rows:
        key = (row["patient_id"], row["claim_date"])
        patient_date_map[key] += 1

    # Classify
    for row in rows:
        if row["error"]:
            invalid.append(row)
            continue

        flags = []
        key = (row["patient_id"], row["claim_date"])

        if patient_date_map[key] > 1:
            flags.append("Multiple claims same day")

        if float(row["claim_amount"]) > 20000:
            flags.append("High claim amount")

        if flags:
            row["flag"] = "; ".join(flags)
            suspicious.append(row)
        else:
            valid.append(row)

    def write_csv(path, data):
        if not data:
            return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    write_csv(os.path.join(BASE_PATH, "output", "valid_claims.csv"), valid)
    write_csv(os.path.join(BASE_PATH, "output", "invalid_claims.csv"), invalid)
    write_csv(os.path.join(BASE_PATH, "output", "suspicious_claims.csv"), suspicious)

    print("Classification done")
