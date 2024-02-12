import datetime
import logging
import os
import shutil

from azure.storage.blob import BlobServiceClient
from decouple import config

from procore import check_status as procore_check_status
from procore import scrape_page as procore_scrape_page

CONNECTION_STRING = config("CONNECTION_STRING", "")
CONTAINER_NAME = config("CONTAINER_NAME", "")


def get_info():
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    fmt = '%(asctime)s | %(levelname)7s | %(message)s'
    if not os.path.exists("temp"):
        os.makedirs("temp")

    logging.basicConfig(
        level=logging.INFO, format=fmt, filename=f"temp/{time}.log")

    if procore_check_status():
        logging.info("All systems operational")
        _upload(time)
        return
    
    logging.warning("Some systems are down")
    logging.info("Scraping page for more information")

    # put scrape content in html file
    with open(f"temp/{time}.html", "w") as f:
        f.write(procore_scrape_page())

    _upload(time)


def _upload(time: str):
    if CONNECTION_STRING == "" or CONTAINER_NAME == "":
        logging.error("Connection string or container name not found")
        return
    assert isinstance(CONNECTION_STRING, str)
    assert isinstance(CONTAINER_NAME, str)

    # zip directory and delete it
    shutil.make_archive(f'{time}_files', 'zip', "temp")
    shutil.rmtree("temp")

    blob_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=f'{time}_files.zip',
    )
    with open(f'{time}_files.zip', "rb") as data:
        blob_client.upload_blob(data)


if __name__ == "__main__":
    get_info()
