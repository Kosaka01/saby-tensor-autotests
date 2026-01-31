# import pytest
from pages.main_page import MainPage
from pages.download_page import DownloadPage

def test_go_to_download_local_versions(browser):
    page = MainPage(browser)
    
    # 1. Открываем главную страницу
    page.open_main()
    
    # 2. Прокручиваем в футер и кликаем по "Скачать локальные версии"
    page.scroll_to_footer_and_click_download()
    
    # 3. Проверяем, что мы на нужной странице
    page.should_be_on_download_page()

    download_page = DownloadPage(browser)
    download_page.click_download_plugin()
    download_page.wait_for_file_download(timeout=90)