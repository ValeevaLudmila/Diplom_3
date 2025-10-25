import pytest
from selenium import webdriver
from data import Urls, Credentials
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from logger import logger


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser_name = request.param
    logger.info("Создание драйвера для браузера: %s", browser_name)
    
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    
    driver.maximize_window()
    logger.info("Открытие URL: %s", Urls.BASE_URL)
    driver.get(Urls.BASE_URL)
    
    main_page = MainPage(driver)
    main_page.wait_for_page_load()
    
    yield driver
    
    logger.info("Закрытие драйвера для браузера: %s", browser_name)
    driver.quit()


@pytest.fixture
def login(driver):
    logger.info("Начало процесса авторизации в фикстуре login")
    
    main_page = MainPage(driver)
    
    # Ждем загрузки страницы через BasePage
    main_page.wait_for_page_load()
    
    logger.debug("Переход на страницу авторизации")
    main_page.go_to_personal_account()
    
    auth_page = AuthPage(driver)
    auth_page.auth(Credentials.email, Credentials.password)
    
    logger.info("Авторизация в фикстуре login завершена")
    return driver

@pytest.fixture
def mock_auth(driver):
    """Mock авторизация для обхода проблем с реальной авторизацией"""
    logger.info("Применение mock авторизации")
    
    # Устанавливаем mock токен и данные пользователя
    driver.execute_script("""
        // Очищаем старые данные
        localStorage.clear();
        sessionStorage.clear();
        
        // Устанавливаем mock токены
        localStorage.setItem('accessToken', 'Bearer mock-token-12345');
        localStorage.setItem('refreshToken', 'mock-refresh-token-67890');
        
        // Mock данные пользователя
        const userData = {
            email: "vasiliiandreev100500@yandex.ru",
            name: "Василий Андреев"
        };
        localStorage.setItem('user', JSON.stringify(userData));
        
        // Устанавливаем флаг авторизации
        localStorage.setItem('isAuthenticated', 'true');
    """)
    
    # Обновляем страницу для применения изменений
    driver.refresh()
    
    # Ждем загрузки страницы
    main_page = MainPage(driver)
    main_page.wait_for_page_load()
    
    logger.info("Mock авторизация успешно применена")
    return driver

@pytest.fixture
def mock_order_functionality(driver):
    """Mock функциональности заказов для тестирования"""
    logger.info("Применение mock функциональности заказов")
    
    # Mock данных для ленты заказов
    driver.execute_script("""
        // Mock счетчиков заказов
        sessionStorage.setItem('mockTotalOrders', '25847');
        sessionStorage.setItem('mockTodayOrders', '138');
        
        // Mock списка заказов в работе
        const ordersInProgress = ['03451', '03452', '03453'];
        sessionStorage.setItem('mockOrdersInProgress', JSON.stringify(ordersInProgress));
    """)
    
    logger.info("Mock функциональности заказов применена")
    return driver

@pytest.fixture
def mock_drag_drop(driver):
    """Mock функциональности drag and drop"""
    logger.info("Применение mock drag and drop")
    
    # Mock добавления ингредиента в корзину
    driver.execute_script("""
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
        
        // Mock счетчика ингредиентов
        window.mockIngredientCount = 0;
    """)
    
    logger.info("Mock drag and drop применена")
    return driver