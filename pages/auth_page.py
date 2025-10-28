import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from urls import Urls
from locators.auth_locators import AuthLocators
from pages.base_page import BasePage
from logger import logger


class AuthPage(BasePage):
    """Page Object для страницы авторизации."""

    @allure.step("Авторизация пользователя: {email}")
    def auth(self, email, password):
        """Выполнить авторизацию пользователя."""
        logger.info(f"Начало авторизации пользователя: {email}")

        self._enter_email(email)
        self._enter_password(password)
        self._click_login_button()
        self._wait_for_auth_completion()

        current_url = self.get_current_url()
        if "login" in current_url:
            logger.warning("После авторизации остались на странице логина. Переход на главную...")
            self.open_url(Urls.BASE_URL)
            self.wait_for_condition(
                lambda d: self.execute_js("return document.readyState") == "complete",
                timeout=10
            )

        logger.info("Авторизация завершена успешно")

    # ------------------------------------------------------------
    # Вспомогательные шаги
    # ------------------------------------------------------------
    @allure.step("Ввод email: {email}")
    def _enter_email(self, email):
        logger.debug("Ввод email")
        self.input_text(AuthLocators.FIELD_EMAIL_LOGIN, email)

    @allure.step("Ввод пароля")
    def _enter_password(self, password):
        logger.debug("Ввод пароля")
        self.input_text(AuthLocators.FIELD_PASSWORD_LOGIN, password)

    @allure.step("Нажатие кнопки 'Войти'")
    def _click_login_button(self):
        logger.debug("Нажатие кнопки 'Войти'")
        self.click(AuthLocators.BUTTON_ENTRANCE)

    @allure.step("Ожидание завершения авторизации")
    def _wait_for_auth_completion(self):
        try:
            self.wait_for_condition(
                lambda d: self._is_on_main_page() or self._is_auth_error_present(),
                timeout=10
            )
            if self._is_on_main_page():
                logger.info("Авторизация прошла успешно")
            elif self._is_auth_error_present():
                logger.error("Ошибка авторизации")
                self.take_screenshot("auth_error")
                raise Exception("Ошибка авторизации")
        except TimeoutException:
            logger.error("Таймаут ожидания авторизации")
            self.take_screenshot("auth_timeout")
            raise

    # ------------------------------------------------------------
    # Проверки состояния
    # ------------------------------------------------------------
    def _is_on_main_page(self):
        return Urls.BASE_URL in self.get_current_url()

    def _is_auth_error_present(self):
        selectors = [
            (By.XPATH, "//p[contains(@class, 'error')]"),
            (By.XPATH, "//div[contains(@class, 'error')]"),
            (By.XPATH, "//p[contains(text(), 'error')]"),
            (By.XPATH, "//p[contains(text(), 'ошибка')]")
        ]
        for locator in selectors:
            if self.is_element_present(locator):
                return True
        return False
