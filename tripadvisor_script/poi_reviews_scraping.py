import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from json_lib import *
import re
from log_config import *
from old_layout import *
from new_layout import *

inputfile = "C:\\Users\\alfon\\Documents\\Master\\Progettone\\scraping\\tripadvisor_output\\poi_list\\poi_list_Milan.csv"
outputpath = "C:\\Users\\alfon\\Documents\\Master\\Progettone\\scraping\\tripadvisor_output\\reviews\\"
log_path = "C:\\Users\\alfon\\Documents\\Master\\Progettone\\scraping\\tripadvisor_output\\reviews\\log\\"


#[start, end] = intervallo chiuso da ambo i lati
#start parte da uno
START_IDX = 80
#end è compreso in automatico
END_IDX = 80


languages = ['Italiano', 'English']


chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

print('Start Scraping')

'''
reviews_dict = {
    "id": "",
    "name: "",
    "url_com": "",
    "url_it": "",
    "reviews": [],
}
'''

wait = 3

print('Open input csvfile')
with open(inputfile, 'r', newline='', encoding='utf-8') as csvread:
    reader = csv.reader(csvread, delimiter=',', quotechar='"')
    data = list(reader)

domain_ita = "www.tripadvisor.it"
domain_com = "www.tripadvisor.com"

for row in data[START_IDX:END_IDX+1]:
    reviews_dict = {}
    index = row[0]
    ID = row[1]
    name = row[2]
    url_com = row[3]
    url_it = url_com.replace(domain_com, domain_ita)

    print('\nInitialize output file')
    outputfile = f'{outputpath}{ID}.json'
    errorfile = f'{outputpath}{ID}_errors.json'

    print('Initialize log file')
    log_all = f'{log_path}{ID}_ALL.log'
    log_error = f'{log_path}{ID}_ERROR.log'
    log = create_log(ID, log_all, log_error)

    reviews_dict['id'] = ID
    reviews_dict['name'] = name
    reviews_dict['url_com'] = url_com
    reviews_dict['url_it'] = url_it

    errors_dict = reviews_dict.copy()
    errors_dict['errors'] = []

    reviews_dict['reviews'] = []

    for lang in languages:

        if lang == 'Italiano':
            url = url_it
        elif lang == 'English':
            url = url_com

        print(f'\nIndex: {index}')
        print(f'ID: {ID}')
        print(name)
        print(url)
        print(f'Language: {lang}')

        log.error(f'Index: {index}')
        log.error(f'ID: {ID}')
        log.error(name)
        log.error(url)
        log.error(f'Language: {lang}')

        driver.get(url)

        try:
            cookies = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "_evidon-accept-button")))
            cookies.click()
            print('Cookies Button')
            log.info('Cookies Button')
        except:
            print('No Cookies Button')
            log.info('No Cookies Button')

        layout = ''
        try:
            name_elem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'HEADING')))  # old layout
            #name_elem = driver.find_element_by_id('HEADING')  # old layout
            layout = 'old'
            log.error(f'Layout: {layout}')
        except Exception as e:
            try:
                name_elem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.vgL7v_9B')))  # new layout
                #name_elem = driver.find_element_by_css_selector('div.vgL7v_9B')  # new layout
                layout = 'new'
                log.error(f'Layout: {layout}')
            except Exception as e:
                layout = None
                print('Error: Name not Found: Skipping!')
                print(e)
                log.error('Name not Found: Skipping!')
                log.error(e)
                continue

        print('layout: ' + layout)

        if layout == 'old':
            old_get_reviews(log, outputfile, errorfile, ID, url, driver, wait, reviews_dict, errors_dict, lang)
        elif layout == 'new':
            new_get_reviews(log, outputfile, errorfile, ID, url, driver, wait, reviews_dict, errors_dict, lang)

        print(f'End Scraping: {ID}, language:{lang}')
        log.info(f'End Scraping: {ID}, language:{lang}\n')
    logging.shutdown()

print('End Scraping!')
#log.info('End Scraping!')
driver.close()
#logging.shutdown()

