from selenium.webdriver.common.by import By

class AuthLocators:
    # ===== ФОРМА АВТОРИЗАЦИИ =====
    FIELD_EMAIL_LOGIN = (By.XPATH, "//input[@name='name']")
    FIELD_PASSWORD_LOGIN = (By.XPATH, "//input[@type='password']")
    BUTTON_ENTRANCE = (By.XPATH, '//*[@id="root"]/div/main/div/form/button')
    PERSONAL_ACCOUNT = (By.XPATH, '//a[p[text()="Личный Кабинет"]]')
    LOGIN_BUTTON_MAIN = (By.XPATH, "//button[text()='Войти в аккаунт']")