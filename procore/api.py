import requests


def check_status() -> bool:
    response = requests.get("https://status.procore.com/api/v2/status.json")
    data = response.json()["status"]

    if (data["description"] == "All Systems Operational"
            and data["indicator"]) == "none":
        return True

    return False
