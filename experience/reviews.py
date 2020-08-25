import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

import re 

import pandas as pd 

def get_reviews(p_url, genre):

    page = p_url.split('=')[-1]
    t_r = requests.get(p_url)
    t_soup = BeautifulSoup(t_r.text, 'lxml')

    #タイトル (ja)
    title_j = ""
    title_e = ""
    li = t_soup.find_all("li")
    for i in li:
        #print(i)
        if "の映画情報・感想・評価・動画配信" in i.text:
            #print(i.text)
            title_j = i.text.replace("の映画情報・感想・評価・動画配信", "")
    
    #タイトル (en)
    title_e = t_soup.find("p", class_ = "p-content-detail__original").text
    #print(title_e)

    names = []
    time_ = []
    reviews = []
    scores = []
    #レビューとコメントはp-marksごとに取得する方法が良さそう
    p_marks = t_soup.find_all("div", class_="p-mark")
    for p in p_marks:
        #<time class="c-media__date" datetime="2019-05-30 16:58">2019/05/30 16:58</time>
        #<h4 class="c-media__text"><a href="/movies/56668/reviews/96034290">つばさの感想・評価</a></h4>
        name = p.find("h4", class_="c-media__text").text
        time = p.find("time", class_="c-media__date").text
        review = p.find("div", class_="p-mark__review").text
        score = p.find("div", class_="c-rating__score").text
        names.append(name)
        time_.append(time)
        reviews.append(review)
        scores.append(score)
        print(name)
        print(time)
        print(review)
        print(score)
        print()
    
    return p_url, page, title_j, title_e, names, time_, reviews, scores

if __name__ == "__main__":
    p_url = "https://filmarks.com/movies/56668"
    get_reviews(p_url, "SF")