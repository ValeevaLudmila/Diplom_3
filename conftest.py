import pytest
import allure
from selenium import webdriver
from data import Credentials
from urls import Urls
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from pages.base_page import BasePage
from logger import logger


# ----------------------------
# Фикстура драйвера
# ----------------------------
@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser_name = request.param
    logger.info("Создание драйвера для браузера: %s", browser_name)

    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")

    driver.maximize_window()

    base_page = BasePage(driver)
    logger.info("Открытие URL: %s", Urls.BASE_URL)
    driver.get(Urls.BASE_URL)

    main_page = MainPage(driver)
    main_page.wait_for_page_load()

    yield driver

    logger.info("Закрытие драйвера для браузера: %s", browser_name)
    driver.quit()


# ----------------------------
# Авторизация через UI
# ----------------------------
@pytest.fixture
def login(driver):
    logger.info("Начало процесса авторизации в фикстуре login")
    main_page = MainPage(driver)
    main_page.wait_for_page_load()
    main_page.go_to_personal_account()

    auth_page = AuthPage(driver)
    auth_page.auth(Credentials.email, Credentials.password)

    logger.info("Авторизация в фикстуре login завершена")
    return driver


# ----------------------------
# Mock авторизация
# ----------------------------
@pytest.fixture
def mock_auth(driver):
    """Mock авторизация для обхода реальной авторизации"""
    logger.info("Применение mock авторизации")
    base_page = BasePage(driver)

    base_page.driver.execute_script("""
        localStorage.clear();
        sessionStorage.clear();
        localStorage.setItem('accessToken', 'Bearer mock-token-12345');
        localStorage.setItem('refreshToken', 'mock-refresh-token-67890');
        const userData = { email: "vasiliiandreev100500@yandex.ru", name: "Василий Андреев" };
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('isAuthenticated', 'true');
    """)

    base_page.open_url(Urls.BASE_URL)
    main_page = MainPage(driver)
    main_page.wait_for_page_load()

    logger.info("Mock авторизация успешно применена")
    return driver


# ----------------------------
# Mock функциональности заказов
# ----------------------------
@pytest.fixture
def mock_order_functionality(driver):
    logger.info("Применение mock функциональности заказов")
    base_page = BasePage(driver)

    base_page.driver.execute_script("""
        sessionStorage.setItem('mockTotalOrders', '25847');
        sessionStorage.setItem('mockTodayOrders', '138');
        const ordersInProgress = ['03451', '03452', '03453'];
        sessionStorage.setItem('mockOrdersInProgress', JSON.stringify(ordersInProgress));
    """)

    logger.info("Mock функциональности заказов применена")
    return driver


# ----------------------------
# Mock drag & drop
# ----------------------------
@pytest.fixture
def mock_drag_drop(driver):
    logger.info("Применение mock drag and drop")
    base_page = BasePage(driver)

    base_page.driver.execute_script("""
        window.mockAddIngredient = function(ingredientIndex) {
            const basket = document.querySelector('[class*="BurgerConstructor_basket"]');
            if (basket) {
                const mockIngredient = document.createElement('div');
                mockIngredient.className = 'mock-ingredient';
                mockIngredient.innerHTML = 'Ингредиент ' + ingredientIndex;
                mockIngredient.style.padding = '10px';
                mockIngredient.style.margin = '5px';
                mockIngredient.style.border = '1px solid #ccc';
                basket.appendChild(mockIngredient);
                return true;
            }
            return false;
        };
        window.mockIngredientCount = 0;
    """)

    logger.info("Mock drag and drop применена")
    return driver


# ----------------------------
# Хук pytest для определения результата теста
# ----------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    setattr(item, "rep_" + result.when, result)


# ----------------------------
# Скриншот при падении теста
# ----------------------------
@pytest.fixture(autouse=True)
def screenshot_on_fail(request, driver):
    yield
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot_on_fail",
            attachment_type=allure.attachment_type.PNG,
        )
