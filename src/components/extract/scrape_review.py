from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.logger import logging
from src.exception import CustomException

import time,sys


import pandas as pd
# SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQKedddvke65kn6omUuSdG6DTfHK9M5L_m1GHBRd-ui2VGx5drxVtH5BlFu3701ruu9P6EuWgmgIseJ/pub?gid=0&single=true&output=csv"
# df = pd.read_csv(SHEET_URL)


# linkedin = df['LinkedIn'].str.strip()
# linkedin.dropna(inplace=True)



def extract_data(link, headless):#, page=1):

    # firefox_binary = FirefoxBinary()
    url = f'{link}/review'
    # driver = 'geckodriver.exe'
    # driver = 'C:\\Users\\jonat\\Downloads\\geckodriver-v0.32.2-win32\\geckodriver.exe'
    # browser = webdriver.Firefox(firefox_binary=firefox_binary,executable_path=driver)
    options = Options()
    options.add_argument("--disable-javascript")
    if headless:
        options.add_argument('--headless')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
    # options.set_capability("marionette", True )
    # browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    browser.get(url)
    timeout = 6
    
    y = 10
    for timer in range(0,450):
        browser.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 7 
    
    i = 0
    
    return browser



def scrape_page(browser):
    timeout = 15
    
    class_dicts = {
        # "name" : "prd_link-product-name css-3um8ox",
        ## "price" : "prd_link-product-price css-1ksb19c",
        # "price": "prd_link-product-price css-h66vau",
        # "cashback(%)" : "prd_label-product-price css-tolj34",
        # "seller" : "prd_link-shop-name css-1kdc32b flip",
        # "location" : "prd_link-shop-loc css-1kdc32b flip",
        # "rating" : "prd_rating-average-text css-t70v7i",
        # # "sold" : "prd_label-integrity css-1duhs3e",
        # "sold" : "prd_label-integrity css-1sgek4h",
        # "price" : "prd_link-product-price css-1ksb19c",
        "username" : "name",
        "rating": "rating",
        "comment" : "css-ed1s1j-unf-heading e1qvo2ff8",
        "likes" : "css-q2y3yl",
        "date" : "css-1dfgmtm-unf-heading e1qvo2ff8"
    }

    els_dict = {x:[] for x in class_dicts.keys()}
    els_dict['additional_desc'] = []

    for x in browser.find_elements(By.XPATH,f"//div[@class='css-1k41fl7']"):
        # if x.get_attribute("class") == "css-1rn0irl":
        #     for y,k in zip(x.find_elements_by_tag_name("span"), ['location','seller']):
        #         els_dict[k].append(y.text)
        #     continue
        # logging.info(x.text)
        for k,v in class_dicts.items():
            try :
                if k == "rating":
                    els_dict[k].append(x.find_element(By.XPATH,f".//*[@class='{v}']").get_attribute('aria-label'))
                elif k=="likes":
                    # els_dict[k].append(x.find_element(By.XPATH,f".//*[@class='{v}']").text)
                    els_dict[k].append(x.find_element(By.XPATH,f".//*[@class='css-1ati3qk']//*[@class='{v}']").text)
                else :
                    els_dict[k].append(x.find_element(By.XPATH,f".//*[@class='{v}']").text)

            except :
                els_dict[k].append("")
        
        kendala = x.find_elements(By.XPATH,f".//*[@class='css-zhjnk4-unf-heading e1qvo2ff8']")
        if len(kendala) > 0:
            for k in kendala:
                els_dict['additional_desc'].append(k.text)
        else :
            els_dict['additional_desc'].append("")
                


    try :
        ActionChains(browser).move_to_element(
            WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "css-16uzo3v-unf-pagination-item")))
        ).perform()
    except :
        browser.refresh()
        ActionChains(browser).move_to_element(
            WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "css-16uzo3v-unf-pagination-item")))
        ).perform()

    buttons = browser.find_elements(By.CLASS_NAME, "css-16uzo3v-unf-pagination-item")
    # len_btn = len(buttons)
    for page in buttons:
        try :
            if page.get_attribute('aria-label') == "Laman berikutnya":
                page.click()
                logging.info("Found!, clicked!")
                break
            else :
                if len(buttons) == 1:
                    logging.info("All data has been sucessfully retrieved!")
                    return browser,els_dict
        except:
            logging.info("Error Occur! page text " + str(page.text))

    list_class_w = "css-1k41fl7"
    list_wait = EC.presence_of_element_located((By.CLASS_NAME, list_class_w))

    try :
        WebDriverWait(browser, 10).until(list_wait)
    except :
        browser.refresh()
        WebDriverWait(browser, 10).until(list_wait)


    y = 1000
    for timer in range(0,4):
        browser.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 1000  
        time.sleep(0.75)
    return browser,els_dict

def run(link, jumlah_halaman, headless=False):
    logging.info("Initializing...")
    data = pd.DataFrame()
    # link = "https://www.tokopedia.com/asus/asus-vivobook-a416mao-fhd426-slate-grey?extParam=ivf%3Dfalse%26src%3Dsearch%26whid%3D7377294"
    try :
        driver = extract_data(link,headless)
        logging.info("Start Scrapping")
        for n in range(1,jumlah_halaman+1):
            driver, data_dict = scrape_page(driver)
            data = pd.concat([data,pd.DataFrame(data_dict)])
            logging.info("Scrapping page " + str(n) + " success!")
        data['likes'] = data['likes'].map(lambda x : 0 if x == "Membantu" else x.split(" ")[0]).astype('int')
        # data.to_csv(f"laptop-review-tokped.csv", index=False)
    except Exception as err:
        try :
            raise CustomException(err,sys)
        except :
            pass
    return data



if __name__ == "__main__":
    logging.info("Initializing...")
    data = pd.DataFrame()
    link = "https://www.tokopedia.com/asus/asus-vivobook-a416mao-fhd426-slate-grey?extParam=ivf%3Dfalse%26src%3Dsearch%26whid%3D7377294"
    driver = extract_data(link)
    logging.info("Start Scrapping")
    for n in range(1,6):
        driver, data_dict = scrape_page(driver)
        data = pd.concat([data,pd.DataFrame(data_dict)])
        logging.info(data)
        logging.info("Scrapping page", n, "success!")
    data['likes'] = data['likes'].map(lambda x : 0 if x == "Membantu" else x.split(" ")[0]).astype('int')
    data.to_csv(f"laptop-review-tokped.csv", index=False)

# content = browser.find_element_by_xpath(name_xpath).text
# logging.info(content)