Healthcare Claims ETL Pipeline (Airflow + PostgreSQL + Docker)

 Project Overview
Designed and implemented a production-style ETL pipeline to process healthcare claims data using Apache Airflow. The pipeline performs data ingestion, validation, anomaly detection, classification, and persists high-risk records into PostgreSQL.

This project simulates real-world data engineering challenges including data quality enforcement, pipeline orchestration, containerized environments, and database integration.



Problem Statement
Healthcare claim data is often noisy and error-prone. Invalid or suspicious claims can lead to financial losses and compliance issues.

 Objective:
- Detect bad data early
- Classify risky claims
- Store structured data for downstream analysis

Architecture
Raw CSV → Data Generation → Validation → Classification → PostgreSQL


 Pipeline Orchestration:
- Apache Airflow DAG
- Task dependencies with retry handling
- Modular Python-based processing

---

 Tech Stack

| Layer            | Technology              |
|------------------|------------------------|
| Orchestration    | Apache Airflow         |
| Processing       | Python (Modular Scripts)|
| Database         | PostgreSQL             |
| Containerization | Docker                 |
| Data Format      | CSV                    |

---

 Pipeline Workflow

 Data Generation
- Reads raw insurance dataset
- Transforms into structured claim records
- Adds synthetic attributes (claim_id, hospital_id, timestamps)

---

### 2️⃣ Data Validation
Implemented rule-based validation logic:
- Missing / null patient IDs
- Invalid or extreme claim amounts
- Incorrect region → hospital mappings

 Invalid records are flagged for downstream handling

---

 Data Classification
Claims are categorized into:
- ✅ Valid
- ❌ Invalid
- ⚠️ Suspicious (high-risk patterns)

---

 Data Loading
- Suspicious claims are inserted into PostgreSQL
- Uses `psycopg2` for database interaction
- Ensures schema alignment and type consistency

---

 Containerized Execution

- Full pipeline runs inside Docker
- Handles real-world issues like:
  - File path mismatches (`/opt/airflow/...`)
  - Dependency management
  - Service communication (Airflow ↔ Postgres)

---

 Sample Query

```sql
SELECT claim_id, patient_id, claim_amount, status
FROM claims
LIMIT 5;

How to Run
docker-compose up -d

Access Airflow UI:
http://localhost:8080

Trigger DAG:
healthcare_pipeline


