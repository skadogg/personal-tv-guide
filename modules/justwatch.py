from alive_progress import alive_bar
from classes.activity import Activity, Tvshow
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import modules.auto_sign_in
import modules.data_bin_convert
import modules.html
import modules.ld_json
import modules.runtime
import os
import random
import time

def get_titles_count(driver):
    try:
        # Reads number of titles from top of page, e.g. "887 titles," and converts to int
        logging.debug('Trying  to read number of titles')
        titles_count_str = driver.find_element(By.XPATH, '//div[@class="titles-count"]').text
        titles_count = int(titles_count_str.split(' titles')[0])
        logging.debug(f'{titles_count=}')
    except:
        logging.error('Error getting title count')
    else:
        return titles_count


def get_random_show(list):
    # Takes a random show from the list and returns the chosen show
    while True:
        r = random.randint(0, len(list) - 1)
        if list[r].activity_type == 'movie':
            return list[r]


# Movies sorted by runtime
def generate_movies_by_runtime_table(movie_list):
    # Create the HTML table string containing the list of shows sorted by runtime (shortest to longest)
    logging.debug('Generating movies by runtime table')
    data_movies_by_runtime = sorted(movie_list, key=lambda x: (x.duration))

    str_start = modules.html.generate_table_start()
    str_end = modules.html.generate_table_end()

    headers_list = ['Title', 'Runtime']
    content = modules.html.sort_by_runtime_table_header(headers_list)

    for i in range(len(data_movies_by_runtime)):
        if data_movies_by_runtime[i].activity_type == 'movie':
            shield = modules.shield.generate_shield_text(data_movies_by_runtime[i])
            runtime_str = str(data_movies_by_runtime[i].duration) if data_movies_by_runtime[i].duration != 0 else 'N/A'
            title_and_runtime_list = [shield, runtime_str]
            content += modules.html.sort_by_runtime_table_row(title_and_runtime_list)

    return str_start + content + str_end


def balance_movie_and_tv_lists(movie_list, tv_list, good_ratio=0.8):
    # Takes two show lists and returns a more balanced list
    # Currently based on number of titles
    # TODO: Create comparison by runtime
    logging.debug(f'{str(len(movie_list))=}')
    logging.debug(f'{str(len(tv_list))=}')
    if len(movie_list) > len(tv_list):
        bigger_list = movie_list
        smaller_list = tv_list
    else:
        bigger_list = tv_list
        smaller_list = movie_list

    # smaller_list_no_episode_info = []
    # for i in range(len(smaller_list)):

    while (len(smaller_list) / len(bigger_list) < good_ratio):
        smaller_list = smaller_list + smaller_list
        logging.debug(f'{len(smaller_list)=}')

    return bigger_list + smaller_list


def scrape_justwatch(url):
    # Scrape your data from JustWatch.
    if '/tv-show/' in url or 'content_type=show' in url or '/tv-show-tracking' in url:
        media = 'tv'
    else:
        media = 'movies'
    
    logging.debug(f'{media=}')
    load_dotenv(dotenv_path='./.env')

    dev_mode = os.environ.get('DEV_MODE').lower() == 'true'

    # Create webdriver instance to connect to site
    driver = open_site_conn()    
    driver.get(url)

    # Scroll to the end of the page
    logging.debug('Scrolling to bottom of page')
    scroll_down(driver)

    show_card_data = get_show_card_data(driver, media)

    if dev_mode:
        dev_items = 5
        logging.debug('Dev mode: only looking at first dev_items items in list')
        show_card_data = show_card_data[0:dev_items]

    '''
    show_card_data = [['/us/movie/oppenheimer', "Oppenheimer (2023)\nThe story of J. Robert Oppenheimer's role in the development of the atomic bomb during World War II.\n8.4\n29 offers available"], ['/us/movie/killers-of-the-flower-moon', 'Killers of the Flower Moon (2023)\nWhen oil is discovered in 1920s Oklahoma under Osage Nation land, the Osage people are murdered one by one—until the FBI steps in to unravel the mystery.\n7.7\nWatch now'], ['/us/movie/everything-everywhere-all-at-once', "Everything Everywhere All at Once (2022)\nAn aging Chinese immigrant is swept up in an insane adventure, where she alone can save what's important to her by connecting with the lives she could have led in other universes.\n7.8\nWatch now"], ['/us/movie/asteroid-city', 'Asteroid City (2023)\nIn an American desert town circa 1955, the itinerary of a Junior Stargazer/Space Cadet convention is spectacularly disrupted by world-changing events.\n6.5\nWatch now'], ['/us/movie/dumb-money', "Dumb Money (2023)\nDavid vs. Goliath tale about everyday people who flipped the script on Wall Street and got rich by turning GameStop (the video game store) into the world's hottest company.\n6.9\nWatch now"]]
    show_card_data = [['/us/tv-show/scrubs', 'TV\nScrubs\nS6 E5\n+17\nMy Friend with Money\nWatch now'], ['/us/tv-show/love-on-the-spectrum-u-s', 'TV\nLove on the Spectrum U.S.\nS2 E2\n+5\nSeason 2\nWatch now']]
    '''
    
    # Compare new show_card_data to stored data
    shows_already_in_db, shows_not_in_db = split_show_card_data(show_card_data)
    
    # >>> shows_already_in_db
    # [['/us/tv-show/scott-pilgrim-the-anime', 'TV\nScott Pilgrim Takes Off\nS1 E4\n+4\nWhatever\nWatch now'], ['/us/tv-show/the-blacklist', 'TV\nThe Blacklist\nS7 E12\n+7\nCornelius Ruck\nWatch now']]
    # >>> shows_not_in_db
    # [['/us/tv-show/one-day-at-a-time-2016', 'TV\nOne Day at a Time\nS2 E3\n+10\nTo Zir, With Love\nWatch now'], ['/us/tv-show/kath-and-kim', 'TV\nKath & Kim\nS1 E2\n+6\nGay\nWatch now'], ['/us/tv-show/wizards-of-waverly-place', "TV\nWizards of Waverly Place\nS1 E19\n+2\nAlex's Spring Fling\nWatch now"]]
    
    # Update TV episode data
    if media == 'tv':
        update_episode_data(shows_already_in_db)
        
    # Keep shows that do not yet exist
    show_card_data = shows_not_in_db

    activity_list = []
    with alive_bar(len(show_card_data), spinner='waves', bar='squares') as bar:
        for i in range(len(show_card_data)):
            reset_every_x_iterations = 25
            if (i + 1) % reset_every_x_iterations == 0:
                driver = reset_site_conn(driver)
            
            this_show_url = 'https://www.justwatch.com' + show_card_data[i][0]
            # print(f"{this_show_url=}")
            logging.debug(this_show_url)
            bar.text = this_show_url
            bar()

            if media == 'tv':
                episode_number, episode_left_in_season = parse_show_card_string(show_card_data[i])

            try:
                # Get year, media type, age rating, and synopsis quickly from ld-json data
                logging.debug('Trying to read ld_json metadata')
                show_ld_json_data = modules.ld_json.get_ld_json(this_show_url)
            except Exception as e:
                print('Error getting data for ' + this_show_url + '. Skipping...')
                logging.error(f'{this_show_url=}')
                continue

            try:
                # Visit each page to get genres and runtimes
                driver.get(this_show_url)
                time.sleep(.5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                try:
                    logging.debug('Trying to read text data from show page')
                    elem = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="title-info title-info"]'))
                    )
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    title_info = driver.find_element(By.XPATH, '//div[@class="title-info title-info"]')
                    detail_infos = title_info.find_elements(By.XPATH,'//div[@class="detail-infos"]')
                except:
                    logging.error('Error reading text data from show page')
                    continue

                # Loop through each section on the page to get headings and text
                logging.debug('Looping through each section on the page to get headings and text')
                title_info_heading = []
                title_info_value = []
                shows_dict = []
                for k in range(len(detail_infos)):
                    text = detail_infos[k].text
                    if len(text) > 0:
                        text_split = text.split(sep='\n')
                        split_head = text_split[0]
                        split_value = text_split[1]
                        title_info_heading.append(split_head)
                        title_info_value.append(split_value)
                        logging.debug(f'{title_info_heading[k]=}')
                        logging.debug(f'{title_info_value[k]=}')
            except Exception as e:
                print("Error getting data for " + this_show_url + " skipping...")
                continue

            shows_dict = dict(zip(title_info_heading, title_info_value))
            show_genres = shows_dict.get('GENRES').split(', ')
            logging.debug('Appending to show_genres:')
            logging.debug(f'{show_genres=}')
            show_runtime = shows_dict.get('RUNTIME')
            logging.debug('Appending to show_runtime:')
            logging.debug(f'{show_runtime=}')
            
            show_name = show_ld_json_data['name']

            date_created = str(show_ld_json_data['dateCreated'])
            # print(date_created)
            year = int(date_created.split('-')[0])

            show_age_rating = show_ld_json_data['contentRating']
            synopsis = show_ld_json_data['description']
            
            if media == 'tv':
                season_data = (show_ld_json_data['containsSeason'])
            logging.debug('Appending season_data')

            show_runtime_minutes = Activity.runtime_to_minutes(show_runtime, round_up=False)
            if media == 'movies':
                activity_list.append(
                    Activity(activity_type='movie', activity_name=show_name, year=year, age_rating=show_age_rating,
                             duration=show_runtime_minutes, source_url=this_show_url, categories=show_genres,
                             description=synopsis))
            else:
                activity_list.append(
                    Tvshow(activity_type='tv', activity_name=show_name, year=year, age_rating=show_age_rating,
                           duration=show_runtime_minutes, source_url=this_show_url, categories=show_genres,
                           description=synopsis, next_episode=episode_number, left_in_season=episode_left_in_season,
                           season_data=season_data))

    # TODO: quit whenever there's a large exception?
    driver.close()
    driver.quit()

    logging.debug('Closing main window')

    # Put newly-collected show data into main database
    show_db = modules.data_bin_convert.bin_to_data('./my_data/saved_data.bin')
    show_db += activity_list

    # Save my work
    modules.data_bin_convert.data_to_bin(show_db, './my_data/saved_data.bin')


def scroll_down(driver):
    # https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpagew
    # A method for scrolling the page.
    last_height = driver.execute_script("return document.body.scrollHeight")
    with alive_bar(None, spinner='waves', bar='squares') as bar:
        while True:
            bar.text = 'Scrolling down'
            bar()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


def get_show_card_data(driver, media):
    # Get name, episode number/title, left in season, main show link from main watchlist
    logging.debug('Getting all show cards from main page')
    if media == 'movies':
        show_cards = driver.find_elements(By.XPATH, '//div[@class="title-card-basic title-card-basic"]')
    else:
        show_cards = driver.find_elements(By.XPATH, '//div[@class="title-card-basic title-card-show-episode"]')

    logging.debug('Getting all show links from each card')
    show_card_data = []
    for i in range(len(show_cards)):
        show_card_main_link = show_cards[i].find_elements(By.TAG_NAME, 'a')[0].get_dom_attribute('href')
        show_card_full_text = show_cards[i].text
        show_card_data.append([show_card_main_link, show_card_full_text])

    return show_card_data


def reset_site_conn(driver):
    # Close window
    driver.close()
    driver.quit()
    
    # Open new window
    return open_site_conn()


def open_site_conn():
    options = webdriver.ChromeOptions()

    # Run the browser in the background without opening a new window
    options.add_argument("--headless=new")
    
    # this will disable image loading
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--no-sandbox')
    
    # Open main window
    logging.debug('Opening main window (headless by default)')
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    
    driver.get('https://www.justwatch.com/')
    
    driver.maximize_window()
    # # driver.implicitly_driwait(1.0)
    # # main_window_handle = driver.window_handles[0]

    # Handle privacy modal
    modules.auto_sign_in.click_through_privacy_model(driver)
    
    # Sign in to JustWatch using stored credentials (my_data/secret_login.bin)
    logging.debug('Signing in')
    modules.auto_sign_in.sign_in(driver)
    
    return driver


def update_episode_data(shows_already_in_db):
    # Update TV episode data
    show_db = modules.data_bin_convert.bin_to_data('./my_data/saved_data.bin')
    for i in range(len(shows_already_in_db)):
        match_found = False
        slug = shows_already_in_db[i][0]
        for j in range(len(show_db)):
            if slug in show_db[j].source_url:
                match_found = True
                episode_number, episode_left_in_season = parse_show_card_string(shows_already_in_db[i])
                logging.debug(f"Updating episode info: {slug=}")
                show_db[j].next_episode = episode_number
                show_db[j].left_in_season = episode_left_in_season
                break
        if match_found:
            continue
    modules.data_bin_convert.data_to_bin(show_db, './my_data/saved_data.bin')


def parse_show_card_string(show_card):
    # Takes show_card
    # ['/us/tv-show/love-on-the-spectrum-u-s', 'TV\nLove on the Spectrum U.S.\nS2 E2\n+5\nSeason 2\nWatch now']
    # and returns episode info
    # ('S2 E2', 5)
    this_show_elements = show_card[1].split(sep='\n')
    episode_number = this_show_elements[2]
    logging.debug(f'{episode_number=}')
    if this_show_elements[3][0] == "+":
        episode_left_in_season = int(this_show_elements[3].split('+')[1])
    else:
        episode_left_in_season = 0
    
    return episode_number, episode_left_in_season


def split_show_card_data(show_card_data):
    # Compare new show_card_data to stored data
    show_db = modules.data_bin_convert.bin_to_data('./my_data/saved_data.bin')
    shows_already_in_db = []
    shows_not_in_db = []
    i = 0
    for i in range(len(show_card_data)):  # TODO: show some kind of progress while comparing
        show_exists = False
        slug = show_card_data[i][0]
        for j in range(len(show_db)):
            if slug in show_db[j].source_url:
                show_exists = True
                break
        if show_exists:
            shows_already_in_db.append(show_card_data[i])
        else:
            shows_not_in_db.append(show_card_data[i])
    return shows_already_in_db, shows_not_in_db

def remove_already_seen(url):
    driver = open_site_conn()
    
    # Read show_card_data from site
    driver.get(url)
    show_card_data = get_show_card_data(driver, 'movies')
    
    # Look in main db for matches and remove from db
    logging.info("Removing already seen from db")
    show_db = modules.data_bin_convert.bin_to_data('./my_data/saved_data.bin')
    for i in range(len(show_card_data)):
        slug = show_card_data[i][0]
        # print(slug)
        for j in range(len(show_db)):
            if slug in show_db[j].source_url:
                logging.info(f"Removing: {show_db[j].activity_name=}")
                # print(show_db[j].activity_name)
                show_db.pop(j)
                j -= 1
                break
    modules.data_bin_convert.data_to_bin(show_db, './my_data/saved_data.bin')


def remove_manually_by_url(url):    
    # Look in main db for matches and remove from db
    logging.info(f"Removing from db: {url=}")
    show_db = modules.data_bin_convert.bin_to_data('./my_data/saved_data.bin')
    for j in range(len(show_db)):
        if url == show_db[j].source_url:
            logging.info(f"Removing: {show_db[j].activity_name=}")
            # print(show_db[j].activity_name)
            show_db.pop(j)
            j -= 1
            break
    modules.data_bin_convert.data_to_bin(show_db, './my_data/saved_data.bin')


def remove_manually_by_percentage(pct):    
    # Remove oldest pct% of shows from db
    logging.info(f"Removing from db: {pct=}")
    show_db = modules.data_bin_convert.bin_to_data('./my_data/saved_data.bin')
    
    num_shows = len(show_db)
    num_to_remove = int(num_shows * (pct / 100))
    show_db = show_db[num_to_remove:num_shows]
    
    modules.data_bin_convert.data_to_bin(show_db, './my_data/saved_data.bin')
