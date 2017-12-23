import ConfigParser
import time
from datetime import datetime, timedelta
import re
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from _mandiri_module import *

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 2)
    return driver
 
def parseMandiriData(data):
    data[1] = data[1].replace('\n', ' ')
    if data[3]=='0,00':
        return data[0:2] + ['DB'] + [data[2]]
    if data[2]=='0,00':
        return data[0:2] + ['CR'] + [data[3]]
    return []

def lookup(driver, username, password):
    raw_data = []
    login=False

    driver.get(Config.get('mandiri', 'url'))
    try:
        elem = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "userID")))
        elem.clear()
        elem.send_keys(username)
        
        elem = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "password")))
        elem.clear()
        elem.send_keys(password)

        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "image")))
        button.click()

        try:
            #driver.wait.until(EC.alert_is_present(),
            #                       'Anda dapat melakukan login kembali setelah 10 menit / ' +
            #                       'You can re-login after 10 minutes.')
            alert = driver.switch_to_alert()
            time.sleep(3)
            alert.accept()
        except:
            login = True

            driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'toc')))
            # Click Account Information
            #driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Account Summary'))).click()
            driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Informasi Rekening'))).click()

            # Click Account Statement
            #driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Transaction History'))).click()
            driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Mutasi Rekening'))).click()

            # Back to main frame
            driver.switch_to_default_content()
            driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'CONTENT')))
            driver.find_element_by_xpath("//input[@value='R']").click()
            #driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value='R']')))
            yesterday = datetime.now() - timedelta(days=7)
            day = yesterday.strftime("%d")
            month = yesterday.strftime("%b")
            year = yesterday.strftime("%Y")
            yesterday = yesterday.strftime("%Y%m%d")

            elem = driver.wait.until(EC.presence_of_element_located((By.NAME, 'fromDay')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == day:
                    option.click()

            elem = driver.wait.until(EC.presence_of_element_located((By.NAME, 'fromMonth')))
            elem = driver.find_element_by_name("fromMonth")
            for option in options:
                if option.get_attribute('value') == month:
                    option.click()

            elem = driver.wait.until(EC.presence_of_element_located((By.NAME, 'fromYear')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == year:
                    option.click()

            elem = driver.wait.until(EC.presence_of_element_located((By.NAME, 'toDay')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == day:
                    option.click()

            elem = driver.wait.until(EC.presence_of_element_located((By.NAME, 'toMonth')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == month:
                    option.click()

            elem = driver.wait.until(EC.presence_of_element_located((By.NAME, 'toYear')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == year:
                    option.click()

            driver.wait.until(EC.element_to_be_clickable((By.ID, "linksubmit"))).click()

            elem = driver.find_elements_by_class_name("tabledata")
            n = 0
            while n < len(elem):
                data = parseMandiriData([str(e.text) for e in elem[n:n+4]])
                deposit_list = [str(r.text).replace('\n', ';') for r in elem[:11]]
                if data:
                    raw_data.append(data)
                n += 4
            raw_data = raw_data[::-1]
            print(deposit_list)

        if raw_data:
            new_data, timenow = transactionLogMandiri(raw_data, username, yesterday)
            transactionFilenameMandiri = os.getcwd() + "/data/" + yesterday + "_TransactionMandiri_" + username + ".txt"
            pendingTransactionMandiri(new_data, transactionFilenameMandiri, yesterday, timenow, username)

        return login
    except TimeoutException:
        print("Element(s) not found in bankmandiri.com")
        return login

if __name__ == "__main__":
    # get data config mandiri
    Config = ConfigParser.ConfigParser()
    Config.read("dist/config/config.txt")
    username = Config.get('mandiri', 'username')
    password = Config.get('mandiri', 'password')
    driver = init_driver()
    login = lookup(driver, username, password)
    if login:
        driver.switch_to_default_content()
        driver.switch_to_frame("top")
        driver.find_element_by_partial_link_text("LOGOUT").click()

    #time.sleep(5)
    driver.quit()
