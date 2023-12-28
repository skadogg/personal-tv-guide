from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Open main window
driver = webdriver.Chrome()

driver.get('https://www.goodreads.com/review/list/40036106-wes?ref=nav_mybooks&shelf=currently-reading')

driver.maximize_window()


# Read books in the list
book_cards = driver.find_elements(By.XPATH, '//tr[@class="bookalike review"]')

book_info_list = []
for i in range(len(book_cards)):
    book = book_cards[i]
    book_card_text = book.text.split('\n')
    title = book_card_text[0]
    author = book_card_text[1]
    rating = book_card_text[2]
    date_added_to_shelf = book_card_text[10]
    link = "https://www.goodreads.com" + book.find_element(By.TAG_NAME, "a").get_dom_attribute('href')
    book_info_list.append([title,author,rating,date_added_to_shelf,link])

book_info_list
# [['  The Ruthless Elimination of Hurry: How to Stay Emotionally Healthy and Spiritually Alive in the Chaos of the Modern World', 'Comer, John Mark *', '4.53', 'Oct 01, 2023', 'https://www.goodreads.com/book/show/43982455-the-ruthless-elimination-of-hurry'], ['  Feeling Good: The New Mood Therapy', 'Burns, David D.', '4.05', 'Aug 12, 2023', 'https://www.goodreads.com/book/show/46674.Feeling_Good'], ['  Dress Your Family in Corduroy and Denim', 'Sedaris, David', '4.11', 'Aug 12, 2023', 'https://www.goodreads.com/book/show/10176.Dress_Your_Family_in_Corduroy_and_Denim'], ["  Madrigal's Magic Key to Spanish", 'Madrigal, Margarita', '4.26', 'May 28, 2023', 'https://www.goodreads.com/book/show/4322506-madrigal-s-magic-key-to-spanish'], ['  Crouching Buzzard, Leaping Loon (Meg Langslow, #4)', 'Andrews, Donna *', '4.07', 'Apr 28, 2023', 'https://www.goodreads.com/book/show/615406.Crouching_Buzzard_Leaping_Loon'], ['  Sink Reflections: Overwhelmed? Disorganized? Living in Chaos? Discover the Secrets That Have Changed the Lives of More Than Half a Million Families...', 'Cilley, Marla', '4.05', 'Dec 11, 2022', 'https://www.goodreads.com/book/show/350258.Sink_Reflections']]

driver.quit()
