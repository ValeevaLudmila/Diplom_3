import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seletools.actions import drag_and_drop
from data import global_timeout
from logger import logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        logger.debug("Инициализирован BasePage с драйвером")

    @allure.step("Подождать видимости элемента")
    def wait_for_element(self, locator, timeout=global_timeout):
        logger.debug("Ожидание видимости элемента: %s", locator)
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        logger.debug("Элемент стал видимым: %s", locator)
        return element

    @allure.step("Подождать кликабельности элемента")
    def wait_for_element_clickable(self, locator, timeout=global_timeout):
        logger.debug("Ожидание кликабельности элемента: %s", locator)
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        logger.debug("Элемент стал кликабельным: %s", locator)
        return element

    @allure.step("Скролл до элемента")
    def scroll_to_element(self, locator, timeout=global_timeout):
        logger.debug("Скролл до элемента: %s", locator)
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        logger.debug("Скролл выполнен до элемента: %s", locator)

    @allure.step("Кликнуть на элемент")
    def click_on_element(self, locator):
        logger.info("Клик на элемент: %s", locator)
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.debug("Клик выполнен на элемент: %s", locator)

    @allure.step("Ввести текст в поле ввода")
    def send_keys_to_input(self, locator, keys, timeout=global_timeout):
        logger.info("Ввод текста в элемент %s: %s", locator, keys)
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(keys)
        logger.debug("Текст введен в элемент: %s", locator)

    @allure.step("Получить текст элемента")
    def get_text_on_element(self, locator, timeout=global_timeout):
        logger.debug("Получение текста из элемента: %s", locator)
        element = self.wait_for_element(locator, timeout)
        text = element.text
        logger.debug("Получен текст из элемента: %s", locator)
        return text

    @allure.step("Подождать пока элемент не станет невидимым")
    def wait_for_element_hide(self, locator, timeout=global_timeout):
        logger.debug("Ожидание скрытия элемента: %s", locator)
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
        logger.debug("Элемент скрыт: %s", locator)

    @allure.step("Перетащить элемент в корзину")
    def drag_and_drop_element(self, source_locator, target_locator):
        logger.info("Перетаскивание элемента %s в %s", source_locator, target_locator)
        source = self.wait_for_element(source_locator)
        target = self.wait_for_element(target_locator)
        drag_and_drop(self.driver, source, target)
        logger.debug("Перетаскивание выполнено: %s -> %s", source_locator, target_locator)

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        url = self.driver.current_url
        logger.debug("Текущий URL: %s", url)
        return url
    
    @allure.step("Сделать скриншот")
    def take_screenshot(self, name="screenshot"):
        from datetime import datetime
        filename = f"logs/{name}_{datetime.now().strftime('%H%M%S')}.png"
        self.driver.save_screenshot(filename)
        logger.info("Скриншот сохранен: %s", filename)

    @allure.step("Закрыть OVERLAY если присутствует")
    def close_overlay_if_present(self):
        from locators.main_page_locators import MainPageLocators
        try:
            overlay = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(MainPageLocators.OVERLAY)
            )
            close_btn = overlay.find_element(By.XPATH, ".//button")
            close_btn.click()
            logger.info("OVERLAY закрыт")
            return True
        except:
            return False

    @allure.step("Ожидать исчезновения OVERLAY")
    def wait_for_overlay_to_disappear(self, timeout=5):
        """Ожидает исчезновения модального окна"""
        from locators.main_page_locators import MainPageLocators
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(MainPageLocators.OVERLAY)
            )
            logger.debug("OVERLAY исчез")
            return True
        except:
            logger.debug("OVERLAY не исчез за отведенное время")
            return False

    @allure.step("Безопасный клик с обработкой OVERLAY")
    def safe_click_with_overlay(self, locator):
        self.close_overlay_if_present()
        self.wait_for_overlay_to_disappear(3)
        self.click_on_element(locator)

    @allure.step("Ожидать выполнения условия")
    def wait_for_condition(self, condition, timeout=global_timeout, description=""):
        """Общий метод для ожидания кастомных условий."""
        logger.debug("Ожидание условия: %s", description)
        return WebDriverWait(self.driver, timeout).until(condition)

    @allure.step("Проверить URL")
    def is_url_contains(self, text):
        return text in self.get_current_url()
    
    @allure.step("Проверить наличие элемента")
    def is_element_present(self, locator, timeout=5):
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False
        
    @allure.step("Закрыть все возможные OVERLAY")
    def close_all_overlays(self):
        """Закрывает все возможные overlay и модальные окна."""
        logger.debug("Поиск и закрытие всех OVERLAY")
    
        overlay_selectors = [
            "//div[contains(@class, 'Modal_modal_overlay')]",
            "//div[contains(@class, 'overlay')]",
            "//div[contains(@class, 'modal') and contains(@class, 'open')]", 
        ]
    
        closed_count = 0
        for selector in overlay_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed():
                        close_buttons = element.find_elements(By.XPATH, 
                            ".//button[contains(@class, 'close')] | " +
                            ".//button[contains(text(), 'Закрыть')] | " +
                            ".//*[contains(@class, 'close')]"
                        )
                    
                        for btn in close_buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                btn.click()
                                logger.info("Закрыт OVERLAY: %s", selector)
                                closed_count += 1
                                break
            except Exception as e:
                logger.debug("Ошибка при закрытии OVERLAY %s: %s", selector, e)
    
        logger.info("Закрыто OVERLAY: %s", closed_count)
        return closed_count