from selenium.webdriver.common.by import By

class MainPageLocators:
    # ===== ОСНОВНЫЕ ЭЛЕМЕНТЫ =====
    OVERLAY = (By.XPATH, ".//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]/parent::div")
    PERSONAL_ACCOUNT = (By.XPATH, '//a[p[text()="Личный Кабинет"]]')
    BUTTON_CHECKOUT = (By.XPATH, '//*[@id="root"]/div/main/section[2]/div/button')
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[contains(text(),'Конструктор')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[contains(text(),'Лента Заказов')]")
    ORDER_BUTTON = (By.XPATH, '//*[@id="root"]/div/main/section[2]/div/button')
    
    # ===== КОНСТРУКТОР =====
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[contains(text(),'Конструктор')]")
    BREAD_SECTION = (By.XPATH, "//span[text()='Булки']/parent::div")
    SAUCES_SECTION = (By.XPATH, "//span[text()='Соусы']/parent::div")
    TOPPINGS_SECTION = (By.XPATH, "//span[text()='Начинки']/parent::div")
    ACTIVE_SECTION = (By.XPATH, "//div[contains(@class, 'tab_tab_type_current')]")
    INSCRIPTION_BREAD = (By.XPATH, "//h2[text()='Булки']")
    
    # ===== ИНГРЕДИЕНТЫ =====
    # Исправленные локаторы для ингредиентов
    INGREDIENT_CARD = (By.XPATH, "(//div[contains(@class, 'BurgerIngredient_ingredient')])[1]")
    INGREDIENT_NAME = (By.XPATH, '//*[@id="root"]/div/main/section[1]/div[2]/ul[1]/a[1]/p')
    INGREDIENT_COUNTER = (By.XPATH, "(//div[contains(@class, 'counter_counter__')])[1]")
    CONSTRUCTOR_AREA = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket')]")
    
    # ДОБАВИТЬ СЮДА АЛЬТЕРНАТИВНЫЕ ЛОКАТОРЫ ДЛЯ ИНГРЕДИЕНТОВ:
    INGREDIENT_BUNS = (By.XPATH, "(//section[.//h2[text()='Булки']]//div[contains(@class, 'BurgerIngredient_ingredient')])[1]")
    INGREDIENT_SAUCES = (By.XPATH, "(//section[.//h2[text()='Соусы']]//div[contains(@class, 'BurgerIngredient_ingredient')])[1]")
    INGREDIENT_TOPPINGS = (By.XPATH, "(//section[.//h2[text()='Начинки']]//div[contains(@class, 'BurgerIngredient_ingredient')])[1]")
    
    # ===== МОДАЛЬНЫЕ ОКНА =====
    # Исправленные локаторы для модальных окон
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    INGREDIENT_MODAL_NAME = (By.XPATH, '//*[@id="root"]/div/section[1]/div[1]/div/p')
    ORDER_MODAL = (By.XPATH, "//*[contains(@class, 'Modal_modal__contentBox')]")
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//h2")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    
    # ===== ЛЕНТА ЗАКАЗОВ =====
    TOTAL_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за все время:')]/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня:')]/following-sibling::p")
    IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList')]")
    ORDER_NUMBER_IN_PROGRESS = (By.XPATH, "(//li[contains(@class, 'OrderFeed_order__number')])[1]")