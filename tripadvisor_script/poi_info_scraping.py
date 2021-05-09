import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import logging as log
from json_lib import *
import re
from old_layout import *
from new_layout import *


now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = 'C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\script\\log\\'
log_file = f'poi_info_scraping_{now}.log'

log.basicConfig(filename=log_path+log_file, filemode='w',  level=log.INFO, format='[%(asctime)s] %(levelname)s : %(message)s')


log.info('Start Scraping')


chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

wait = 3


'''
poi_dict = {
    "id": "",
    "name": "",
    "url": "",
    "ranking": "",
    "partial_rank": "",
    "zone": "",
    "n_reviews": "",
    "rating": "",
    "categories": "",
    "address": "",
    "duration": "",
    "get_there": "",
    "mentions": "",
    "reviews": [],
}
'''

inputfile = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list\\poi_list_Milan.csv"
outputfile = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list_raw\\Poi_info_Milan.json"
errorfile = "C:\\Users\\alfon\\OneDrive - University of Pisa\\MasterBigData2021\\Progettone\\Alfonso\\scraping\\output\\poi_list_raw\\Poi_info_errors.json"

with open(outputfile, "w", encoding='utf-8') as f:
    json.dump({"pois": []}, f, indent=2)

with open(errorfile, "w", encoding='utf-8') as f:
    json.dump({"errors": []}, f, indent=2)

log.info('Open readfile')
with open(inputfile, 'r', newline='', encoding='utf-8') as csvread:
    reader = csv.reader(csvread, delimiter=',', quotechar='"')
    next(reader)

    count = 0
    for row in reader:
        count += 1
        poi_dict = {}
        if int(row[4]) >= 20:

            url = row[2]

            print(f'idx: {count}')
            print(row[1])
            print(url)

            log.info(f'idx: {count}')
            log.info(row[1])
            log.info(url)

            driver.get(url)
            time.sleep(1)

            try:
                cookies = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, "_evidon-accept-button")))
                cookies.click()
                log.info('Cookies Button')
            except:
                log.info('No Cookies Button')

            layout = ''
            try:
                name_elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, 'HEADING'))) #old layout
                #name_elem = driver.find_element_by_id('HEADING')  # old layout
                layout = 'old'
                log.info(f'Layout: {layout}')
            except:
                try:
                    name_elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.vgL7v_9B'))) #new layout
                    #name_elem = driver.find_element_by_css_selector('div.vgL7v_9B')  # new layout
                    layout = 'new'
                    log.info(f'Layout: {layout}')
                except:
                    print('Error: Name not Found')
                    log.error('Name not Found')


            print('layout: ' + layout)

            name = name_elem.text

            if name == row[1]:
                poi_dict['id'] = re.search(r'g187849-(.*?)-Reviews', url).group(1)
                poi_dict['name'] = name
                poi_dict['type'] = row[6]
                poi_dict['partial_rank'] = row[0]
                name_row = row[1]
                poi_dict['url'] = url
                poi_dict['zone'] = row[3]
                poi_dict['n_reviews'] = row[4]
                poi_dict['rating'] = row[5]

                if layout == 'old':
                    poi_dict, check_error = old_get_info(log, driver, poi_dict, wait)

                elif layout == 'new':
                    poi_dict, check_error = new_get_info(log, driver, poi_dict, wait)

                if check_error == 1:
                    log.info('Write Json None')
                    json_write_adding(errorfile, 'errors', poi_dict)

                log.info('Write Json file')
                json_write_adding(outputfile, 'pois', poi_dict)

            else:
                print('Error: No matching names')
                log.error('No matching names')
                no_match_dict = {'error': 'No matching names',
                                 'count': count,
                                 'url': url,
                                 'name_row': row[1],
                                 'name': name
                                }

                log.info('Write Json no_match')
                json_write_adding(errorfile, 'errors', no_match_dict)
                continue
        #break
driver.close()









