from selenium.webdriver.common.by import By


class MainPageLocators:
    # ===== ОСНОВНЫЕ ЭЛЕМЕНТЫ =====
    OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
    PERSONAL_ACCOUNT = (By.XPATH, "//a[.//p[contains(text(), 'Личный Кабинет')]]")
    BUTTON_CHECKOUT = (By.XPATH, "//main//button[contains(@class, 'button') and text()='Оформить заказ']")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//nav//p[contains(text(),'Конструктор')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//nav//p[contains(text(),'Лента Заказов')]")
    ORDER_BUTTON = (By.XPATH, "//main//button[contains(@class, 'button') and text()='Оформить заказ']")

    # ===== КОНСТРУКТОР =====
    BREAD_SECTION = (By.XPATH, "//section//span[text()='Булки']/ancestor::div[contains(@class,'tab_tab')]")
    SAUCES_SECTION = (By.XPATH, "//section//span[text()='Соусы']/ancestor::div[contains(@class,'tab_tab')]")
    TOPPINGS_SECTION = (By.XPATH, "//section//span[text()='Начинки']/ancestor::div[contains(@class,'tab_tab')]")
    ACTIVE_SECTION = (By.XPATH, "//div[contains(@class, 'tab_tab_type_current')]")
    INSCRIPTION_BREAD = (By.XPATH, "//h2[text()='Булки']")

    # ===== ИНГРЕДИЕНТЫ =====
    INGREDIENT_CARD = (By.XPATH, "//div[contains(@class, 'BurgerIngredient_ingredient')]")
    INGREDIENT_NAME = (By.XPATH, "//div[contains(@class, 'BurgerIngredient_ingredient')]//p")
    INGREDIENT_COUNTER = (By.XPATH, "//div[contains(@class, 'BurgerIngredient_ingredient')]//div[contains(@class, 'counter_counter')]")
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")

    # ===== МОДАЛЬНЫЕ ОКНА =====
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal')]")
    INGREDIENT_MODAL_NAME = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//p")
    ORDER_MODAL = (By.XPATH, "//section[contains(@class, 'Modal_modal__contentBox')]")
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_modal')]//h2")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")

    # ===== ЛЕНТА ЗАКАЗОВ =====
    TOTAL_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList')]")
    ORDER_NUMBER_IN_PROGRESS = (By.XPATH, "//li[contains(@class, 'OrderFeed_order__number')]")
