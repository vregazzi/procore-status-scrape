import logging

from procore import check_status as procore_check_status
from procore import scrape_page as procore_scrape_page

if __name__ == "__main__":
    fmt = '%(levelname)7s | %(asctime)s | %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    operational = procore_check_status()

    if operational:
        logging.info("All systems operational")
    else:
        logging.warning("Some systems are down")
        logging.info("Scraping page for more information")
        service_groups = procore_scrape_page()
