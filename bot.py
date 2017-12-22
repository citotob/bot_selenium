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

from bca_module import *

def nameValidation(name, line):
    name = name.lower()
    line = line.lower()
    if name == line:
        return True
    if name not in line:
        return False
    try:
        x = line.index(name)
        y = len(name)
        if line.endswith(name):
            return True
        if line[x+y] == ' ':
            return True
        else:
            return False
    except:
        return False
    return False

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 3)
    return driver

def login_bo_okecash88(driver, username, password):
    driver.get(Config.get('settings', 'OKECASH88_URL'))
    try:
        elem = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")))
        elem.clear()
        elem.send_keys(username)

        elem = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "password")))
        elem.clear()
        elem.send_keys(password)

        elem = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "captchaSource")))
        captcha = elem.get_attribute('value')
        elem = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "captcha")))
        elem.clear()
        elem.send_keys(str(captcha))

        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "login")))
        button.click()

        nameLength = int(Config.get('settings', 'CHARACTERS'))
        Delay = Config.get('settings', 'WAIT_DELAY')
        processData = []
        pendingData = []
        BCA = [["NUR", "111111111;Ir. NURHANDAYANTO", "3,300.00", "17-12-2017 00:00:00"], ["KARIM", "222222222;Karimba", "100.00", "17-12-2017 00:00:00"]]
        for deposit in BCA:
            found_action = None
            amount = deposit[2].split('.')
            a,b = amount[0], '0.'+amount[1]
            amount = int("".join(a.split(',')))*1000 + float(b)*1000
            amount = '{:,.2f}'.format(amount)

            name = deposit[1].split(';')
            name, account_number = name[1], name[0]
            date = deposit[3].split(' ')
            date = date[0].split('-')
            date = date[0] + '/' + date[1]

            today = datetime.now().strftime("%Y%m%d")
            pendingFilenameBCA = os.getcwd() + "/data/" + today + "_pendingTransactionBCA_" + username + ".txt"

            lines = []
            if os.path.exists(pendingFilenameBCA):
                with open(pendingFilenameBCA, 'r') as f:
                    lines = f.readlines()
            for line in lines:
                try:
                    line = line.strip('\n')
                    tmp = line.split('||')
                    sender_name = tmp[2].split(';')
                    sender_name = sender_name[len(sender_name)-1].lower()
                    if name.lower() in tmp[2].lower() and tmp[4] == amount and tmp[5].lower() == 'cr' and len(name) >= nameLength and nameValidation(name, tmp[2]):
                        found_action = 1
                        #l = deposit[11]
                        #driver.execute_script("window.open('" + l + "', '_blank');")
                        #time.sleep(2)
                        #elem = driver.find_element_by_tag_name("body")
                        #elem.send_keys(Keys.CONTROL + 'w')
                        #l = l.replace("process", "confirm")
                        #driver.execute_script("window.open('" + l + "', '_blank');")
                        #time.sleep(2)
                        #elem = driver.find_element_by_tag_name("body")
                        #elem.send_keys(Keys.CONTROL + 'w')
                        timenow = datetime.now().strftime("%H:%M:%S")
                        processData.append(tmp + [account_number, today, timenow])
                        updatePendingTransactionBCA(line, pendingFilenameBCA)
                        notFoundTransactionLogBCA(deposit[1:], Delay, name, True)
                        break
                except:
                    pass

            if not found_action and notFoundTransactionLogBCA(deposit[1:], Delay, name):
                l = amount

        processTransactionBCA(processData, username)

    except TimeoutException:
        print("Element(s) not found in okecash88.com")

if __name__ == "__main__":
    Config = ConfigParser.ConfigParser()
    Config.read("dist/config/_settings.txt")
    username = Config.get('settings', 'OKECASH88_USERNAME')
    password = Config.get('settings', 'OKECASH88_PASSWORD')
    driver = init_driver()
    login_bo_okecash88(driver, username, password)
    #time.sleep(10)
    driver.quit()
