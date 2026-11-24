
import requests
import getpass
import json

BASE_URL = "http://localhost:8080"

# Get Airflow credentials securely
username = input("Airflow username: ")
password = getpass.getpass("Airflow password: ")

# Step 1: Generate JWT token
response = requests.post(
    f"{BASE_URL}/auth/token",
    json={
        "username": username,
        "password": password
    },
    timeout=15
)

print("\nAuthentication HTTP Status:", response.status_code)

if response.status_code not in (200, 201):
    print("Authentication failed:", response.text)
    raise SystemExit

token = response.json()["access_token"]

print("JWT authentication successful!")

# Step 2: Fetch latest DAG runs
headers = {
    "Authorization": f"Bearer {token}"
}

runs_response = requests.get(
    f"{BASE_URL}/api/v2/dags/ecommerce_data_pipeline/dagRuns",
    headers=headers,
    params={
        "limit": 5,
        "order_by": "-logical_date"
    },
    timeout=15
)

print("\nDAG Runs HTTP Status:", runs_response.status_code)

if runs_response.status_code == 200:
    runs = runs_response.json().get("dag_runs", [])
    print("Latest DAG Runs:")

    for run in runs:
        print(
            "Run ID:", run.get("dag_run_id"),
            "| State:", run.get("state"),
            "| Start:", run.get("start_date"),
            "| End:", run.get("end_date")
        )
else:
    print(runs_response.text)
