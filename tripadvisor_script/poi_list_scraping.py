import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)


host = 'https://www.tripadvisor.com'


#Categoria Sights & Landmarks
url_list = []
start_path = '/Attractions-g187849-Activities-c47'
end_path = '-Milan_Lombardy.html'

for x in range(0, 810+1, 30):
    if x == 0:
        url_list.append(host+start_path+end_path)
    else:
        url_list.append(host+start_path+'-oa'+str(x)+end_path)

filename = 'Landmarks_Milan.csv'

print('Start Scraping Sights & Landmarks')
count = 0
with open(filename, 'w', newline='', encoding='utf-8') as output_handle:
    writer = csv.writer(output_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    header = ['ranking', 'name', 'url', 'zone', 'n_reviews', 'rating']
    writer.writerow(header)

    for url in url_list:
        print('Page '+str(count))
        count +=1
        driver.get(url)
        pois = driver.find_elements_by_css_selector("._392swiRT") #seleziona i 30 PoI della pagina corrente
        for poi in pois:
            poi_url = poi.find_element_by_xpath("descendant::a[1]").get_attribute('href') #Url
            name = poi.find_element_by_xpath("descendant::a[1]").text #Ranking+Name
            poi_ranking = name.split('.')[0].strip() #Ranking = numero vicino al nome
            print('PoI ' + poi_ranking)
            poi_name = name.split('.', 1)[1].strip() #PoI Name
            try:
                poi_n_reviews = poi.find_element_by_css_selector(".zTTYS8QR").text.replace(',', '') #Numero di reviews
            except:
                print('0 Reviews')
                continue
            poi_rating = poi.find_element_by_css_selector(".zWXXYhVR").get_attribute('title').split()[0] #Rating=numero di stelline
            try:
                poi_zone = poi.find_element_by_css_selector(".ZtPwio2G > div:first-child").text  #quartiere/zona del PoI (Non è presente iin tutti i PoI)
            except:
                poi_zone=None
                print('Zone not found!')

            writer.writerow([poi_ranking, poi_name, poi_url, poi_zone, poi_n_reviews, poi_rating])

driver.close()
print('End Scraping')


# Categoria Museums
url_list=[]
start_path = '/Attractions-g187849-Activities-c49'
end_path = '-Milan_Lombardy.html'

for x in range(0, 180+1, 30):
    if x == 0:
        url_list.append(host+start_path+end_path)
    else:
        url_list.append(host+start_path+'-oa'+str(x)+end_path)

filename = 'Museums_Milan.csv'

print('Start Scraping Museums')
count = 0
with open(filename, 'w', newline='', encoding='utf-8') as output_handle:
    writer = csv.writer(output_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    header = ['ranking', 'name', 'url', 'zone', 'n_reviews', 'rating']
    writer.writerow(header)

    for url in url_list:
        print('Page '+str(count))
        count +=1
        driver.get(url)
        pois = driver.find_elements_by_css_selector("._392swiRT") #seleziona i 30 PoI della pagina corrente
        for poi in pois:
            poi_url = poi.find_element_by_xpath("descendant::a[1]").get_attribute('href')
            name = poi.find_element_by_xpath("descendant::a[1]").text
            poi_ranking = name.split('.')[0].strip()
            print('PoI ' + poi_ranking)
            poi_name = name.split('.', 1)[1].strip()
            try:
                poi_n_reviews = poi.find_element_by_css_selector(".zTTYS8QR").text.replace(',', '')
            except:
                print('0 Reviews')
                continue
            poi_rating = poi.find_element_by_css_selector(".zWXXYhVR").get_attribute('title').split()[0]
            try:
                poi_zone = poi.find_element_by_css_selector(".ZtPwio2G > div:first-child").text
            except:
                poi_zone=None
                print('Zone not found!')

            writer.writerow([poi_ranking, poi_name, poi_url, poi_zone, poi_n_reviews, poi_rating])

driver.close()
print('End Scraping')


# Categoria Nature
url_list=[]
start_path = '/Attractions-g187849-Activities-c57'
end_path = '-Milan_Lombardy.html'

for x in range(0, 90+1, 30):
    if x == 0:
        url_list.append(host+start_path+end_path)
    else:
        url_list.append(host+start_path+'-oa'+str(x)+end_path)

filename = 'Nature_Milan.csv'

print('Start Scraping Nature')
count = 0
with open(filename, 'w', newline='', encoding='utf-8') as output_handle:
    writer = csv.writer(output_handle, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    header = ['ranking', 'name', 'url', 'zone', 'n_reviews', 'rating']
    writer.writerow(header)

    for url in url_list:
        print('Page '+str(count))
        count +=1
        driver.get(url)
        pois = driver.find_elements_by_css_selector("._392swiRT") #seleziona i 30 PoI della pagina corrente
        for poi in pois:
            poi_url = poi.find_element_by_xpath("descendant::a[1]").get_attribute('href')
            name = poi.find_element_by_xpath("descendant::a[1]").text
            poi_ranking = name.split('.')[0].strip()
            print('PoI ' + poi_ranking)
            poi_name = name.split('.', 1)[1].strip()
            try:
                poi_n_reviews = poi.find_element_by_css_selector(".zTTYS8QR").text.replace(',', '')
            except:
                print('0 Reviews')
                continue
            poi_rating = poi.find_element_by_css_selector(".zWXXYhVR").get_attribute('title').split()[0]
            try:
                poi_zone = poi.find_element_by_css_selector(".ZtPwio2G > div:first-child").text
            except:
                poi_zone=None
                print('Zone not found!')

            writer.writerow([poi_ranking, poi_name, poi_url, poi_zone, poi_n_reviews, poi_rating])

driver.close()
print('End Scraping')

