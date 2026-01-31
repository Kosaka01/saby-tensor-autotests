from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 12)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        el = self.find(locator)
        self.wait.until(EC.element_to_be_clickable(el))
        el.click()

    def get_text(self, locator):
        return self.find(locator).text.strip()

    def url_contains(self, substring: str) -> bool:
        return self.wait.until(lambda d: substring.lower() in d.current_url.lower())
    
    def scroll_to_element(self, locator):
        """Прокручиваем страницу до элемента"""
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element