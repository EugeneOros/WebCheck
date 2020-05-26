from time import sleep
from selenium import webdriver
from functools import partial
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import read_write_data as data
import email_send
from multiprocessing.pool import ThreadPool
import login
import re
import threading


def check_changes(url, element):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    if element == '':
        element = '/html/body'
    try:
        driver.get(url)
        mainPage = driver.find_element_by_xpath(element).text
        actualPage = mainPage
        while mainPage == actualPage:
            driver.get(url)
            actualPage = driver.find_element_by_xpath(element).text
            sleep(1)
        driver.get('https://www.google.com/')
        sleep(10)
    except NoSuchElementException:
        print('Cant find element')
    except WebDriverException:
        print("cant reach site.Chrome closed")
    finally:
        print('My work is done')
        driver.quit()


def check_if_price_lower(element, _FINISHED):
    # login.allegro_login(element['login'], element['password'])
    allegro_login = element["login"]
    allegro_password = element["password"]
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    options.add_argument("headless")
    options.add_argument("no-default-browser-check")
    options.add_argument("no-first-run")
    options.add_argument("no-sandbox")
    # with this options driver will work in background
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    url_login = 'https://allegro.pl/login/form?authorization_uri=https:%2F%2Fallegro.pl%2Fauth%2Foauth%2Fauthorize%3Fclient_id%3Dtb5SFf3cRxEyspDN%26redirect_uri%3Dhttps:%2F%2Fallegro.pl%2Flogin%2Fauth%26response_type%3Dcode%26state%3DhgnqyY&oauth=true'
    driver.get(url_login)
    driver.set_window_size(1100, 750)
    driver.find_element_by_xpath("//*[contains(text(), 'przejdź dalej')]").click()
    driver.find_element_by_id('username').send_keys(allegro_login)
    driver.find_element_by_id('password').send_keys(allegro_password)
    driver.find_element_by_id('login-button').click()
    print("zalogowałem się")
    actualPrice = float(element['price'])
    driver.get(element["link"])
    try:
        while actualPrice >= float(element['price']):

            if _FINISHED[element["link"]]:
                break

            driver.get(element["link"])
            priceText = re.split(' ', driver.find_element_by_xpath(element['xpath']).text)
            priceInParts = re.split(',', priceText[0])
            actualPrice = float(priceInParts[0]) + float(priceInParts[1]) / 100
            print(priceText, "   ", priceInParts, "   ", actualPrice)
            sleep(element["time"])
    except NoSuchElementException:
        print('Cant find element')
    except WebDriverException:
        print("cant reach site/Chrome closed")
    except AttributeError:
        print("Attribute not found")
    finally:
        print('My work is done')
        if actualPrice < element["price"]:
            if not element["is_monitoring"]:
                driver.find_element_by_id('buy-now-button').click()
            email_send.send_email(element["email_to_send"], element["link"], actualPrice)
        driver.quit()


def start_monitor(shared_dict):
    print("I'm starting to monitor")
    actual_index = 0
    pools = {}
    while True:
        # if shared_dict['isTerminatedP2']:
        #     shared_dict['isTerminatedP2'] = False
        previous_iteration_elements = {elem["link"]: elem for elem in pools.values()}
        previous_pools = pools
        elements_all = data.read_monitored_elements()
        for e in elements_all:
            # print((e["is_on"] is False, e["name"])
            if e["is_done"] is False and e["is_on"] is True and e not in pools.values():
                print("dodaje")
                shared_dict[e["link"]] = False
                globals()['pool%s' % actual_index] = ThreadPool(processes=1)
                pools[globals()['pool%s' % actual_index]] = e
                monitor_fun = partial(check_if_price_lower, _FINISHED=shared_dict)
                globals()['pool%s' % actual_index].apply_async(monitor_fun, (e,))
                # globals()['pool%s' % actual_index].close()
                actual_index += 1
                sleep(0.5)
            elif e["is_done"] is True or e["is_on"] is False and e["link"] in previous_iteration_elements:
                print("usuwam")
                shared_dict[e["link"]] = True
                pool_to_remove = list(pools.keys())[list(pools.values()).index(previous_iteration_elements[e["link"]])]
                pools.pop(pool_to_remove)
                pool_to_remove.terminate()
                pool_to_remove.join()
        if len(elements_all) < len(pools):
            # for e in pools.values():
            for e in list(previous_pools.values()):
                if e not in elements_all:
                    pool_to_remove = list(pools.keys())[list(pools.values()).index(previous_iteration_elements[e["link"]])]
                    shared_dict[e["link"]] = True
                    pools.pop(pool_to_remove)
                    pool_to_remove.terminate()
                    pool_to_remove.join()
                    if len(elements_all) >= len(pools):
                        shared_dict[e["link"]] = False
                        break
        sleep(0.1)


if __name__ == "__main__":
    _FINISHED = {}
    start_monitor(_FINISHED)
