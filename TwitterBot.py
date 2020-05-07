from time import sleep
import json

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

import secret


class Twitter_bot():
    '''Creates a automated message to post on our twitter line by logging in
    then sending a post to the browser'''

    def __init__(self, username, password):
        '''Sets up the browsers and maximizes the windows for consistency.'''
        self.driver = webdriver.Chrome()
        self.driver.get('https://twitter.com')
        self.driver.maximize_window()
        self.usr = username
        self.pw = password
        sleep(4)

    def log_in(self):
        '''Sends our username and password to the input fields for loging in
        and clicks "Log in" afterwards'''
        self.driver.find_element_by_xpath(
        '//input[@name="session[username_or_email]"]').send_keys(self.usr)
        self.driver.find_element_by_xpath(
        '//input[@name="session[password]"]').send_keys(self.pw)
        self.driver.find_element_by_xpath(
        '//div[@data-testid="LoginForm_Login_Button"]').click()
        sleep(4)

    def post(self, msg):
        '''Navigates to profile to post a new message'''
        self.driver.find_element_by_xpath('//div[@role="textbox"]').send_keys(msg)
        self.driver.find_element_by_xpath(
        '//div[@data-testid="tweetButtonInline"]').click()
        sleep(2)


def all_headlines():
    '''Collect all headlines from wsj as a dict of the article title and url
    link to page, and out put result to Headlines.txt as json object'''
    r = requests.get('https://www.wsj.com', headers={'User-Agent': 'Custom'})
    soup = BeautifulSoup(r.text, 'html.parser').find_all('a')
    headlines = [x for x in soup if x.get('href') != None and x.string != None and '/articles' in x.get('href')]
    headlines.sort(key=lambda x: len(x.string))
    url_link = [x.get('href') for x in headlines]
    articles = [x.string for x in headlines]
    result = dict(zip(articles, url_link))
    with open("Headlines.txt","w+") as file:
        json.dump(result, file)

def create_key_words():
    '''Looping through the headlines you can create a list of keyword seperated
    by a space, any duplicates will be removed and if no keyword is needed for
    the headline you can continue with enter.'''
    try:
        with open('Keywords.txt', 'r') as file:
            key_words = set(json.loads(file.read()))
    except json.decoder.JSONDecodeError:
        print('\nFile is empty. Creating a new keyword set.\n')
        key_words = set()
    with open('Headlines.txt','r') as file:
        headlines = json.loads(file.read())
    for k, v in headlines.items():
        print('\n' + k)
        words = input('\nWhat key words are importatnt from this article title? : => ').split(' ')
        w_filter = [x for x in words if x != '']
        if w_filter:
            key_words.update(set(w_filter))
    with open('Keywords.txt', 'w+') as file:
        json.dump(list(key_words), file)

def edit_key_words():
    '''Using the existing list of keywords, loop through each one chosing which
    to keep, which to delete, and if you want to add any'''
    pass

def twitter_post(message):
    bot = Twitter_bot(secret.TwtUsr, secret.TwtPsw)
    bot.log_in()
    bot.post(message)
    bot.driver.quit()

def wsj_headlines():
    '''Collect all headlines and filter out using our keywords in title'''
    all_headlines()

def main():
    wsj_headlines()
    # twitter_post('Test')
    create_key_words()

if __name__ == '__main__':
    main()
