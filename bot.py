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
from tarik_bca import *

from mandiri_module import *

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

        while True:
            driver.switch_to_default_content()
            driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'left_frame')))

            try:
                driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '4. Deposit'))).click()
                driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '4.1 Deposit'))).click()
                #driver.find_element_by_partial_link_text("4. Deposit").click()
                #driver.find_element_by_partial_link_text("4.1 Deposit").click()
            except:
                driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '4. Deposit'))).click()
                driver.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '4.1 Deposit'))).click()
                #driver.find_element_by_partial_link_text("4. Deposit").click()
                #driver.find_element_by_partial_link_text("4.1 Deposit").click()

            driver.switch_to_default_content()
            driver.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'right_frame')))
            elem = driver.find_elements_by_xpath("//table//tr[@align='center']")

            nDelay = 0
            nameLength = 0
    
            BCA_FLAG = 0
            BNI_FLAG = 0
            BRI_FLAG = 0
            DANAMON_FLAG = 0
            MANDIRI_FLAG = 0
    
            BCA = []
            BNI = []
            BRI = []
            DANAMON = []
            MANDIRI = []
            #comment for test
            #if len(elem) > 0:
            nameLength = int(Config.get('settings', 'CHARACTERS'))
            nDelay = Config.get('settings', 'WAIT_DELAY')
            BCA_FLAG = Config.get('settings', 'BCA')
            BNI_FLAG = Config.get('settings', 'BNI')
            BRI_FLAG = Config.get('settings', 'BRI')
            DANAMON_FLAG = Config.get('settings', 'DANAMON')
            MANDIRI_FLAG = Config.get('settings', 'MANDIRI')
            Delay = int(nDelay)
            #comment for test
            for e in elem:
                rows = e.find_elements_by_tag_name("td")
                deposit_list = [str(r.text).replace('\n', ';') for r in rows[:11]]
                if len(deposit_list) == 1:
                    break
                #deposit_list = ['1','oujisama','okecash88','0.00','MANDIRI;YUDHA PERMANA;1060011651117;BCA;DEDE FIRMANSYAH;8830371576','2017-12-23 14:06:14','50.00','IDR','Member','Submitting']
                tmp = []
                for r in rows[11:]:
                    link = r.get_attribute("onclick")
                    if link:
                        link = str(link)
                        link = link[link.index('deposit.php'):]
                        link = "http://v02.okecash88.com/website/deposit/" + link[:len(link)-2]
                        tmp.append(link)
                #print transaction
                if 'BCA' in deposit_list[3].split(';'):
                    BCA.append(deposit_list + tmp)
                if 'BNI' in deposit_list[3].split(';'):
                    BNI.append(deposit_list + tmp)
                if 'BRI' in deposit_list[3].split(';'):
                    BRI.append(deposit_list + tmp)
                if 'DANAMON' in deposit_list[3].split(';'):
                    DANAMON.append(deposit_list + tmp)
                if 'MANDIRI' in deposit_list[3].split(';'):
                    MANDIRI.append(deposit_list + tmp)

            print 'BCA = '+str(BCA), 'BNI = '+str(BNI), 'BRI = '+str(BRI), 'DANAMON = '+str(DANAMON), 'MANDIRI = '+str(MANDIRI)
            MANDIRI = [['1','oujisama','okecash88','0.00','MANDIRI;INDAH ALIFIANI;1060011651117;BCA;DEDE FIRMANSYAH;8830371576','-','2017-12-23 14:06:14','10.00','IDR','Member','Submitting']]
            #BCA = [['1','oujisama','okecash88','0.00','MANDIRI;YUDHA PERMANA;1060011651117;BCA;DEDE FIRMANSYAH;8830371576','2017-12-23 14:06:14','50.00','IDR','Member','Submitting']]
            #BCA = [["NUR", "111111111;Ir. NURHANDAYANTO", "3,300.00", "17-12-2017 00:00:00"], ["KARIM", "222222222;Karimba", "100.00", "17-12-2017 00:00:00"]]
            BCA = [['1','NUR', 'okecash88','0.00','BCA;Ir. NURHANDAYANTO;11111111111','','2017-12-23 14:06:14','3,300.00', 'IDR','Member','Submitting'], ['2','KARIM', 'okecash88','0.00','BCA;Karimba;222222222','','2017-12-23 14:06:14','100.00', 'IDR','Member','Submitting']]

            if len(BCA) and BCA_FLAG:
                Config_bank = ConfigParser.ConfigParser()
                Config_bank.read("dist/config/config.txt")
                username_bank = Config_bank.get('bca', 'USERNAME')
                password_bank = Config_bank.get('bca', 'PASSWORD')
                #execfile('tarik_bca.py')

                processData = []
                pendingData = []
                for deposit in BCA:
                    found_action = None
                    amount = deposit[7].split('.')
                    a,b = amount[0], '0.'+amount[1]
                    amount = int("".join(a.split(',')))*1000 + float(b)*1000
                    amount = '{:,.2f}'.format(amount)
        
                    name = deposit[4].split(';')
                    name, account_number = name[1], name[0]
                    date = deposit[6].split(' ')
                    date = date[0].split('-')
                    date = date[0] + '/' + date[1]
        
                    today = datetime.now().strftime("%Y%m%d")
                    pendingFilenameBCA = os.getcwd() + "/data/" + today + "_pendingTransactionBCA_" + username_bank + ".txt"
        
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
        
                processTransactionBCA(processData, username_bank)

            # ------------------------------------------------------------ #
            # MANDIRI
            # ------------------------------------------------------------ #
            #MANDIRI = [['1','oujisama','okecash88','0.00','MANDIRI;YUDHA PERMANA;1060011651117;BCA;DEDE FIRMANSYAH;8830371576',' ','2017-12-23 14:06:14','50.00','IDR','Member','Submitting']]
            if len(MANDIRI) and MANDIRI_FLAG:
                Config_bank = ConfigParser.ConfigParser()
                Config_bank.read("dist/config/config.txt")
                username_bank = Config_bank.get('mandiri', 'USERNAME')
                password_bank = Config_bank.get('mandiri', 'PASSWORD')

                # Write today transaction
                today = datetime.now().strftime("%Y%m%d")
                pendingFilenameMandiri = os.getcwd() + "/data/" + today + "_pendingTransactionMandiri_" + username_bank + ".txt"

                #new_data, timenow = transactionLogMandiri(raw_mandiri_data, username_bank)
                #today = datetime.now().strftime("%Y%m%d")
                #notFoundFilenameMandiri = os.getcwd() + "/data/" + today + "_notFoundTransactionMandiri.txt"
                #transactionFilenameMandiri = os.getcwd() + "/data/" + today + "_TransactionMandiri_" + username_bank + ".txt"
                #pendingFilenameMandiri = os.getcwd() + "/data/" + today + "_pendingTransactionMandiri_" + username_bank + ".txt"
                #pendingTransactionMandiri(new_data, transactionFilenameMandiri, timenow, username_bank)

                processData = []
                pendingData = []
                for deposit in MANDIRI:
                    found_action = None
                    amount = deposit[7].split('.')
                    a,b = amount[0], '0.'+amount[1]
                    amount = int("".join(a.split(',')))*1000 + float(b)*1000
                    amount = '{:,.2f}'.format(amount)
                    amount = amount.replace('.','_')
                    amount = amount.replace(',','.')
                    amount = amount.replace('_',',')
                    name = deposit[4].split(';')
                    name, account_number = name[1], name[2]
                    date = deposit[6].split(' ')
                    date = date[0].split('-')
                    date = date[2] + '/' + date[1]

                    lines = []
                    
                    if os.path.exists(pendingFilenameMandiri):
                        with open(pendingFilenameMandiri, 'r') as f:
                            lines = f.readlines()
                    for line in lines:
                        try:
                            line = line.strip('\n')
                            tmp = line.split('||')
                            if (name.lower() in tmp[2].lower() and len(name) >= nameLength and nameValidation(name, tmp[2])) or (account_number in tmp[2]) and tmp[4] == amount and tmp[3]== 'CR':
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
                                updatePendingTransactionMandiri(line, pendingFilenameMandiri)
                                notFoundTransactionLogMandiri(deposit[1:9], Delay, name, True)
                                break
                        except:
                            pass
                    if not found_action and notFoundTransactionLogMandiri(deposit[1:9], Delay, name):
                        l = amount
                        #driver.execute_script("window.open('" + l + "', '_blank');")
                        #time.sleep(2)
                        #elem = driver.find_element_by_tag_name("body")
                        #elem.send_keys(Keys.CONTROL + 'w')

                processTransactionMandiri(processData, username_bank)

            driver.get("http://v02.okecash88.com/logout.php")
            #time.sleep(3)
            #driver.quit()

    except TimeoutException:
        #driver.get("http://v02.okecash88.com/logout.php")
        print("ok")

if __name__ == "__main__":
    Config = ConfigParser.ConfigParser()
    Config.read("dist/config/_settings.txt")
    username = Config.get('settings', 'OKECASH88_USERNAME')
    password = Config.get('settings', 'OKECASH88_PASSWORD')
    driver = init_driver()
    login_bo_okecash88(driver, username, password)
    time.sleep(3)
    driver.quit()
