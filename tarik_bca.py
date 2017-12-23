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
from _bca_module import *

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 2)
    return driver
 
def login_bca(driver, username, password):
    data = []
    raw_data = []
    login=False

    driver.get(Config.get('bca', 'url'))
    try:
        elem = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "user_id")))
        elem.clear()
        elem.send_keys(username)
        
        elem = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "pswd")))
        elem.clear()
        elem.send_keys(password)

        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "value(Submit)")))
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
            driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'menu')))
            #try:
            # Click Account Information
            driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Informasi Rekening'))).click()
            #driver.find_element_by_link_text("Informasi Rekening").click()

            # Click Account Statement
            driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Mutasi Rekening'))).click()

            # Back to main frame
            driver.switch_to_default_content()
            driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'atm')))

            yesterday = datetime.now() - timedelta(days=1)
            day = yesterday.strftime("%d")
            month = int(yesterday.strftime("%m"))
            year = yesterday.strftime("%Y")
            yesterday = yesterday.strftime("%Y%m%d")

            elem = driver.wait.until(EC.presence_of_element_located((By.ID, 'startDt')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == day:
                    option.click()
                    break

            elem = driver.wait.until(EC.presence_of_element_located((By.ID, 'startMt')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == month:
                    option.click()
                    break

            elem = driver.wait.until(EC.presence_of_element_located((By.ID, 'startYr')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == year:
                    option.click()
                    break

            elem = driver.wait.until(EC.presence_of_element_located((By.ID, 'endDt')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == day:
                    option.click()
                    break

            elem = driver.wait.until(EC.presence_of_element_located((By.ID, 'endMt')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == month:
                    option.click()
                    break

            elem = driver.wait.until(EC.presence_of_element_located((By.ID, 'endYr')))
            options = elem.find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == year:
                    option.click()
                    break

            #time.sleep(2)
            driver.wait.until(EC.element_to_be_clickable((By.NAME, "value(submit1)"))).click()
            #except:
            #    pass

            rows = driver.find_elements_by_xpath("//table")
            row = rows[4].find_elements_by_tag_name("tr")
            for r in row:
                s = r.find_elements_by_tag_name("td")
                tmp = [str(i.text).replace("\n",";") for i in s]
                data.append(tmp)
                raw_data.append(tmp)
            if data[0]:
                data = data[1:]
                for i in range(len(data)):
                    try:
                        #print (data[i])
                        tmp = [j for j in data[i]]
                        t = tmp[1]
                        t = t.replace("\n", " ")
                        name = re.search(r'[0-9\.\,]+ [a-zA-Z]', t)
                        name = name.group().split(" ")
                        tmp[1] = t[(t.index(name[0]) + len(name[0]) + 1):].lower()
                        data[i] = tmp
                    except:
                        continue

            #time.sleep(30)
            #driver.switch_to_default_content()
            #driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'header')))
            #driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'LOGOUT'))).click()
 
        #driver.quit()
        
        if data:
            new_data, timenow = transactionLogBCA(raw_data, username, yesterday)
            transactionFilenameBCA = os.getcwd() + "/data/" + yesterday + "_TransactionBCA_" + username + ".txt"
            pendingTransactionBCA(new_data, transactionFilenameBCA, yesterday, timenow, username)

        return login
    except TimeoutException:
        print("Element(s) not found in klikbca.com")
        return login

if __name__ == "__main__":
    # get data config bca
    Config = ConfigParser.ConfigParser()
    Config.read("dist/config/config.txt")
    username = Config.get('bca', 'username')
    password = Config.get('bca', 'password')
    driver = init_driver()
    login = login_bca(driver, username, password)
    if login:
        driver.switch_to_default_content()
        driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'header')))
        driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'LOGOUT'))).click()
    #time.sleep(5)
    driver.quit()
