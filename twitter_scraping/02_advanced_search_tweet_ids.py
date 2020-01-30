from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import json
import datetime
import os

# Search variables.
all_words = ''
phrase = ''
any_words = ''
no_words = ''
hastags = 'cancelnetflix'
language = 'en'
from_user = ''
to_user = ''
mentioning = ''
start = datetime.datetime(2019, 12, 11)  # yyyy, m, d
end = datetime.datetime(2019, 12, 31)  # yyyy, m, d
retweets = True

# Only edit these if you're having problems.
delay = 2  # time to wait on each page load before reading the page
chrome_options = webdriver.chrome.options.Options()
chrome_options.add_argument('--user-data-dir=chrome-data')
# options are Chrome() Firefox() Safari()
driver = webdriver.Chrome(options=chrome_options)
# Remote webdiving option.
# desiredCapabilities = DesiredCapabilities.CHROME.copy()
# driver = webdriver.Remote(desired_capabilities=desiredCapabilities,
#                           command_executor='http://127.0.0.1:4444/wd/hub')

# Don't mess with this stuff.
twitter_ids_filename = 'all_tweet_ids'
days = (end - start).days + 1
id_selector = '.time a.tweet-timestamp'
tweet_selector = 'li.js-stream-item'
ids = set([])


def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)
                                         ) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])


def form_url(hastags='', language='', mentioning='', since='', until='', retweets=False):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q='
    if hastags != '':
        hastags = '(%23' + hastags + ')'
    if language != '':
        language = '%20lang%3A' + language
    if mentioning != '':
        mentioning = '(%40' + mentioning + ')'
    if retweets:
        retweets = 'include%3Aretweets'
    else:
        retweets = ''
    since = '%20since%3A' + since
    until = '%20until%3A' + until
    p2 = hastags + mentioning + since + until + retweets + '&src=typd'
    return p1 + p2


def increment_day(date, i):
    return date + datetime.timedelta(days=i)


for day in range(days):
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 1))
    url = form_url(hastags, language, mentioning, d1, d2, retweets)
    print(url)
    print(d1)
    driver.get(url)
    # Continue session.
    # cookies = pickle.load(open('cookies.pkl', 'rb'))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    sleep(delay)

    try:
        found_tweets = driver.find_elements_by_css_selector(tweet_selector)
        iteration = 1
        increment = 10

        while len(found_tweets) >= iteration * increment:
            print(str(iteration) +
                  '. scrolling down to load more tweets')
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            sleep(delay)
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)

            for tweet in found_tweets:
                try:
                    id = tweet.find_element_by_css_selector(
                        id_selector).get_attribute('href').split('/')[-1]
                    ids.add(id)
                except StaleElementReferenceException:
                    print('lost element reference', tweet)

            # The data is saved into two files to prevent file corruption when
            # the program is terminated early.
            filename = twitter_ids_filename + \
                str(iteration % 2) + '.json'

            try:
                with open(filename) as f:
                    all_ids = list(ids) + json.load(f)
                    data_to_write = list(set(all_ids))
                    print('tweets found:', len(ids))
                    print('tweets in file: ', len(data_to_write))
            except FileNotFoundError:
                with open(filename, 'w') as f:
                    all_ids = ids
                    data_to_write = list(set(all_ids))
                    print('tweets found:', len(ids))
                    print('tweets in file: ', len(data_to_write))

            with open(filename, 'w') as outfile:
                json.dump(data_to_write, outfile)

            # Saves surrent session.
            # pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))

            iteration += 1

    except NoSuchElementException:
        print('no tweets on this day')

    start = increment_day(start, 1)

# Write final output.
with open(twitter_ids_filename + '0.json') as f:
    data0 = json.load(f)
    count0 = len(data0)
with open(twitter_ids_filename + '1.json') as f:
    data1 = json.load(f)
    count1 = len(data0)
with open(twitter_ids_filename + '.json', 'w') as finaloutput:
    if count0 > count1:
        json.dump(data0, finaloutput)
    else:
        json.dump(data1, finaloutput)

# Cleanup.
os.remove(twitter_ids_filename + '0.json')
os.remove(twitter_ids_filename + '1.json')

print('all done.')
driver.close()
