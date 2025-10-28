import os
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from logger import logger


class BasePage:
    """Базовый класс для всех PageObject — инкапсулирует работу с WebDriver."""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    # ------------------------------------------------------------
    # 🔹 Навигация
    # ------------------------------------------------------------
    @allure.step("Открываем страницу: {url}")
    def open_url(self, url: str):
        logger.info(f"Открываем страницу: {url}")
        self.driver.get(url)

    @allure.step("Получаем текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Обновляем страницу")
    def refresh_page(self):
        self.driver.refresh()

    # ------------------------------------------------------------
    # 🔹 WebDriverWait wrapper
    # ------------------------------------------------------------
    def wait(self, timeout=None):
        timeout = timeout or self.timeout
        return WebDriverWait(self.driver, timeout)

    # ------------------------------------------------------------
    # 🔹 Поиск элементов
    # ------------------------------------------------------------
    @allure.step("Поиск элемента: {locator}")
    def find(self, locator):
        return self.wait().until(EC.presence_of_element_located(locator))

    @allure.step("Поиск всех элементов: {locator}")
    def find_all(self, locator):
        return self.wait().until(EC.presence_of_all_elements_located(locator))

    # ------------------------------------------------------------
    # 🔹 Действия
    # ------------------------------------------------------------
    @allure.step("Клик по элементу: {locator}")
    def click(self, locator):
        logger.debug(f"Кликаем по элементу: {locator}")
        element = self.wait().until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Ввод текста '{text}' в элемент: {locator}")
    def input_text(self, locator, text: str):
        logger.debug(f"Вводим текст '{text}' в элемент: {locator}")
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    @allure.step("Получаем текст из элемента: {locator}")
    def get_text(self, locator) -> str:
        return self.find(locator).text.strip()

    # ------------------------------------------------------------
    # 🔹 Ожидания
    # ------------------------------------------------------------
    @allure.step("Ожидание полной загрузки страницы")
    def wait_for_page_load(self, timeout=None):
        """Ждёт, пока document.readyState == 'complete'."""
        timeout = timeout or self.timeout
        try:
            self.wait(timeout).until(
                lambda driver: self.execute_js("return document.readyState") == "complete"
            )
            logger.info("Страница успешно загружена.")
        except TimeoutException:
            logger.warning("Загрузка страницы заняла слишком много времени.")
            self.take_screenshot("page_load_timeout")
            raise

    @allure.step("Ожидание видимости элемента: {locator}")
    def wait_for_element_visible(self, locator):
        logger.debug(f"Ждём видимости элемента: {locator}")
        return self.wait().until(EC.visibility_of_element_located(locator))

    @allure.step("Ожидание исчезновения элемента: {locator}")
    def wait_for_element_invisible(self, locator):
        logger.debug(f"Ждём исчезновения элемента: {locator}")
        return self.wait().until(EC.invisibility_of_element_located(locator))

    @allure.step("Ожидание пользовательского условия")
    def wait_for_condition(self, condition_fn, timeout=None):
        timeout = timeout or self.timeout
        try:
            self.wait(timeout).until(condition_fn)
        except TimeoutException:
            raise TimeoutException("Условие ожидания не выполнено за отведённое время.")

    # ------------------------------------------------------------
    # 🔹 JS и Storage
    # ------------------------------------------------------------
    @allure.step("Выполняем JS: {script}")
    def execute_js_script(self, script: str, *args):
        """Безопасное выполнение JS"""
        logger.debug(f"Выполняем JS: {script[:100]}...")
        return self.driver.execute_script(script, *args)

    def execute_js(self, script: str, *args):
        """Алиас для execute_js_script — для совместимости"""
        return self.execute_js_script(script, *args)

    @allure.step("Устанавливаем значение sessionStorage: {key} = {value}")
    def set_session_storage_item(self, key, value):
        self.execute_js(f"sessionStorage.setItem('{key}', '{value}');")

    @allure.step("Получаем значение из sessionStorage: {key}")
    def get_session_storage_item(self, key):
        return self.execute_js(f"return sessionStorage.getItem('{key}');")

    @allure.step("Очищаем sessionStorage")
    def clear_session_storage(self):
        self.execute_js("sessionStorage.clear();")

    @allure.step("Устанавливаем значение localStorage: {key} = {value}")
    def set_local_storage_item(self, key, value):
        self.execute_js(f"localStorage.setItem('{key}', '{value}');")

    @allure.step("Получаем значение из localStorage: {key}")
    def get_local_storage_item(self, key):
        return self.execute_js(f"return localStorage.getItem('{key}');")

    # ------------------------------------------------------------
    # 🔹 Вспомогательные методы
    # ------------------------------------------------------------
    @allure.step("Проверяем наличие элемента: {locator}")
    def is_element_present(self, locator) -> bool:
        try:
            self.find(locator)
            return True
        except TimeoutException:
            return False

    @allure.step("Прокрутка до элемента: {locator}")
    def scroll_to(self, locator):
        element = self.find(locator)
        self.execute_js("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    # ------------------------------------------------------------
    # 🔹 Скриншоты
    # ------------------------------------------------------------
    @allure.step("Сохранение скриншота: {name}")
    def take_screenshot(self, name: str):
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        filepath = os.path.join(screenshot_dir, f"{name}.png")
        try:
            self.driver.save_screenshot(filepath)
            allure.attach.file(filepath, name=name, attachment_type=allure.attachment_type.PNG)
            logger.info(f"Скриншот сохранён: {filepath}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении скриншота: {e}")
