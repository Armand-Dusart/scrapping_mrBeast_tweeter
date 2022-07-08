# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 10:38:08 2021

@author: arman
"""

from collections import Counter
from wordcloud import WordCloud

import pandas as pd
import string
import matplotlib.pyplot as plt
from matplotlib import colorbar
from matplotlib.figure import Figure
import seaborn as sns
import re
#from statistics import mean

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords 
from nltk import StanfordPOSTagger

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


class tweet_analyst_init:
    def __init__(self,PATH):
        self.df = pd.read_csv(PATH,sep=";").dropna().drop_duplicates(subset=['tweet'])
        self.df_origin = pd.read_csv(PATH,sep=";").dropna().drop_duplicates(subset=['tweet'])
        # PATH_JAR = r"C:\Users\arman\Desktop\projet_webscraping\stanford-postagger-full-2020-11-17\stanford-postagger.jar"
        # PATH_MODEL = r"C:\Users\arman\Desktop\projet_webscraping\stanford-postagger-full-2020-11-17\models\english-caseless-left3words-distsim.tagger"
        # self.Tagger = StanfordPOSTagger(PATH_MODEL,PATH_JAR)
        self.stemmer = SnowballStemmer("english")
        self.stop_words = stopwords.words('english')
        self.preprocess = False
        self.vectorize = False
        self.df['nb_rt'] = self.df['nb_rt'].apply(lambda x : x.replace(" M","000000").replace(",","")).astype(int)
        
        
    def wordcloud(self,origin): 
        print("wordcloud creation...")
        if origin==True :
            df = self.df_origin
            prepro = False
        else :
            df = self.df
            prepro = True
          
        freq = Counter([word.replace("callusertwitt","@") for tweet in df['tweet'] for word in tweet.split(" ")])
        wordcloud = WordCloud().generate_from_frequencies(freq)
        figure = plt.figure()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title("Wordcloud with preprocess = {}".format(str(prepro)))
        print("wordcloud finished")
        return figure
    
    def preprocessing(self):
        print("preprocessing...")
        # Convertir le texte en minuscule
        self.df['tweet'] = self.df['tweet'].astype('str').apply(lambda x : x.lower().replace('@','callusertwitter '))
        # supprimer les digits 
        self.df['tweet'] = self.df['tweet'].apply(lambda x: re.sub('\d+', '', x))
        # Supprimer caractères spéciaux
        self.df['tweet'] = self.df['tweet'].apply(lambda x: re.sub('\W+', ' ', x))
        self.df['tweet'] = self.df['tweet'].apply(lambda x: " ".join([self.stemmer.stem(word) for word in word_tokenize(x) if word not in self.stop_words]))
        self.df = self.df.reset_index(drop=True)
        self.preprocess = True
        print("prepocessing finished")
        
    # def pos_tagger_stand(self) :
    #     print("tagger...")
    #     try :
    #         self.df.loc[:,'tweet_tag'] = [self.Tagger.tag(tweet) for tweet in self.df['tweet'].apply(word_tokenize)]
    #         print("tagging success new column : tweet_tag")
    #     except :
    #         print("ERROR USE TAGGER")   
    
    def vectorize_tweet(self,tf_idf):
        print("vectoriz tweet with tf_idf : ",str(tf_idf), "...")
        if tf_idf == False :
            vectorizer = CountVectorizer()
            vector = vectorizer.fit_transform(self.df['tweet'])
        else :
            vectorizer = TfidfVectorizer()
            vector = vectorizer.fit_transform(self.df['tweet'])
        self.df_vectoriz = pd.DataFrame(data=vector.toarray(),columns=vectorizer.get_feature_names())
        self.vectorize = True
        self.df_corr = pd.concat([self.df_vectoriz,self.df[['nb_like','nb_rt','nb_com']]], axis=1)
        print("vectorizer success new dataframe : df_vectoriz build")
        
        
    def words_weight_analyse_for_notoriety(self,opt):
        print("analyse of word's weight for : ",opt,"...")
        try :
            weight = self.df_vectoriz
            if opt=="com":
                for column in weight.columns :
                    weight[column] = weight[column] * self.df['nb_com']
                weight = weight.apply(sum).sort_values(ascending=False)[:20]
                
            elif opt=="like":
                for column in weight.columns :
                    weight[column] = weight[column] * self.df['nb_like']
                weight = weight.apply(sum).sort_values(ascending=False)[:20]
            elif opt=="rt":
                for column in weight.columns :
                    weight[column] = weight[column] * self.df['nb_rt']
                weight = weight.apply(sum).sort_values(ascending=False)[:20]
            else :
                print("use param : com or like or rt")
                return False
            figure = plt.figure(figsize=(15,6))
            weight = weight.rename(index={'callusertwitt':'@'})
            title = "word's importance for " + opt
            plt.title(title)
            plt.bar(weight.index,weight.values)
            plt.xticks(rotation = 90, fontsize = 10)
            print('analyse finished') 
            return figure
        except AttributeError :
            print('ERROR, maybe you have to use vectorize_tweet before')
      
    def correlation(self):
        print("Correlation....")
        if self.vectorize == True :
            print('Correlation finished') 
            df_corr = self.df_corr.corr()[['nb_like','nb_rt','nb_com']].drop(['nb_like','nb_rt','nb_com'])
            df_corr = df_corr.applymap(lambda x : x if abs(x) > 0.2 else None).dropna(how="all")
            figure = plt.figure(figsize=(10,6))
            sns.heatmap(df_corr, vmin=-1, vmax=1, annot=True)
            plt.title("Correlation matrix")
            return figure
        else :
            print('ERROR, maybe you have to use vectorize_tweet before')
            return False
            
"""
test
"""           
# PATH = r"C:\Users\arman\Desktop\projet_webscraping\tweets_mrbeast.csv"        
# data = tweet_analyst_init(PATH)
# data.preprocessing()
# data.vectorize_tweet(tf_idf=True)
# data.correlation()




