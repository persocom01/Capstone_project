from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import json
import datetime

# Search variables.
all_words = ''
phrase = ''
any_words = ''
no_words = ''
hastags = ''
from_user = ''
to_user = ''
mentioning = 'jk_rowling'
start = datetime.datetime(2019, 12, 19)  # year, m, d
end = datetime.datetime(2019, 12, 19)  # yyyy, m, d

# only edit these if you're having problems
delay = 2  # time to wait on each page load before reading the page
driver = webdriver.Chrome()  # options are Chrome() Firefox() Safari()
# Commented out remote webdiving option.
# desiredCapabilities = DesiredCapabilities.CHROME.copy()
# driver = webdriver.Remote(desired_capabilities=desiredCapabilities,
#                           command_executor='http://127.0.0.1:4444/wd/hub')

# Don't mess with this stuff.
twitter_ids_filename = 'all_tweet_ids_'
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


def form_url(mentioning, since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q='
    mentioning = '(%40' + mentioning + ')'
    since = '%20since%3A' + since
    until = '%20until%3A' + until
    p2 = mentioning + since + until + 'include%3Aretweets&src=typd'
    return p1 + p2


def increment_day(date, i):
    return date + datetime.timedelta(days=i)


for day in range(days):
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 1))
    url = form_url(mentioning, d1, d2)
    print(url)
    print(d1)
    driver.get(url)
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
                    ids.append(id)
                except StaleElementReferenceException:
                    print('lost element reference', tweet)

            # The data is saved into two files to prevent file corruption.
            filename = twitter_ids_filename + \
                str(iteration % 2) + '.json'

            try:
                with open(filename) as f:
                    all_ids = list(ids) + json.load(f)
                    data_to_write = list(set(all_ids))
                    print(f'{len(ids)} tweets found')
                    print('tweets in file: ', len(data_to_write))
            except FileNotFoundError:
                with open(filename, 'w') as f:
                    all_ids = ids
                    data_to_write = list(set(all_ids))
                    print(f'{len(ids)} tweets found')
                    print('tweets in file: ', len(data_to_write))

            with open(filename, 'w') as outfile:
                json.dump(data_to_write, outfile)
            iteration += 1

    except NoSuchElementException:
        print('no tweets on this day')

    start = increment_day(start, 1)


print('all done here')
driver.close()
