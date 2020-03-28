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


class Wsj_bot():
    '''Creates a bot to collect all the headlines from WSJ'''

    def __init__(self, username, password):
        '''Set up driver and maximize window for consistency'''
        self.driver = webdriver.Chrome()
        self.driver.get('https://wsj.com')
        self.driver.maximize_window()
        self.usr = username
        self.pw = password

    def all_headlines(self):
        '''Collect all headlines from wsj as a list and save to file'''
        r = requests.get('https://www.wsj.com', headers={'User-Agent': 'Custom'})
        soup = BeautifulSoup(r.text, 'html.parser').find_all('a')
        headlines = [x for x in soup if x.get('href') != None and x.string != None and '/articles' in x.get('href')]
        headlines.sort(key=lambda x: len(x.string))
        articles =[x.string for x in headlines]
        with open("Headlines.txt","w+") as file:
            json.dump(articles, file)

# Possibly to be split up into a few funtions instead of just One
# Create a new keywords list, Extend list, Edit List
    def _collect_key_words(self):
        '''To collect our keywords we manualy enter them in to a list and should
        really only be used when trying to set up a new criteria for the type
        of headlines we want to recive. As of now the list of keywords is exteneded
        each time we run this function'''
        e = []
        with open('Keywords.txt', 'r') as file:
            key_words = json.loads(file.read())
        with open('Headlines.txt','r') as file:
            e = json.loads(file.read())
        for each in e:
            print(each)
            k = input('\nWhat key words are importatnt from this article title? : => ')
            w = k.split(' ')
            w = [x for x in w if x != '']
            if len(w):
                key_words.extend(w)
        with open('Keywords.txt', 'w+') as file:
            json.dump(key_words, file)


if __name__ == '__main__':
    bot = Twitter_bot(secret.TwtUsr, secret.TwtPsw)
    bot.log_in()
    bot.post('test')
    wsj = Wsj_bot('a','b')
    wsj.all_headlines()
    # bot.driver.quit()
