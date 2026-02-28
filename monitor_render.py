import os
import time
import requests

API_KEY = "rnd_r9eB71jm8C7CLa3xH1rBlFTvySqT"
SERVICE_ID = "srv-d6hi3bogjchc73cp1av0"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
BASE_URL = "https://api.render.com/v1"


def get_latest_deploy():
    url = f"{BASE_URL}/services/{SERVICE_ID}/deploys"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    deploys = response.json()
    if not deploys:
        return None
    return deploys[0]["deploy"]


def get_deploy_logs(deploy_id):
    url = f"{BASE_URL}/services/{SERVICE_ID}/deploys/{deploy_id}/logs"
    print(f"Fetching logs from: {url}")
    # Render API does not have a direct historical deploy log endpoint in the same way,
    # but the service logs endpoint can be streamed.
    # However, let's just trigger a deploy and stream the service logs since we 
    # are interested in the *current* state.
    pass

def trigger_deploy():
    url = f"{BASE_URL}/services/{SERVICE_ID}/deploys"
    response = requests.post(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["id"]

def monitor_service():
    print(f"Monitoring Service {SERVICE_ID}...")
    known_log_ids = set()
    while True:
        url = f"{BASE_URL}/services/{SERVICE_ID}/logs?limit=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            logs = response.json()
            logs.reverse() # Print oldest to newest
            for log in logs:
                log_id = log.get("id", log["cursor"])
                if log_id not in known_log_ids:
                    print(log["log"]["text"], end="")
                    known_log_ids.add(log_id)
        
        # Check deployment status
        latest_deploy = get_latest_deploy()
        if latest_deploy:
            status = latest_deploy["status"]
            if status in ["live", "build_failed", "update_failed", "canceled"]:
                print(f"\n--- Deployment {latest_deploy['id']} finished with status: {status} ---")
                if status != "live":
                    print("\n[!] Errors detected! Please review the console output.")
                else:
                    print("\n[+] Deployment successful and live!")
                break
                
        time.sleep(5)

if __name__ == "__main__":
    latest = get_latest_deploy()
    if latest and latest["status"] == "build_in_progress":
        print(f"Tracking ongoing deployment {latest['id']}...")
        monitor_service()
    else:
        print("Triggering new deployment...")
        deploy_id = trigger_deploy()
        print(f"Triggered deployment {deploy_id}. Tracking logs...")
        time.sleep(2) # Wait for it to register
        monitor_service()
