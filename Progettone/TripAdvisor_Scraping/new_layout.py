from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
import time
import re
from json_lib import *
from word_dict import *


def new_get_info(log, driver, poi_dict, wait):
    check_error = 0
    log.info('Get Ranking')
    try:
        ranking_elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_28X3NMFC'][2]//div")))
        ranking = ranking_elem.text.split()[0][1:]
    except:
        log.error('No Ranking')
        print('No Ranking')
        ranking = None
    poi_dict['ranking'] = ranking

    log.info('Get Categories')
    try:
        categories_elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH,"//div[@class='_28X3NMFC'][3]/div")))
        categories = [x.strip() for x in categories_elem.text.split('\u2022')]
    except:
        log.error('No Categories')
        print('No Categories')
        categories = None
    poi_dict['categories'] = categories

    log.info('Get Address')
    try:
        address_elem = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH,"//div[@class='_2Xkb5A8Y']/following::span[1]")))
        address = address_elem.text
    except:
        log.error('No Address')
        print('No Address')
        address = None
    poi_dict['address'] = address

    log.info('Get Duration')
    try:
        duration_elem = driver.find_element_by_xpath("//div[@class='lyGV4Xx2']/following::div[1]")
        duration = duration_elem.text.split('\n')[1]
    except:
        log.warning('No Suggested Duration')
        duration = None
    poi_dict['duration'] = duration

    log.info('Get Getting There')
    try:
        getting_there_elem = driver.find_elements_by_xpath("//div[@class='_3Ev4pJxb']//li")
        getting_there = [x.text for x in getting_there_elem]
    except:
        getting_there = None
        log.warning('No Getting There')
    poi_dict['getting_there'] = getting_there

    log.info('Get Mentions')
    try:
        mentions_elem = driver.find_elements_by_xpath("//div[@class='_13nAUAiT']/div[3]//span//span")
        mentions = [x.text for x in mentions_elem if x.text != '']
    except:
        mentions = None
        log.warning('No Mentions')
    poi_dict['mentions'] = mentions

    if None in [ranking, categories, address]:
        check_error = 1
    return poi_dict, check_error


def new_init_check(log, driver, wait, lang, click_on_lang=True):
    log.info('Get Initial Reviews for language click')
    try:
        #reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_2rspOqPP']/div")))[:-1]
        reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_2nBYkPk3']")))
    except Exception as e:
        log.error('No initial Reviews found: Skipping!')
        print('No initial Reviews found: Skipping!')
        print(e)
        log.error(e)
        reviews = None
        return 0

    try:
        lang_menu = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//div[@class='KzNv-W1S']//button")))
    except Exception as e:
        log.error(f'Error in language menu: Skipping!')
        print(f'Error in language menu: Skipping!')
        print(e)
        log.error(e)
        return 0

    if lang_menu.text.strip() == lang:
        log.info(f'Language: {lang} is already selected')
        print(f'Language: {lang} is already selected')
    elif click_on_lang:
        try:
            lang_menu.click()
            lang_element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, f"//span[contains(@id, 'menu-item')]/span[text()='{lang}']")))
            log.info(f'Language: {lang} click')
            print(f'Language: {lang} click')
            try:
                lang_element.click()
                for review in reviews:
                    WebDriverWait(driver, wait).until(staleness_of(review))
            except Exception as e:
                log.error('Page not correctly loaded after language click: Skipping!')
                print('Page not correctly loaded after language click; Skipping!')
                print(e)
                log.error(e)
                return 0
        except Exception as e:
            log.error(f'Language menu click or {lang} not present: Skipping!')
            print(f'Language menu click or {lang} not present: Skipping!')
            print(e)
            log.error(e)
            return 0
    else:
        log.error(f'Language {lang} not preserved after force loading next page: Skipping!')
        print(f'Language {lang} not preserved after force loading next page: Skipping!')
        return 0
    return 1


def new_next_page(log, driver, wait, lang, ID, url, reviews, page, n_page, or_page, current_url):
    old_url = current_url
    need_next_page = False

    try:
        # next_page = driver.find_element_by_xpath("//div[@class='_1I73Kb0a']/div[@class='_3djM0GaD']")
        next_page = WebDriverWait(driver, wait).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_1I73Kb0a']/div[@class='_3djM0GaD']")))
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
        if not new_init_check(log, driver, wait, lang, click_on_lang=False):
            log.error(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
            print(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
            return 0
    return 1


def new_get_reviews(log, outputfile, errorfile, ID, url, driver, wait, reviews_dict, errors_dict, lang, dot):
    # Reviews
    log.info('Start scraping Reviews')
    n_page = 0

    if not new_init_check(log, driver, wait, lang):
        return

    log.info('Get last page number')
    try:
        last_page = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1w5PB8Rk'][last()]"))).text
    except:
        last_page = None
        log.error('Last Page not found! Assuming only 1 page of reviews')
        print('Last Page not found! Assuming only 1 page of reviews')

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
            #reviews = driver.find_elements_by_xpath("//div[@class='_2rspOqPP']/div")[:-1]
            #reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_2rspOqPP']/div")))[:-1]
            reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_2nBYkPk3']")))
        except Exception as e:
            log.error(f'Skipping page! No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
            print(f'Skipping page! No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
            print(e)
            log.error(e)
            log.error("Trying to force same page url...")
            print("Trying to force same page url...")
            driver.get(current_url)
            if not new_init_check(log, driver, wait, lang, click_on_lang=False):
                log.error(f"Force loading same page failed: Skipping page! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                print(f"Force loading same page failed: Skipping page! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                need_next_page = True
            else:
                try:
                    reviews = WebDriverWait(driver, wait).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='_2nBYkPk3']")))
                except Exception as e:
                    log.error(f'No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                    print(f'No Reviews found. n_page: {n_page} , or_page: {or_page} , url: {current_url}')
                    print(e)
                    log.error(e)
                    need_next_page = True

            if need_next_page:
                log.error("Trying to force next page url...")
                print("Trying to force next page url...")
                next_or_page = 'or' + str(int(page) + 10)
                next_url = re.sub(f'{ID}-Reviews', f'{ID}-Reviews-{next_or_page}', url)
                driver.get(next_url)
                if not new_init_check(log, driver, wait, lang, click_on_lang=False):
                    log.error(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                    print(f"Force loading next page failed: Skipping! n_page: {n_page} , or_page: {or_page} , url: {current_url}")
                    return
                else:
                    continue

        log.info(f'Page {n_page}: {len(reviews)} reviews')
        print(f'Page {n_page}: {len(reviews)} reviews')

        for i in range(len(reviews)):
            review = reviews[i]
            review_dict = {}

            try:
                read_more = review.find_element_by_xpath("..//div[@class='_36B4Vw6t']")
                read_more.click()
                log.info('Click on Read more')
            except:
                pass

            log.info('Get User')
            try:
                user = WebDriverWait(review, wait).until(EC.presence_of_element_located((By.XPATH, "..//div[@class='_2nBYkPk3']//a"))).get_attribute('href').split('/')[-1]
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
                rating = WebDriverWait(review, wait).until(EC.presence_of_element_located((By.XPATH, "..//div[@class='_3HXgtLZQ']/following::div[1]/*['svg']"))).get_attribute('title')
                if dot == 'it':
                    rating = rating.split()[1].replace(',', '')
                elif dot == 'com':
                    rating = rating.split()[0].replace('.', '')
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
                link = review.find_element_by_xpath("..//div[@class='_3HXgtLZQ']/following-sibling::a").get_attribute('href')
            except:
                log.warning('No Link')
                link = None
            review_dict['review']['link'] = link

            log.info('Get Date and Visit Type')
            try:
                date_and_visit = review.find_element_by_xpath("..//div[@class='_3JxPDYSx']").text.split('\u2022')
                date = date_and_visit[0].strip().lower()
                month = date.split()[0]
                year = date.split()[1]
                if dot == 'it':
                    month = it_new_month_dict[month]
                if len(date_and_visit) > 1:
                    visit_type = date_and_visit[1].strip().lower()
                    if dot == 'it':
                        visit_type = it_new_type_dict[visit_type]
                    elif dot == 'com':
                        visit_type = com_new_type_dict[visit_type]
                else:
                    visit_type = None
                    log.warning('No Visit Type')
            except:
                log.warning('No Date and Visit Type')
                month = None
                year = None
                visit_type = None
            review_dict['review']['month'] = month
            review_dict['review']['year'] = year
            review_dict['review']['visit_type'] = visit_type

            review_dict['review']['lang'] = lang

            log.info('Get Title')
            try:
                title = review.find_element_by_xpath("..//div[@class='_3HXgtLZQ']/following-sibling::a").text
            except:
                log.warning('No Title')
                title = None
            review_dict['review']['title'] = title

            log.info('Get Like')
            try:
                like = review.find_element_by_xpath("..//div[@class='_2nBYkPk3']//span[@class='_37Nr884k']").text
            except:
                like = '0'
                log.info('No like for this review')
            review_dict['review']['like'] = like

            log.info('Get Text')
            try:
                text = review.find_element_by_xpath("..//div[@class='_3HXgtLZQ']/following::div[@class='_2f_ruteS _1bona3Pu']").text
            except:
                log.warning('No Text')
                text = None
            review_dict['review']['text'] = text

            reviews_dict['reviews'].append(review_dict)

            if None in [link, month, year, title, like, text]:
                errors_dict['errors'].append(review_dict)

        log.info('Write Json file')
        json_write(outputfile, reviews_dict)

        log.info('Write Json None')
        json_write(errorfile, errors_dict)

        #Last Page
        if last_page is None:
            current_page = None
        else:
            current_page = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_1w5PB8Rk']//button['disabled']"))).text

        if current_page == last_page or last_page is None:
            log.info('Last Page of reviews')
            print('Last Page of reviews')
            break

        #Next Page
        if not new_next_page(log, driver, wait, lang, ID, url, reviews, page, n_page, or_page, current_url):
            return

    return None

