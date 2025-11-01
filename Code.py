import os
import requests
import logging
from time import sleep
from urllib.parse import urlparse

# ------------------ CONFIG ------------------
LOG_FILE = "image_downloader.log"
DOWNLOAD_DIR = "downloads"
RETRY_LIMIT = 3
TIMEOUT = 10  # seconds
# --------------------------------------------

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
)

def create_download_dir():
    """Ensure the download folder exists."""
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        logging.info(f"Created download directory: {DOWNLOAD_DIR}")

def get_image_name_from_url(url):
    """Extract a clean image name from the URL."""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    return filename or "downloaded_image.jpg"

def download_image(url):
    """Download an image with advanced error handling and retry mechanism."""
    create_download_dir()
    filename = get_image_name_from_url(url)
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    attempt = 0
    while attempt < RETRY_LIMIT:
        try:
            logging.info(f"Attempt {attempt + 1}: Downloading {url}")
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()  # Raise HTTPError for bad responses

            # Check if content is image
            if "image" not in response.headers.get("Content-Type", ""):
                raise ValueError("URL does not point to an image")

            # Save image
            with open(file_path, "wb") as f:
                f.write(response.content)
            logging.info(f"Successfully downloaded image: {file_path}")
            print(f"✅ Download complete: {file_path}")
            return file_path

        except requests.exceptions.RequestException as req_err:
            logging.error(f"Network error: {req_err}")
            print(f"⚠️ Network error: {req_err}, retrying...")
            attempt += 1
            sleep(2)  # Wait before retry

        except ValueError as val_err:
            logging.error(f"Invalid content: {val_err}")
            print(f"❌ Error: {val_err}")
            return None

        except Exception as e:
            logging.critical(f"Unexpected error: {e}")
            print(f"🚨 Unexpected error: {e}")
            return None

    print("❌ Failed to download image after multiple attempts.")
    return None


if __name__ == "__main__":
    # Example usage:
    image_url = input("Enter Google Image URL: ").strip()
    download_image(image_url)
