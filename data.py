import os

class Credentials:
    email = 'vasiliiandreev100500@yandex.ru'
    password = '123456'

class Urls:
    BASE_URL = "https://stellarburgers.education-services.ru"
    LOGIN_URL = f"{BASE_URL}/login"
    FEED_URL = f"{BASE_URL}/feed"
    PROFILE_URL = f"{BASE_URL}/account/profile"

global_timeout = 15