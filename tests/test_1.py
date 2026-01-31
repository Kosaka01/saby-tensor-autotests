# import pytest
from pages.contacts_page import ContactsPage


def test_saby_contacts_to_tensor_full_scenario(browser):
    page = ContactsPage(browser)

    # 1. Переход на контакты
    page.open_main_and_go_to_contacts()

    # 2. Клик по баннеру Тензор
    page.click_tensor_banner()

    # 3. Проверка tensor.ru
    page.should_be_on_tensor_page()

    # 4. Блок "Сила в людях"
    page.should_see_sila_v_ludyakh_block()

    # 5. Клик "Подробнее" → /about
    page.click_podrobnee_in_sila_block()
    page.should_be_on_tensor_about_page()

    # 6. Раздел "Работаем" + проверка одинаковых размеров изображений
    page.should_see_rabotaem_section()
    page.check_all_work_images_same_size()