from alive_progress import alive_bar
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import modules.html
import modules.runtime
import modules.ld_json
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
    r = random.randint(0,len(list))
    return list[r]


# Movies sorted by runtime
def generate_movies_by_runtime_table(movie_list):
    # Create the HTML table string containing the list of shows sorted by runtime (shortest to longest)
    logging.debug('Generating movies by runtime table')
    data_movies_by_runtime = sorted(movie_list,key=lambda x:(modules.runtime.runtime_to_minutes(x[5],False)))

    str_start = modules.html.generate_table_start()
    str_end = modules.html.generate_table_end()

    headers_list = ['Title','Runtime']
    content = modules.html.sort_by_runtime_table_header(headers_list)

    for i in range(len(data_movies_by_runtime)):
        shield = modules.shield.generate_shield(data_movies_by_runtime[i])
        runtime_str = str(modules.runtime.runtime_to_minutes(data_movies_by_runtime[i][5],False))
        title_and_runtime_list = [shield,runtime_str]
        content += modules.html.sort_by_runtime_table_row(title_and_runtime_list)

    return str_start + content + str_end


def balance_movie_and_tv_lists(movie_list, tv_list, good_ratio = 0.8):
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
        
    while(len(smaller_list) / len(bigger_list) < good_ratio):
        smaller_list = smaller_list + smaller_list
        logging.debug(f'{len(smaller_list)=}')
    
    return bigger_list + smaller_list


def scrape_justwatch(media):
    # Scrape your data from JustWatch.
    # media should be either 'tv' or 'movies'
    import modules.auto_sign_in
    
    media = media.lower()
    logging.debug(f'{media=}')
    load_dotenv(dotenv_path='./my_data/.env')

    dev_mode = os.environ.get('DEV_MODE').lower() == 'true'

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
    
    if media == 'movies':
        driver.get('https://www.justwatch.com/us/lists/my-lists?content_type=movie&sort_by=popular_30_day')
    else:
        driver.get('https://www.justwatch.com/us/lists/tv-show-tracking?inner_tab=continue_watching')

    driver.maximize_window()
    # driver.implicitly_driwait(1.0)
    # main_window_handle = driver.window_handles[0]


    # Sign in to JustWatch using stored credentials (my_data/secret_login.bin)
    logging.debug('Signing in')
    modules.auto_sign_in.sign_in(driver)

    # Scroll to the end of the page
    logging.debug('Scrolling to bottom of page')
    items_in_list = get_titles_count(driver)
    if dev_mode:
        items_in_list = 5
    pages = (items_in_list // 20) + 1
    i = 0
    with alive_bar(pages, spinner='waves', bar='squares') as bar:
        for i in range(pages):
            bar()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(.5)


    # Get name, episode number/title, left in season, main show link from main watchlist
    logging.debug('Getting all show cards from main page')
    if media == 'movies':
        show_cards = driver.find_elements(By.XPATH, '//div[@class="title-card-basic title-card-basic"]')
    else:
        show_cards = driver.find_elements(By.XPATH, '//div[@class="title-card-basic title-card-show-episode"]')

    if dev_mode:
        dev_items = 10
        logging.debug('Dev mode: only looking at first dev_items items in list')
        show_cards = show_cards[0:dev_items]

    logging.debug('Getting all show links from each card')
    i = 0
    show_card_all_links = []
    show_card_full_text = []
    for i in range(len(show_cards)):
        show_card_all_links.append(show_cards[i].find_elements(By.TAG_NAME,'a'))
        show_card_full_text.append(show_cards[i].text)

    i = 0
    show_main_link = []
    for i in range(len(show_card_all_links)):
        show_main_link.append(show_card_all_links[i][0].get_dom_attribute('href'))
        logging.debug(f'{show_main_link[i]=}')

    i = 0
    show_name = []
    episode_number = []
    episode_left_in_season = []
    episode_title = []
    for i in range(len(show_card_full_text)):
        this_show_elements = show_card_full_text[i].split(sep='\n')
        if media == 'movies':
            show_name.append(this_show_elements[0])
            logging.debug(f'{show_name[i]=}')
            episode_number.append('')
            episode_left_in_season.append('')
            episode_title.append('')
        else:
            show_name.append(this_show_elements[1])
            logging.debug(f'{show_name[i]=}')
            episode_number.append(this_show_elements[2])
            logging.debug(f'{episode_number[i]=}')
            if this_show_elements[3][0] == "+":
                episode_left_in_season.append(this_show_elements[3])
                episode_title.append(this_show_elements[4])
            else:
                episode_left_in_season.append('')
                episode_title.append(this_show_elements[3])


    # Get genres, runtime, age rating from show pages
    j = 0
    show_genres = []
    show_runtime = []
    show_age_rating = []
    year = []
    media_type = []
    synopsis = []
    season_data = []
    with alive_bar(len(show_main_link), spinner='waves', bar='squares') as bar:
        for j in range(len(show_main_link)):
            logging.debug(show_main_link)
            bar.text = show_main_link[j]
            bar()
            
            full_url = 'https://www.justwatch.com' + show_main_link[j]
            
            try:
                # Get year, media type, age rating, and synopsis quickly from ld-json data
                logging.debug('Trying to read ld_json metadata')
                show_ld_json_data = modules.ld_json.get_ld_json(full_url)
            except Exception as e:
                print('Error getting data for ' + show_main_link[j] + '. Skipping...')
                logging.error(f'{show_main_link[j]=}')
                continue
            
            try:
                # Visit each page to get genres and runtimes
                driver.get(full_url)
                try:
                    logging.debug('Trying to read text data from show page')
                    elem = WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="title-info title-info"]'))
                    )
                except:
                    logging.error('Error reading text data from show page')
                finally:
                    time.sleep(.5)

                title_info = driver.find_element(By.XPATH, '//div[@class="title-info title-info"]')
                detail_infos = title_info.find_elements(By.XPATH,'//div[@class="detail-infos"]')

                # Loop through each section on the page to get headings and text
                logging.debug('Looping through each section on the page to get headings and text')
                k = 0
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
                print("Error getting data for " + show_main_link[j] + " skipping...")
                continue
            
            shows_dict = dict(zip(title_info_heading,title_info_value))
            show_genres.append(shows_dict.get('GENRES'))
            logging.debug('Appending to show_genres:')
            logging.debug(f'{show_genres[j]=}')
            show_runtime.append(shows_dict.get('RUNTIME'))
            logging.debug('Appending to show_runtime:')
            logging.debug(f'{show_runtime[j]=}')
            # show_age_rating.append(shows_dict.get('AGE RATING'))

            year.append(str(show_ld_json_data['dateCreated']).split('-')[0])
            media_type.append(show_ld_json_data['@type'])
            show_age_rating.append(show_ld_json_data['contentRating'])
            synopsis.append(show_ld_json_data['description'])
            if media == 'movies':
                season_data.append('')
            else:
                season_data.append(show_ld_json_data['containsSeason'])
                logging.debug('Appending season_data')


    # driver.close()
    driver.quit()
    logging.debug('Closing main window')


    # Pull elements together
    logging.debug('Pulling it all together into one list')
    data_list_everything = list(zip(show_name,episode_number,episode_left_in_season,episode_title,show_genres,show_runtime,show_age_rating,show_main_link,year,media_type,synopsis,season_data))
    # sorted(data_list_everything)

    # df = pd.DataFrame(data_list_everything, columns=['Show Name','Episode Number','Episodes Remaining','Episode Title','Genres','Runtime','Age Rating'])
    # html_string = df.to_html()


    # Save my work
    import modules.data_bin_convert
    if media == 'movies':
        modules.data_bin_convert.data_to_bin(data_list_everything, './my_data/saved_data_movies.bin')
    else:
        modules.data_bin_convert.data_to_bin(data_list_everything, './my_data/saved_data_tv.bin')
    # data_list_everything = modules.data_bin_convert.bin_to_data()
