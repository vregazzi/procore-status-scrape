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


def get_info() -> None:
    """
    Checks the status of Procore services via API. If all systems are not
    operational, it will scrape the Procore status page. All data will be
    logged and uploaded to Azure Blob Storage.
    """
    _ensure_temp_dir()
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    logging.basicConfig(format='%(asctime)s | %(levelname)7s | %(message)s',
                        level=logging.INFO, filename=f"temp/{time}.log")

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


def _ensure_temp_dir() -> None:
    """Creates temp directory if it doesn't exist."""
    if not os.path.exists("temp"):
        os.makedirs("temp")


def _upload(time: str) -> None:
    """Moves files to Azure Blob Storage and removes temp directory."""
    logging.debug("Checking for connection string and container name")
    if CONNECTION_STRING == "" or CONTAINER_NAME == "":
        logging.error("Connection string or container name not found")
        return
    assert isinstance(CONNECTION_STRING, str)
    assert isinstance(CONTAINER_NAME, str)

    # zip directory and delete it
    logging.info("Zipping files and removing temp directory")
    shutil.make_archive(f'{time}_files', 'zip', "temp")
    shutil.rmtree("temp")

    logging.info("Uploading files to Azure Blob Storage")
    blob_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=f'{time}_files.zip',
    )
    with open(f'{time}_files.zip', "rb") as data:
        blob_client.upload_blob(data)


if __name__ == "__main__":
    get_info()
