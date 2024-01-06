from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import modules.html
import modules.runtime

def get_titles_count(driver):
    try:
        # Reads number of titles from top of page, e.g. "887 titles," and converts to int
        titles_count_str = driver.find_element(By.XPATH, '//div[@class="titles-count"]').text
        titles_count = int(titles_count_str.split(' titles')[0])
    except:
        print("Error getting title count")
    else:
        return titles_count


def get_random_show(list):
    # Takes a random show from the list and returns the chosen show
    r = random.randint(0,len(list))
    return list[r]


# Movies sorted by runtime
def generate_movies_by_runtime_table(movie_list):
    # Create the HTML table string containing the list of shows sorted by runtime (shortest to longest)
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