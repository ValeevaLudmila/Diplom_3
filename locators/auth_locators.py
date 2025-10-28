from selenium.webdriver.common.by import By


class AuthLocators:
    # ===== ФОРМА АВТОРИЗАЦИИ =====
    FIELD_EMAIL_LOGIN = (By.XPATH, "//form//input[@name='name' or @type='text']")
    FIELD_PASSWORD_LOGIN = (By.XPATH, "//form//input[@type='password']")
    BUTTON_ENTRANCE = (By.XPATH, "//form//button[contains(@class, 'button') or text()='Войти']")
    PERSONAL_ACCOUNT = (By.XPATH, "//a[.//p[contains(text(), 'Личный Кабинет')]]")
    LOGIN_BUTTON_MAIN = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")
