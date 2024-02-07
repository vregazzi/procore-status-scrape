import requests
from bs4 import BeautifulSoup


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