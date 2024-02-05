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


def scrape_page():
    r = requests.get('https://status.procore.com/')
    soup = BeautifulSoup(r.text, 'html.parser')
    service_groups = []

    service_group_div = soup.find_all("div", class_='component-container border-color is-group')
    for thing in service_group_div:
        services = []
        top = thing.span.text.strip()
        service_div = thing.find_all("div", class_="component-inner-container status-green")
        print(len(service_div))
        for l in service_div:
            new_thing = l.span.text.strip()
            services.append(new_thing)

        services.remove(services[0])
        service_groups.append({top: services})

    pprint(service_groups)


if __name__ == "__main__":
    # operational = check_status()
    # if not operational:
    scrape_page()
