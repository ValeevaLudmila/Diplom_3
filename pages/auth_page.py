import allure
from selenium.common.exceptions import TimeoutException
from locators.auth_locators import AuthLocators
from pages.base_page import BasePage
from logger import logger


class AuthPage(BasePage):
    """Page Object для страницы авторизации."""

    @allure.step("Авторизация пользователя")
    def auth(self, email, password):
        """Выполнить авторизацию пользователя."""
        logger.info("Начало процесса авторизации для пользователя: %s", email)
    
        logger.debug("Ввод email в поле логина")
        self.send_keys_to_input(AuthLocators.FIELD_EMAIL_LOGIN, email)
    
        logger.debug("Ввод пароля в поле пароля")
        self.send_keys_to_input(AuthLocators.FIELD_PASSWORD_LOGIN, password)
    
        logger.info("Нажатие кнопки 'Войти' для завершения авторизации")
        self.click_on_element(AuthLocators.BUTTON_ENTRANCE)
    
        logger.debug("Ожидание завершения авторизации")
        self._wait_for_auth_completion()

        from data import Urls
        current_url = self.get_current_url()
        if "login" in current_url:
            logger.warning("После авторизации остались на странице логина. Переходим на главную...")
            self.driver.get(Urls.BASE_URL)
            self.wait_for_condition(
                lambda driver: driver.execute_script("return document.readyState") == "complete",
                timeout=10,
                description="полная загрузка страницы"
            )
    
        logger.debug("Обработка возможного OVERLAY после авторизации")
        self.close_overlay_if_present()
        self.wait_for_overlay_to_disappear(5)
    
        logger.info("Процесс авторизации завершен")
        
    @allure.step("Ожидание завершения процесса авторизации.")
    def _wait_for_auth_completion(self):
        logger.debug("Ожидание завершения авторизации")
        try:
            self.wait_for_condition(
                lambda driver: (
                    self._is_on_main_page() or 
                    self._is_auth_error_present() or
                    self._is_still_on_login_page()
                ),
                timeout=10,
                description="ожидание завершения авторизации"
            )
            
            if self._is_on_main_page():
                logger.debug("Авторизация прошла успешно")
            elif self._is_auth_error_present():
                logger.error("Ошибка авторизации")
                self.take_screenshot("auth_error")
                raise Exception("Ошибка авторизации")
            else:
                logger.warning("Авторизация не завершилась")
                
        except TimeoutException:
            logger.error("Таймаут ожидания завершения авторизации")
            self.take_screenshot("auth_timeout")
            raise

    @allure.step("Проверить, находимся ли на главной странице.")
    def _is_on_main_page(self):
        from data import Urls
        return self.is_url_contains(Urls.BASE_URL)

    @allure.step("Проверить наличие сообщения об ошибке авторизации.")
    def _is_auth_error_present(self):
        error_selectors = [
            "//p[contains(@class, 'error')]",
            "//div[contains(@class, 'error')]",
            "//p[contains(text(), 'error')]",
            "//p[contains(text(), 'ошибка')]"
        ]
        
        for selector in error_selectors:
            try:
                self.find_element_by_xpath(selector)
                return True
            except:
                continue
        return False
    
    @allure.step("Проверить, остались ли на странице логина.")
    def _is_still_on_login_page(self):
        return self.is_url_contains("login")

    @allure.step("Найти элемент по XPath.")
    def find_element_by_xpath(self, xpath):
        from selenium.webdriver.common.by import By
        return self.driver.find_element(By.XPATH, xpath)