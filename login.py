from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def allegro_login(mail, password):
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)

    url_login = 'https://allegro.pl/login/form?authorization_uri=https:%2F%2Fallegro.pl%2Fauth%2Foauth%2Fauthorize%3Fclient_id%3Dtb5SFf3cRxEyspDN%26redirect_uri%3Dhttps:%2F%2Fallegro.pl%2Flogin%2Fauth%26response_type%3Dcode%26state%3DhgnqyY&oauth=true'
    driver.get(url_login)
    driver.set_window_size(1100, 750)
    driver.find_element_by_xpath("//*[contains(text(), 'przejdź dalej')]").click()
    driver.find_element_by_id( 'username').send_keys(mail)
    driver.find_element_by_id( 'password').send_keys(password)
    driver.find_element_by_id( 'login-button').click()
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(('name', 'string')))
    sleep(10)
    driver.quit()

