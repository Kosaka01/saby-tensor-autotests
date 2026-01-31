import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os


@pytest.fixture(scope="function")
def browser():
    options = Options()
    # options.add_argument("--headless=new")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    download_dir = download_dir = os.path.abspath("tests")
    print(f"Папка для скачивания: {download_dir}")
    prefs = {
        "download.default_directory": download_dir,             # куда сохранять
        "download.prompt_for_download": False,                  # без диалога "Сохранить как"
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(10)
    yield driver
    driver.quit()