from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ContactsPage(BasePage):

# ------------------------- Первый сценарий -------------------------
    CONTACTS_LINK_MAIN = (By.XPATH, "//a[contains(text(), 'Контакты')]") 

    TENSOR_BANNER_LINK = (By.CSS_SELECTOR, 'a.sbisru-Contacts__logo-tensor[href*="tensor.ru"]') 

    SILA_V_LUDYAKH_BLOCK = (
        By.XPATH,
        '//p[contains(@class, "tensor_ru-Index__card-title") and contains(text(), "Сила в людях")]'
    ) 

    PODROBNEE_LINK = (
        By.CSS_SELECTOR,
        'a.tensor_ru-link.tensor_ru-Index__link[href="/about"]'
    ) 

    ABOUT_URL_PART = "/about" 

    RABOTAEM_TITLE = (
        By.XPATH,
        '//h2[contains(text(), "Работаем") or contains(@class, "tensor_ru-About__block-title")]'
    ) 

    WORK_IMAGES_BY_ALT = (
        By.XPATH,
        '//img[contains(@alt, "Разрабатываем систему Saby") or '
        'contains(@alt, "Продвигаем сервисы") or '
        'contains(@alt, "Создаем инфраструктуру") or '
        'contains(@alt, "Сопровождаем клиентов")]'
    ) 

    def open_main_and_go_to_contacts(self): 
        self.open("https://saby.ru/")
        self.click(self.CONTACTS_LINK_MAIN)
        self.url_contains("/contacts")

    def click_tensor_banner(self): 
        original_window = self.driver.current_window_handle
        clicked = False

        locator = self.TENSOR_BANNER_LINK
        link = self.find(locator)
        href = link.get_attribute("href")
        text_or_alt = link.get_attribute("title") or link.text.strip() or link.find_element(By.TAG_NAME, "img").get_attribute("alt") if 'img' in link.get_attribute("innerHTML") else ""
        print(f"Нашли элемент: '{text_or_alt}' → href: {href}")

        target = link.get_attribute("target")
        if target == "_blank":
            print("→ Откроется в новой вкладке")

        self.click(locator)
        clicked = True

        # Ждём новую вкладку, если target="_blank"
        try:
            self.wait.until(lambda d: len(d.window_handles) > 1)
            for handle in self.driver.window_handles:
                if handle != original_window:
                    self.driver.switch_to.window(handle)
                    break
            print("Переключились на новую вкладку")
        except TimeoutException:
            print("Новая вкладка не появилась → продолжаем в текущей")

        # Ждём загрузки tensor.ru
        self.url_contains("tensor.ru")
            
        assert clicked, "Не удалось найти и кликнуть баннер/ссылку на tensor.ru"
    
    def click_podrobnee_in_sila_block(self):
        original_window = self.driver.current_window_handle
        clicked = False
        locator = self.PODROBNEE_LINK

        link = self.find(locator)
        href = link.get_attribute("href")
        text = link.text.strip()
        print(f"Нашли ссылку 'Подробнее': текст='{text}', href='{href}'")

        self.click(locator)
        clicked = True

        # Проверяем, новая ли вкладка (маловероятно, но на всякий случай)
        try:
            self.wait.until(lambda d: len(d.window_handles) > 1, timeout=4)
            for handle in self.driver.window_handles:
                if handle != original_window:
                    self.driver.switch_to.window(handle)
                    break
            print("Переключились на новую вкладку (неожиданно)")
        except:
            print("Остаёмся в текущей вкладке")

        # Ждём смены URL
        self.wait.until(
            lambda d: self.ABOUT_URL_PART in d.current_url,
            message="Не произошёл переход на /about"
            )

        assert clicked, "Не удалось найти и кликнуть ссылку 'Подробнее' в блоке 'Сила в людях'"

    def check_all_work_images_same_size(self):
        """Проверяем, что все изображения в разделе 'Работаем' имеют одинаковые width и height"""
        images = []
        locator = self.WORK_IMAGES_BY_ALT
        
        try:
            candidates = self.driver.find_elements(*locator)
            if len(candidates) == 4:
                images = candidates
                print(f"Успешно найден локатор с 4 изображениями: {locator}")
            elif len(candidates) > 0:
                print(f"Найдено {len(candidates)} изображений по {locator} — не 4, пробуем следующий")
        except Exception as e:
            print(f"Локатор {locator} вызвал ошибку: {str(e)[:100]}...")
        
        if not images:
            # Финальная попытка — самый общий поиск
            images = self.driver.find_elements(By.XPATH, '//img[@width="270"][@height="192"]')
            if len(images) == 4:
                print("Нашли 4 изображения по атрибутам width=270 height=192")
            else:
                current_section_html = self.driver.find_element(By.XPATH, '//h2[contains(., "Работаем")]/..').get_attribute('outerHTML')
                print("HTML раздела 'Работаем' для отладки:\n" + current_section_html[:800] + "...")
                raise AssertionError(f"Не удалось найти ровно 4 изображения в разделе 'Работаем'. Найдено: {len(images)}")

        sizes = []
        for idx, img in enumerate(images, 1):
            width = img.get_attribute("width")
            height = img.get_attribute("height")
            alt = img.get_attribute("alt") or "(без alt)"
            
            print(f"Изображение {idx}: alt='{alt[:40]}...', width={width}, height={height}")
            
            if not width or not height:
                raise AssertionError(f"Изображение {idx} без атрибутов width/height")
            
            sizes.append((width, height))

        first_size = sizes[0]
        for size in sizes[1:]:
            assert size == first_size, \
                f"Размеры отличаются: {first_size} ≠ {size}"

        print(f"Все 4 изображения имеют размер {first_size[0]} × {first_size[1]} — проверка пройдена")



    def should_be_on_tensor_page(self):
        current_url = self.driver.current_url
        print(f"Текущий URL: {current_url}")
        assert "tensor.ru" in current_url.lower(), f"Ожидался tensor.ru, получили: {current_url}"

    def should_see_sila_v_ludyakh_block(self):
        text = self.get_text(self.SILA_V_LUDYAKH_BLOCK)
        print(f"Найден текст блока: '{text}'")
        assert "Сила в людях" in text, f"Ожидали 'Сила в людях', нашли: '{text}'"

    def should_be_on_tensor_about_page(self):
        current_url = self.driver.current_url
        print(f"Текущий URL после клика 'Подробнее': {current_url}")
        assert "/about" in current_url and "tensor.ru" in current_url, \
            f"Ожидался переход на https://tensor.ru/about, получили: {current_url}"
    
    def should_see_rabotaem_section(self):
        """Проверяем наличие раздела 'Работаем'"""
        element = self.find(self.RABOTAEM_TITLE)
        text = element.text.strip()
        print(f"Найден заголовок раздела: '{text}'")
        assert "Работаем" in text, f"Раздел 'Работаем' не найден, заголовок: '{text}'"


# ------------------------- Второй сценарий -------------------------

    CURRENT_REGION_XPATH = (
        By.XPATH,
        '//*[@id="container"]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]'
        '//span[contains(@class, "sbis_ru-Region-Chooser__text")]'
    )

    # Панель/список регионов (popup) — ждём его появления после клика
    REGION_PANEL = (
        By.ID,
        "popup"  # или By.CSS_SELECTOR, ".sbis_ru-Region-Panel"
    )

    KAMCHATKA_BY_POSITION = (
        By.XPATH,
        '//*[@id="popup"]/div[2]/div/div/div/div/div[2]/div/ul/li[43]'
    )


    def verify_region_determined(self):
                
        region_element = self.find(self.CURRENT_REGION_XPATH)
        region_name = region_element.text.strip()
        
        if region_name:
            print(f"Регион определён: {region_name}")
            return region_name
        else:
            raise Exception("Элемент по xpath найден, но текст пустой")
                

    def verify_partners_list_exists(self):
        """Проверяет наличие блока со списком партнёров"""
        PARTNERS_BLOCK = (By.ID, "contacts_list")
        
        self.find(PARTNERS_BLOCK)
        print("Найден блок со списком партнёров")
        
    def click_to_open_region_chooser(self):
        self.click(self.CURRENT_REGION_XPATH)

        # Ждём появления панели регионов
        self.wait.until(EC.presence_of_element_located(self.REGION_PANEL),
                        "Панель выбора региона не появилась после клика")

        print("Панель выбора региона открыта")

    def select_kamchatsky_kray(self):
        old_url = self.driver.current_url
        print(f"URL до смены региона: {old_url}")
        
        old_title = self.driver.title
        print(f"Старый title: {old_title}")

        self.click(self.KAMCHATKA_BY_POSITION)

        # Ждём, пока панель закроется или регион обновится
        self.wait.until(
            lambda d: "камчат" in d.find_element(*self.CURRENT_REGION_XPATH).text.lower(),
            message="Регион не сменился на Камчатский край за отведённое время"
        )
        self.wait.until(
            lambda driver: driver.current_url != old_url,
            message="URL страницы не изменился после выбора региона"
        )

        new_url = self.driver.current_url
        if new_url == "https://saby.ru/contacts/41-kamchatskij-kraj?tab=clients":
            print(f"URL поменялся на Камчатский: {new_url}")
        new_region = self.find(self.CURRENT_REGION_XPATH).text.strip()
        print(f"Новый регион после выбора: {new_region}")



        CITY_ID_2_LOCATOR = (By.XPATH, '//*[@id="city-id-2"]')

        city_elem = self.driver.find_element(*CITY_ID_2_LOCATOR)
        city_text = city_elem.text.strip()
        print(f"Город из списка партнеров: '{city_text}'")

        new_title = self.driver.title
        print(f"Новый title: {new_title}")
    
