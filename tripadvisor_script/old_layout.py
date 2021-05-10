from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
import time
import re
from json_lib import *


def old_get_info(log, driver, poi_dict, wait):
    check_error = 0
    log.info('Get Ranking')
    try:
        ranking_elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.LVF8hnT6')))
        ranking = ranking_elem.text.split()[0][1:]
    except:
        log.error('No Ranking')
        print('No Ranking')
        ranking = None
    poi_dict['ranking'] = ranking

    log.info('Get Categories')
    try:
        categories_elem = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_3RTCF0T0']//a")))
        categories = [x.text for x in categories_elem]
    except:
        log.error('No Categories')
        print('No Categories')
        categories = None
    poi_dict['categories'] = categories

    log.info('Get Address')
    try:
        address_elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//span[@class='ui_icon map-pin _3D9Qcwoe']/following-sibling::span")))
        address = address_elem.text
    except:
        log.error('No Address')
        print('No Address')
        address = None
    poi_dict['address'] = address

    log.info('Get Duration')
    try:
        duration_elem = driver.find_element_by_css_selector('._2y7puPsQ')
        duration = duration_elem.text.split(':')[1]
    except:
        log.warning('No Suggested Duration')
        duration = None
    poi_dict['duration'] = duration

    log.info('Get Getting There')
    try:
        getting_there_elem = driver.find_elements_by_xpath("//span[@class='_3WTwIb_9']/parent::div")
        getting_there = [x.text for x in getting_there_elem]
    except:
        getting_there = None
        log.warning('No Getting There')
    poi_dict['getting_there'] = getting_there

    log.info('Get Mentions')
    try:
        mentions_elem = driver.find_elements_by_xpath("//div[@class='_3oYukhTK']/button[position()>1]")
        mentions = [x.text for x in mentions_elem]
    except:
        mentions = None
        log.warning('No Mentions')
    poi_dict['mentions'] = mentions

    if None in [ranking, categories, address]:
        check_error = 1
    return poi_dict, check_error


def old_init_check(log, driver, wait, lang, click_on_lang=False):
    log.info('Get Initial Reviews for language click')
    try:
        reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class = 'Dq9MAugU T870kzTX LnVzGwUB']")))
    except Exception as e:
        log.error('No initial Reviews found: Skipping!')
        print('No initial Reviews found: Skipping!')
        print(e)
        log.error(e)
        reviews = None
        return 0

    try:
        lang_element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, f"//label[@class='bUKZfPPw']//*[text()='{lang}']")))
        lang_is_selected = lang_element.find_element_by_xpath("../preceding-sibling::input").is_selected()
    except Exception as e:
        log.error(f'Language {lang} not present: Skipping!')
        print(f'Language {lang} not present: Skipping!')
        print(e)
        log.error(e)
        return 0

    if lang_is_selected:
        log.info(f'Language: {lang} is already selected')
        print(f'Language: {lang} is already selected')
    elif click_on_lang:
        log.info(f'Language: {lang} click')
        print(f'Language: {lang} click')
        try:
            lang_element.click()
            # all_language = driver.find_element_by_xpath("//label[@class='bUKZfPPw']//*[text()='Tutte le lingue']")
            # all_language.click()
            for review in reviews:
                WebDriverWait(driver, wait).until(staleness_of(review))
        except Exception as e:
            log.error('Page not correctly loaded after language click: Skipping!')
            print('Page not correctly loaded after language click: Skipping!')
            print(e)
            log.error(e)
            return 0
    else:
        log.error(f'Language {lang} not preserved after force loading next page: Skipping!')
        print(f'Language {lang} not preserved after force loading next page: Skipping!')
        return 0
    return 1


def old_next_page(log, driver, wait, lang, ID, url, reviews, page, n_page, or_page, current_url):
    old_url = current_url
    need_next_page = False

    try:
        # next_page = driver.find_element_by_xpath("//a[@class='ui_button nav next primary ']")
        next_page = WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ui_button nav next primary ']")))
        next_page.click()
        try:
            for review in reviews:
                WebDriverWait(driver, wait).until(staleness_of(review))
        except Exception as e:
            log.error(f"Can't load next page. n_page: {n_page} , or_page: {or_page} , url: {current_url}")
            print(f"Can't load next page. n_page: {n_page} , or_page: {or_page} , url: {current_url}")
            print(e)
            log.error(e)
            need_next_page = True
    except Exception as e:
        log.error(f'Next page not Found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
        print(f'Next page not Found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
        print(e)
        log.error(e)
        need_next_page = True

    if old_url == driver.current_url or need_next_page:
        log.error("TripAdvisor can't go on next page: Trying to force next page url...")
        print("TripAdvisor can't go on next page: Trying to force next page url...")
        next_or_page = 'or' + str(int(page) + 5)
        next_url = re.sub(f'{ID}-Reviews', f'{ID}-Reviews-{next_or_page}', url)
        driver.get(next_url)
        if not old_init_check(log, driver, wait, lang, click_on_lang=False):
            log.error(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
            print(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
            return 0
    return 1


def old_get_reviews(log, outputfile, errorfile, ID, url, driver, wait, reviews_dict, errors_dict, lang):
    # Reviews
    log.info('Start scraping Reviews')
    n_page = 0

    if not old_init_check(log, driver, wait, lang):
        return

    log.info('Get last page number')
    try:
        last_page = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//div[@class='pageNumbers']/a[last()]"))).text
    except:
        last_page = None
        log.error('Last Page not found! Assuming only 1 page of reviews')
        print('Last Page not found! Assuming only 1 page of reviews')

    '''
    #Codice per inziare da una specifica pagina di recensioni (in caso di rottura codice prima dell'ultima pagina)
    if start_url:
        log.info(f'Start from page {driver.current_url}')
        print(f'Start from page {driver.current_url}')
        current_page = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//div[@class='pageNumbers']/span[@class='pageNum current disabled']"))).text
        n_page = int(current_page) - 1
        if current_page == last_page:
            print('Already scraped all review pages for this PoI!!!')
            log.info('Already scraped all review pages for this PoI!!!')
            exit()
    '''

    while True:
        n_page += 1
        current_url = driver.current_url
        need_next_page = False

        #page = 'or'+re.search(r'Reviews-or(.*?)-', current_url).group(1)
        page = re.findall(r'Reviews-or(.*?)-', current_url)
        if len(page) == 0:
            page = 0
            or_page = ''
        else:
            page = page[0]
            or_page = 'or' + page

        try:
            #reviews = driver.find_elements_by_xpath("//div[@class = 'Dq9MAugU T870kzTX LnVzGwUB']")
            reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class = 'Dq9MAugU T870kzTX LnVzGwUB']")))
        except Exception as e:
            log.error(f'No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
            print(f'No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
            print(e)
            log.error(e)
            log.error("Trying to force same page url...")
            print("Trying to force same page url...")
            driver.get(current_url)
            if not old_init_check(log, driver, wait, lang, click_on_lang=False):
                log.error(f"Force loading same page failed: Skipping page! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                print(f"Force loading same page failed: Skipping page! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                need_next_page = True
            else:
                try:
                    reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class = 'Dq9MAugU T870kzTX LnVzGwUB']")))
                except Exception as e:
                    log.error(f'No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                    print(f'No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                    print(e)
                    log.error(e)
                    need_next_page = True

            if need_next_page:
                log.error("Trying to force next page url...")
                print("Trying to force next page url...")
                next_or_page = 'or' + str(int(page) + 5)
                next_url = re.sub(f'{ID}-Reviews', f'{ID}-Reviews-{next_or_page}', url)
                driver.get(next_url)
                if not old_init_check(log, driver, wait, lang, click_on_lang=False):
                    log.error(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                    print(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                    return
                else:
                    continue

        log.info(f'Page {n_page}: {len(reviews)} reviews')
        print(f'Page {n_page}: {len(reviews)} reviews')

        try:
            #basta cliccare una sola volta su read more per ogni pagina che automaticamente espande tutte le reviews
            log.info('Click on Read more')
            #read_more = WebDriverWait(driver, wait[3]).until(EC.presence_of_element_located((By.XPATH, "//div[@class='XUVJZtom']")))
            read_more = driver.find_element_by_xpath("//div[@class='XUVJZtom']")
            read_more.click()
        except Exception as e:
            log.error(f'No Read more found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
            print(f'No Read more found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
            print(e)
            log.error(e)

        for i in range(len(reviews)):
            review = reviews[i]
            review_dict = {}

            log.info('Get User')
            try:
                user = WebDriverWait(review, wait).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='_2fxQ4TOx']//a"))).get_attribute('href').split('/')[-1]
                #user = review.find_element_by_xpath(".//div[@class='_2fxQ4TOx']//a").get_attribute('href').split('/')[-1]
                review_dict['user'] = user
            except Exception as e:
                log.error(f'Skipping review {i+1}! No User. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                print(f'Skipping review {i+1}! No User. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                print(e)
                log.error(e)
                continue

            review_dict['review'] = {}

            log.info('Get Rating')
            try:
                rating = WebDriverWait(review, wait).until(EC.presence_of_element_located((By.XPATH, ".//div[@class='nf9vGX55']/span"))).get_attribute('class').split('_')[-1]
                #rating = review.find_element_by_xpath(".//div[@class='nf9vGX55']/span").get_attribute('class').split('_')[-1]
                review_dict['review']['rating'] = rating
            except Exception as e:
                log.error(f'Skipping review {i+1}! No Rating. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                print(f'Skipping review {i+1}! No Rating. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                print(e)
                log.error(e)
                continue

            review_dict['review']['page'] = or_page

            log.info('Get Link')
            try:
                link = review.find_element_by_xpath(".//div[@class='glasR4aX']/a").get_attribute('href')
            except:
                log.warning('No Link')
                link = None
            review_dict['review']['link'] = link

            log.info('Get Date')
            try:
                date = review.find_element_by_xpath(".//span[@class='_34Xs-BQm']").text.split(':')[-1].strip()
                date = date[:3]+date[-5:]
            except:
                log.warning('No Date')
                date = None
            review_dict['review']['date'] = date

            log.info('Get Visit Type')
            try:
                visit_type = review.find_element_by_xpath(".//span[@class='_2bVY3aT5']").text.split(' ')[-1].strip()
            except:
                log.warning('No Visit Type')
                visit_type = None
            if visit_type == 'affari':
                visit_type = 'lavoro'
            review_dict['review']['visit_type'] = visit_type

            review_dict['review']['lang'] = lang

            log.info('Get Title')
            try:
                title = review.find_element_by_xpath(".//div[@class='glasR4aX']").text
            except:
                log.warning('No Title')
                title = None
            review_dict['review']['title'] = title

            log.info('Get Like')
            try:
                like = review.find_element_by_xpath(".//span[@class='_3UnecFwl kJ7oOBi9']").text
            except:
                like = '0'
                log.info('No like for this review')
            review_dict['review']['like'] = like

            log.info('Get Text')
            try:
                text = review.find_element_by_xpath(".//q[@class='IRsGHoPm']").text
            except:
                log.warning('No Text')
                text = None
            review_dict['review']['text'] = text

            reviews_dict['reviews'].append(review_dict)

            if None in [link, date, title, like, text]:
                errors_dict['errors'].append(review_dict)

        log.info('Write Json file')
        json_write(outputfile, reviews_dict)

        log.info('Write Json None')
        json_write(errorfile, errors_dict)

        #Last Page
        if last_page is None:
            current_page = None
        else:
            current_page = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//div[@class='pageNumbers']/span[@class='pageNum current disabled']"))).text

        if last_page is None or current_page == last_page:
            log.info('Last Page of reviews')
            print('Last Page of reviews')
            break

        #Next Page
        if not old_next_page(log, driver, wait, lang, ID, url, reviews, page, n_page, or_page, current_url):
            return

    return None

