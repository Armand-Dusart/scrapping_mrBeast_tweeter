import time
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np
import sys


def driver():

    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    return webdriver.Chrome(executable_path=ChromeDriverManager().install())

def scroll(wait, nbr_of_scroll=1, time_to_sleep=15):
    for item in range(1): 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        sleep(time_to_sleep)
        
def scrap_tweets(driver):
    
    tweets = []
    coms = []
    rts = []
    likes = []
    nb_tweet = 0
    tweet_div = driver.find_elements_by_css_selector("div[class='css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0']")
    number = driver.find_elements_by_css_selector("div[class='css-1dbjc4n r-xoduu5 r-1udh08x']")
    
    for tweet in tweet_div:
        tweets.append(tweet.text.replace("\n"," "))
        nb_tweet += 1
   
    i = 0
    for numb in number:
        numb = numb.text
        if ('k' in numb):
            numb = numb.replace(" k","").replace(",", ".")
            numb = float(numb) * 1000
            numb = int(numb)
            numb = str(numb)
            
        if ( i % 3 == 0):
            coms.append(numb.replace("\n"," "))
        if ( i % 3 == 1 ):
            rts.append(numb.replace("\n"," "))
        if (i % 3 == 2 ):
            likes.append(numb.replace("\n"," "))
        i += 1

    return tweets,nb_tweet, coms, rts, likes

def work(nb_tweet,page):
    
    driver.get(page) 
    
    wait = WebDriverWait(driver,15)
    sleep(2)
    SCROLL_PAUSE_TIME = 2
    cmpt = 0  
    tweets = np.array([])
    coms = np.array([])
    rts = np.array([])
    likes = np.array([])
    
    while cmpt < nb_tweet:
            
        tweet, nb_scrap_tweet, com, rt, like = scrap_tweets(driver)
        tweets = np.append(tweets,tweet)
        coms = np.append(coms,com)
        rts = np.append(rts,rt)
        likes = np.append(likes,like)

        cmpt += nb_scrap_tweet
        print("scroll")
        scroll(wait,1,2)
        time.sleep(SCROLL_PAUSE_TIME)

    data ={'tweet': tweets,
       'nb_com' : coms,
       'nb_rt' : rts,
       'nb_like': likes
       }
    
    df = pd.DataFrame(data, columns = ['tweet', 'nb_com', 'nb_rt', 'nb_like'])
    df.to_csv('tweets_mrbeast.csv', index = False, header=True,encoding='utf-8-sig',sep=';')

if __name__ == "__main__":  
    
    driver = driver()
    page = "https://twitter.com/mrbeastyt"
    nb_tweets = 300
    work(nb_tweets,page)
    driver.close()