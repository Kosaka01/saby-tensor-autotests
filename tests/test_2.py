# import pytest
from pages.contacts_page import ContactsPage


def test_contacts_region_and_partners(browser):
    page = ContactsPage(browser)

    # 1. Переходим в контакты
    page.open_main_and_go_to_contacts()  

    # 2. Проверяем регион 
    page.verify_region_determined()

    # 3. Проверяем наличие списка партнёров
    page.verify_partners_list_exists()

    page.click_to_open_region_chooser()

    page.select_kamchatsky_kray()

    
