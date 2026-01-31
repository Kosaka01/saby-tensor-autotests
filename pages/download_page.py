# pages/download_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage
import time
import os


class DownloadPage(BasePage):
    DOWNLOAD_BUTTON = (
        By.CSS_SELECTOR,
        'a[href*="saby-setup.exe"] span.controls-Button__text'  # или по id / name из твоего HTML
    )

    # Альтернатива по тексту кнопки
    DOWNLOAD_BUTTON_TEXT = (
        By.XPATH,
        '//span[contains(text(), "Скачать") and contains(@class, "controls-Button__text")]'
    )

    FILE_NAME = "saby-setup.exe"

    def open_download_page(self):
        self.open("https://saby.ru/download")

    def click_download_plugin(self):
        # Прокрутить к кнопке (на всякий случай)
        btn = self.scroll_to_element(self.DOWNLOAD_BUTTON)
        print("Кнопка 'Скачать' найдена → кликаем")
        self.click(self.DOWNLOAD_BUTTON)

    def wait_for_file_download(self, timeout=60):
        """Ждём появления файла в папке теста"""
        download_dir = os.path.abspath("tests")
        file_path = os.path.join(download_dir, self.FILE_NAME)

        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"Файл {self.FILE_NAME} скачан! Размер: {file_size / (1024*1024):.2f} МБ")
                print("Задание №5: Не получится сравнить размер скачанного файла в мегабайтах, на сайте не указан размер")
                return True
            time.sleep(2)  # проверяем каждые 2 секунды

        raise TimeoutError(f"Файл {self.FILE_NAME} не появился за {timeout} секунд")