from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):
    # Ссылка в футере "Скачать локальные версии"
    DOWNLOAD_LOCAL_VERSIONS_LINK = (
        By.XPATH,
        '//a[contains(@class, "sbisru-Footer__link") and contains(text(), "Скачать локальные версии")]'
    )

    DOWNLOAD_URL_PART = "/download"

    def open_main(self):
        self.open("https://saby.ru/")

    def scroll_to_footer_and_click_download(self):
        # Прокручиваем до футера и кликаем
        link = self.scroll_to_element(self.DOWNLOAD_LOCAL_VERSIONS_LINK)
        
        href = link.get_attribute("href")
        print(f"Найдена ссылка 'Скачать локальные версии' → href: {href}")
        
        self.click(self.DOWNLOAD_LOCAL_VERSIONS_LINK)

        # Ждём перехода
        self.wait.until(
            lambda d: self.DOWNLOAD_URL_PART in d.current_url.lower(),
            message="Не перешли на страницу скачивания (/download)"
        )

        print(f"Перешли на страницу: {self.driver.current_url}")

    def should_be_on_download_page(self):
        assert "/download" in self.driver.current_url.lower(), \
            f"Ожидался /download в URL, получили: {self.driver.current_url}"