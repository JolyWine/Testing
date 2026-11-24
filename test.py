import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(3)
    yield browser
    browser.quit()

def test_login(driver):
    with allure.step("Открываем сайт"):
        driver.get("https://www.demoblaze.com/")

    with allure.step("Открываем окно логина"):
        driver.find_element(By.ID, "login2").click()

    with allure.step("Вводим логин и пароль"):
        driver.find_element(By.ID, "loginusername").send_keys("admin")
        driver.find_element(By.ID, "loginpassword").send_keys("admin")
        driver.find_element(By.XPATH, "//button[text()='Log in']").click()
        time.sleep(2)

    with allure.step("Проверяем, что вошли"):
        text = driver.find_element(By.ID, "nameofuser").text
        assert "Welcome admin" in text
        driver.save_screenshot("screen.png")

        
def test_form(driver):
    with allure.step("Открываем сайт"):
        driver.get("https://www.demoblaze.com/")

    with allure.step("Открываем форму Contact"):
        driver.find_element(By.LINK_TEXT, "Contact").click()

    with allure.step("Заполняем форму"):
        driver.find_element(By.ID, "recipient-email").send_keys("Melnik@mail.ru")
        driver.find_element(By.ID, "recipient-name").send_keys("Student")
        driver.find_element(By.ID, "message-text").send_keys("Student!")
        driver.find_element(By.XPATH, "//button[text()='Send message']").click()

    with allure.step("Закрываем всплывающее окно"):
        alert = driver.switch_to.alert
        assert "Thanks for the message!!" in alert.text
        alert.accept()
        driver.save_screenshot("screen2.png")
        
def test_cart(driver):
    with allure.step("Открываем сайт"):
        driver.get("https://www.demoblaze.com/")

    with allure.step("Переходим в корзину"):
        driver.find_element(By.ID, "cartur").click()

    with allure.step("Проверяем ссылку"):
        assert driver.current_url == "https://www.demoblaze.com/cart.html"
        driver.save_screenshot("screen3.png")
