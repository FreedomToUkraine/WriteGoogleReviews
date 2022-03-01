from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import re
import time
import json
from time import sleep

LOGIN_COUNT=0

def read_json(filename):
    with open(filename, encoding="utf8") as f:
        data = json.load(f)
    return data
            
def wait_to_click(driver, delay, xpath):
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,xpath)))
    button = driver.find_element(By.XPATH,xpath)
    button.click()

def scroll_to_click(driver, delay, xpath,p):
    sleep(2)
    count=0
    while(count<6):
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,xpath)))
            error = False
            button = driver.find_element(By.XPATH,xpath)
            button.click()
            write_review(driver, delay)
        except Exception as exception:
            error = True
            print(exception)

        if error:
            count=count+1
            if(count%2==1):
                driver.execute_script('''document.querySelector(\".section-scrollbox:nth-child(1)\").scrollTo(0,document.querySelector(\".section-scrollbox:nth-child(1)\").scrollHeight/2)''')
            else:    
                driver.execute_script('''document.querySelector(\".section-scrollbox:nth-child(1)\").scrollTo(0,document.querySelector(\".section-scrollbox:nth-child(1)\").scrollHeight)''')
        else:
            return

    raise RuntimeError('Something obscures the element. I am skipping the iteration.') from None


def write_review(driver, delay):
    try:
        try:
            sleep(3)
            reviews_xpath="/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button"
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,reviews_xpath)))
            button = driver.find_element(By.XPATH,reviews_xpath)
            button.click()
        except:
            return

        write_xpath="/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[4]/div/button/span"
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH,write_xpath)))
        button = driver.find_element(By.XPATH,write_xpath)
        button.click()

        global LOGIN_COUNT
        while LOGIN_COUNT==0:
            sleep(20)
            LOGIN_COUNT=1

        sleep(5)            
        actions = ActionChains(driver)
        

        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.TAB)
        actions.send_keys('Было хорошо! Однако, Путин испортил нам настроение, вторгшись в Украину. Восстаньте  против своего диктатора, прекратите убивать невинных людей! Ваше правительство лжет вам. Восстаньте!')
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        sleep(5)
    except Exception as exception: 
        print(exception)
        return


def main():
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.page_load_strategy = 'none'
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)
    delay = 5
    short_delay=2
    v_short_delay = 1

    driver.get("https://www.google.com/maps/search/moscow+restaurant")
    agree_xpath = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span"
    wait_to_click(driver,delay,agree_xpath)

    city_list = read_json('data.json')

    for city in city_list["results"]:
        place=city['name']
        print(place)
        maps_link = f"https://www.google.com/maps/search/{place},+restaurant"     
        driver.get(maps_link)

        while(True):     
            try:
                results_number_xpath= "/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/span/span[2]"
                WebDriverWait(driver, short_delay).until(EC.presence_of_element_located((By.XPATH, results_number_xpath)))
            except:
                try:
                    results_number_xpath= "/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/span/span[2]"
                    WebDriverWait(driver, short_delay).until(EC.presence_of_element_located((By.XPATH, results_number_xpath)))
                except:
                    break
            results_number = driver.find_element(By.XPATH, results_number_xpath).text
            results_number = int(results_number)%20
            print(results_number)
            if results_number%20==0:
                results_number=20

            for p in range(3,results_number*2):
                if p % 2 != 0:
                    print(p)

                    listing_xpath = f"/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[{p}]/div/a"
                    try:
                        scroll_to_click(driver,v_short_delay,listing_xpath,p)
                    except:
                        continue

                    try:
                        back_element ="/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[1]/button/img"
                        wait_to_click(driver,delay,back_element)
                    except:
                        driver.get(maps_link)
                         
            try:
                next_page_xpath = "/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[2]/div/div[1]/div/button[2]/img"
                wait_to_click(driver,v_short_delay,next_page_xpath)     
                sleep(2)         
            except:
                try:
                    next_page_xpath = "/html/body/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div/button[2]/img"
                    wait_to_click(driver,v_short_delay,next_page_xpath)     
                    sleep(3)        
                except:
                    break 


if __name__ == '__main__':
  main()