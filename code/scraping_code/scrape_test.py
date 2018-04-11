import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3
from os.path import expanduser
import os
import codecs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.chdir('/Users/chrispaul/Desktop/wordplay/wordplay/scraping_code')

driver = webdriver.Chrome('/Users/chrispaul/Desktop/chromedriver')  # Optional argument, if not specified will search path.
# or, fill in your ANACONDA_INSTALL_DIR and try this:
# driver = webdriver.Chrome('ANACONDA_INSTALL_DIR/chromedriver-Darwin')

driver.get('https://genius.com')

time.sleep(2)

#signing into venmo

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/search-form/form/input"))
    )
except:
    driver.quit()

search = driver.find_element_by_xpath('/html/body/div[1]/search-form/form/input')

search.send_keys("Shape of You Ed Sheeran")
search.submit()

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a/div[2]'))
    )

# time.sleep(10)
#
toplink = driver.find_element_by_xpath('/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a/div[2]')

toplink.click()

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div/defer-compile[1]/lyrics/div/section'))
    )

lyrics = driver.find_element_by_xpath('/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div/defer-compile[1]/lyrics/div/section')
lyrics_text = lyrics.text

print(lyrics_text)

# time.sleep(5)
#
# coderequest = driver.find_element_by_class_name('ladda-label')
# coderequest.submit()
#
# time.sleep(15)
#
# connection = _new_connection()
# c = connection.cursor()
#
# # The `handle` table stores all known recipients.
# c.execute("SELECT text FROM `message`")
# texts = c.fetchall()
#
# connection.close()
#
# texts = texts[-5:]
#
# for i in range(1,6):
#     if u'Venmo' in texts[-i][0]:
#         code = texts[-i][0].split(u' ')[-1]
#         print code
#         break
#
# codeverification = driver.find_element_by_class_name('auth-form-input')
#
# codeverification.send_keys(code)
# codeverification.submit()
#
# time.sleep(2)
#
# NotNow = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/form/div/button[2]/span[1]')
# NotNow.click()
#
# time.sleep(5)
#
# print "\a"
#
# friends = driver.find_element_by_xpath('//*[@id="inc_right_side"]/div[3]/div[1]/div[1]/a')
# friends.click()
#
# time.sleep(2)
#
# # friends lists scraping
#
# friends_list_URL = driver.current_url
#
# friends = driver.find_elements_by_class_name("profile52")
#
# NUMBER_OF_FRIENDS = len(friends)
#
# full1 = '//*[@id="app"]/div/div[2]/div/div/table/tbody/tr['
# full2 = ']/td[1]/a/div'
#
# sentences = []
# dates = []
# peoples = []
#
# for ii in range(1,NUMBER_OF_FRIENDS + 1):
#
#     if ii not in [3, 18, 23]: # friends not in MSAN
#
#         xpath = full1 + str(ii) + full2
#
#         print xpath
#
#         driver.find_element_by_xpath(xpath).click()
#
#         time.sleep(5)
#
#         try:
#             more_button = driver.find_element_by_xpath('//*[@id="profile_feed_MORE_BUTTON"]/a')
#
#             for i in range(0,50):
#                 time.sleep(0.5)
#                 try:
#                     more_button.click()
#                 except:
#                     break
#         except:
#             print "bummer"
#
#         date = driver.find_elements_by_xpath("//a[contains(@class,'gray_link')]")
#         people = driver.find_elements_by_xpath("//div[contains(@data-story-class,'profile_feed_story')]")
#         transaction_descr = driver.find_elements_by_xpath("//div[contains(@style,'word-wrap:break-word')]")
#
#         for i in people:
#             value = i.text
#             #value = value.replace(u",", u"")
#             #print value
#             peoples.append(value)
#
#         for i in transaction_descr:
#             value = i.text
#             #value = value.replace(u",", u"")
#             #print value
#             sentences.append(value)
#
#         for i in date:
#             value = i.text
#             #value = value.replace(u",", u"")
#             #print value
#             #print 'tried'
#             dates.append(value)
#
#         driver.get(friends_list_URL)
#
#         time.sleep(3)
#
#
# print sentences
# print dates
# print peoples
#
# f = open('/tmp/venmosentences3.csv', 'w+')
# for i in range(0, len(sentences)):
#     f.write(peoples[i].encode('utf8') + u', ' + sentences[i].encode('utf8') + u', ' + dates[i].encode('utf8'))
#     f.write('\n'.encode('utf8'))
# f.close
#
#
# # here is where some useful work would typically happen
#
# #raw_input("Press Enter to quit")
# #driver.quit() # close browser
#
