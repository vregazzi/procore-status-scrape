import requests


def check_status() -> bool:
    """
    Check the status of Procore's API and return True if
    'All Systems Operational'.
    """
    response = requests.get("https://status.procore.com/api/v2/status.json")
    data = response.json()["status"]

    if (data["description"] == "All Systems Operational"
            and data["indicator"]) == "none":
        return True

    return False
