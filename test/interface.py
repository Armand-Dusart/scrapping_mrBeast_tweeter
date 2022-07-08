# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 10:38:08 2021

@author: arman
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# import matplotlib 
# matplotlib.use("TkAgg")
from tkinter import *
from data_analyst import *
from PIL import ImageTk, Image
class interface:
    def __init__(self,object_data,color1,color2):
        self.color1, self.color2 = color1,color2
        self.object_data = object_data
        self.root = Tk()
        self.root.geometry("825x650")
        self.root.title("Analyse : twitter's MrBeast")
        self.list_elem = []
        
        
    def page_start(self):
        self.reset_elem()
        title = Label(self.root,text="Menu principal",relief = RAISED )
        creator = Label(self.root,text="Réalisé par DUSART Armand et GALERNEAU Arthur")
        data_viz = Button(self.root, text="Data Analyse", command=self.page_data_viz,bg=self.color1 , fg=self.color2)
        data_traitement = Button(self.root, text="Data Traitement", command=self.page_traitement,bg=self.color1 , fg=self.color2)       
        exit = Button(self.root, text="Exit", command=self.quit,bg=self.color1 , fg=self.color2)
        self.list_elem = [title,data_traitement,data_viz,exit,creator]
        self.pack()
        
        
    def page_traitement(self):
        global var
        self.reset_elem()
        var =IntVar()
        label = Label(self.root,text="Sélection avec ou sans la méthode de vectorisation tf-idf",relief = RAISED )
        tf = Checkbutton(self.root,text="TF-IDF",variable=var)
        checkbutton = Button(self.root,text="Traitement",command=self.traitement,bg=self.color1 , fg=self.color2)
        retour = Button(self.root,text="Retour",command=self.page_start,bg=self.color1 , fg=self.color2)
        exit = Button(self.root, text="Exit", command=self.quit,bg=self.color1 , fg=self.color2)
        list_tweet_origin = self.object_data.df_origin['tweet']
        df_origin = Text(self.root, height=60, width=50)
        for tweet in list_tweet_origin :
            df_origin.insert(END, str(tweet)+"\n",'follow')
        
        self.list_elem = [label,tf,checkbutton,retour,exit]
        self.pack()
        df_origin.pack(side=LEFT,padx=5,pady=5)
        self.list_elem.append(df_origin)
        
    def page_data_viz(self):
        global var2, val_choice
        var2 = IntVar()
        var2.set(0)
        val_choice = StringVar()
        val_choice.set("Commentaire")
        self.reset_elem()
        label = Label(self.root,text="Sélection de la méthode de data visualisation",relief = RAISED )
        retour = Button(self.root,text="Retour",command=self.page_start,bg=self.color1 , fg=self.color2)
        exit = Button(self.root, text="Exit", command=self.quit,bg=self.color1 , fg=self.color2)
        wordcloud = Button(self.root, text="Wordcloud", command=self.wordcloud_display,bg=self.color1 , fg=self.color2)
        if self.object_data.preprocess == False :
            disp = 'disabled'
        else :
            var2.set(1)
            disp = 'normal'
        preprocess = Checkbutton(self.root,text="Preprocess for the wordcloud",variable=var2,state=disp)
        choice = OptionMenu(self.root, val_choice, "Commentaire", "Like", "Retweet")
        graph_weight = Button(self.root, text="Les mots les plus importants", command=self.graph_tk,bg=self.color1 , fg=self.color2,state=disp)
        graph_corr = Button(self.root, text="Correlation entre les mots et RT,likes et commentaires", command=self.graph_corr,bg=self.color1 , fg=self.color2,state=disp)
        self.list_elem = [label,preprocess,wordcloud,choice,graph_weight,graph_corr,retour,exit]
        self.pack()
        
        
        
    def reset_elem(self):
        for elem in self.list_elem :
            elem.destroy()
        #self.list_elem = []
     
    def pack(self):
        for elem in self.list_elem :
            elem.pack(side=TOP,padx=5,pady=5)
        
    def quit(self) :
        self.root.destroy()
        
    def loop(self):
        self.root.mainloop()
    
    def wordcloud_display(self):
        global var2,fig
        if len(self.list_elem) > 8 : 
            fig.destroy()
            self.list_elem.remove(fig)
        origin = True
        if var2.get() == 1 :
            origin = False
        fig = self.object_data.wordcloud(origin)
        plot = FigureCanvasTkAgg(fig, self.root) 
        fig = plot.get_tk_widget()
        fig.pack()
        self.list_elem.append(fig)
    
    def graph_tk(self):
        global fig, val_choice
        dict = {"Commentaire":'com',"Like":'like','Retweet':'rt'}
        val = dict[val_choice.get()]
        if len(self.list_elem) > 8 : 
            fig.destroy()
            self.list_elem.remove(fig)
        fig = self.object_data.words_weight_analyse_for_notoriety(val)
        plot = FigureCanvasTkAgg(fig, self.root) 
        fig = plot.get_tk_widget()
        fig.pack()
        self.list_elem.append(fig)
    
    def graph_corr(self):
        global fig
        if len(self.list_elem) > 8 : 
            fig.destroy()
            self.list_elem.remove(fig)
        fig = self.object_data.correlation()
        plot = FigureCanvasTkAgg(fig, self.root) 
        fig = plot.get_tk_widget()
        fig.pack()
        self.list_elem.append(fig)
        
    def traitement(self):
        global var
        if var.get() == 1 : 
            tf_idf = True
        else :
            tf_idf = False
        self.object_data.preprocessing()
        self.object_data.vectorize_tweet(tf_idf)
        list_tweet_origin = self.object_data.df['tweet']
        df = Text(self.root, height=60, width=50)
        for tweet in list_tweet_origin :
            df.insert(END, str(tweet)+"\n",'follow')
        df.pack(side=LEFT,padx=5,pady=5)
        self.list_elem.append(df)
        
        
   
        
        
            

    
   