import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup


def check_status() -> bool:
    response = requests.get("https://status.procore.com/api/v2/status.json")
    data = response.json()["status"]

    if (data["description"] == "All Systems Operational" and 
        data["indicator"]) == "none":
        return True

    return False


def scrape_page() -> dict[dict, str]:
    r = requests.get('https://status.procore.com/')
    soup = BeautifulSoup(r.text, 'html.parser')
    service_groups = {}
    statuses = []

    all_group_divs = soup.find_all("div", class_='component-container border-color is-group')
    for group_div in all_group_divs:
        group_name = (group_div.span.text.strip())
        services = {}
        service_divs = group_div.find_all("div", class_="child-components-container")[0]

        for div in service_divs.find_all("span", class_="name"):
            service = div.text.strip()
            status = div.find_next("span").text.strip()
            if status == "?":
                status = div.find_next("span").find_next("span").text.strip()
            services[service] = status
            statuses.append(status)

        service_groups[group_name] = services

    return service_groups


if __name__ == "__main__":
    operational = check_status()
    if operational:
        print("All systems operational")
    else:
        service_groups = scrape_page()
        pprint(service_groups)
