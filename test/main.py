# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 10:38:07 2021

@author: arman
"""

from data_analyst import *
from interface import *

PATH = r"C:\Users\arman\Desktop\projet_webscraping\tweets_mrbeast.csv"
data = tweet_analyst_init(PATH)
intt = interface(data,'SkyBlue3','black')
intt.page_start()
intt.loop()


