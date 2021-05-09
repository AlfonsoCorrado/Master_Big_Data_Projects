import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import logging as log
from selenium.webdriver.support.ui import WebDriverWait
from json_lib import *
import re
from old_layout import *
from new_layout import *

#inserire ID del poi da riparare (prende le restanti recensioni nel caso si sia rotto durante lo scraping)
ID = 'd10067145'

now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = 'C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\script\\log\\'
log_file = f'poi_reviews_repair_{now}.log'
log.basicConfig(filename=log_path+log_file, filemode='w',  level=log.INFO, format='[%(asctime)s] %(levelname)s : %(message)s')

log.info('Start Scraping')

chrome_options = Options()

#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

wait = 3

domain_com = "www.tripadvisor.com"
domain_it = "www.tripadvisor.it"

inputfile = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list\\poi_list_Milan.csv"
outputpath = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\reviews_raw\\"

log.info(f'id: {ID}')
print(f'id: {ID}')

log.info('Open Json files')
print('Open Json files')

outputfile = f'{outputpath}{ID}.json'
errorfile = f'{outputpath}{ID}_errors.json'

reviews_dict = json_load(outputfile)
errors_dict = json_load(errorfile)

url = reviews_dict['url']
#url_it = url.replace(domain_com, domain_it)

page = reviews_dict['reviews'][-1]['page']
page = 'or' + str(int(page.replace('or', ''))+5)

start_url = re.sub(f'{ID}-Reviews', f'{ID}-Reviews-{page}', url)

print(reviews_dict['name'])
print(start_url)

log.info(reviews_dict['name'])
log.info(start_url)

driver.get(start_url)

try:
    cookies = WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.ID, "_evidon-accept-button")))
    cookies.click()
    log.info('Cookies Button')
except:
    log.info('No Cookies Button')

old_get_reviews(log, outputfile, errorfile, driver, wait, reviews_dict, errors_dict, start_url)

driver.close()

