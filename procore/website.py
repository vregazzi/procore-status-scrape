import requests
from bs4 import BeautifulSoup


def scrape_page() -> str:
    """Scrape the Procore status page and return all HTML as a string."""
    r = requests.get('https://status.procore.com/')
    return r.text


def process_scrape() -> dict[dict, str]:
    """
    Process the scraped page and return a dictionary of service groups and
    their statuses as a dictionary.
    """
    page = scrape_page()
    soup = BeautifulSoup(page, 'html.parser')
    service_groups = {}
    statuses = []

    all_group_divs = soup.find_all(
        "div",
        class_='component-container border-color is-group'
    )

    for group_div in all_group_divs:
        group_name = (group_div.span.text.strip())
        services = {}
        service_divs = group_div.find_all(
            "div",
            class_="child-components-container"
        )[0]

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
    from pprint import pprint
    pprint(process_scrape())
