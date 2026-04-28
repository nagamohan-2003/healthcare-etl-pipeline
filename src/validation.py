import csv
from collections import defaultdict

input_file = "claims_with_issues.csv"

valid = []
invalid = []
suspicious = []

seen_claim_ids = set()
patient_date_map = defaultdict(int)

# First pass: count patient-date occurrences
with open(input_file, "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

    for row in rows:
        key = (row["patient_id"], row["claim_date"])
        patient_date_map[key] += 1

# Second pass: classify
for row in rows:
    errors = []
    flags = []

    # Invalid checks
    if not row["patient_id"]:
        errors.append("Missing patient_id")

    if float(row["claim_amount"]) <= 0:
        errors.append("Invalid claim_amount")

    if row["hospital_id"] not in ["H01", "H02", "H03", "H04"]:
        errors.append("Invalid hospital_id")

    # Suspicious checks
    key = (row["patient_id"], row["claim_date"])

    if patient_date_map[key] > 1:
        flags.append("Multiple claims same day")

    if float(row["claim_amount"]) > 20000:
        flags.append("High claim amount")

    # Classification
    if errors:
        invalid.append(row)
    elif flags:
        suspicious.append(row)
    else:
        valid.append(row)

print("Valid:", len(valid))
print("Invalid:", len(invalid))
print("Suspicious:", len(suspicious))

def write_csv(filename, data):
    if not data:
        return
    
    fieldnames = data[0].keys()
    
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

write_csv("valid_claims.csv", valid)
write_csv("invalid_claims.csv", invalid)
write_csv("suspicious_claims.csv", suspicious)


