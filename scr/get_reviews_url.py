import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

import re 

import pandas as pd 
import numpy as np


"""
url = "https://filmarks.com/movies/63747"

title_url = url
t_r = requests.get(title_url)
t_soup = BeautifulSoup(t_r.text, 'lxml')

#レビューのページネーションを取得してサンプルとしていくつか取得する
#<a class="c-pagination__last" href="/movies/63747?page=10343">&gt;|</a>

#n_page = t_soup.find("a", class_ = "c-pagination__last")
#max_page = int(n_page.get('href').split("=")[-1])
#print(max_page)

#for p in tqdm(range(1, max_page+1)):
#    p_url = title_url + '?page=' + str(p)

#個々のレビューと評価値（星の数）を取得する
t_soup.find_all("")
#個々のレビュー <div class="p-mark__review">自分が知ってるキャラ...</div>
#星の数<div class="c-rating__score">3.5</div>
reviews = t_soup.find_all("")


#レビューとコメントはp-marksごとに取得する方法が良さそう
p_marks = t_soup.find_all("div", class_="p-mark")

for p in p_marks:
    review = p.find("div", class_="p-mark__review")
    score = p.find("div", class_="c-rating__score")
    print(review)
    print(score)
    print()

#for i, r in enumerate(reviews):
#    print("score:{}, review:{}".format((i, r)))
"""


def get_urls_per_page(url, genre):
    print("\n"+url)  
    title_url = url 
    #title_url = "https://filmarks.com//movies/81472"
     
    t_r = requests.get(title_url)
    t_soup = BeautifulSoup(t_r.text, 'lxml')

    #レビューのページネーションを取得してサンプルとしていくつか取得する
    #<a class="c-pagination__last" href="/movies/63747?page=10343">&gt;|</a>

    #<a class="c-pagination__last" href="/movies/5603?page=14751">&gt;|</a>
    #<a class="c-pagination__last" href="/movies/81472?page=3">&gt;|</a>

    n_page = t_soup.find("a", class_ = "c-pagination__last")
    if n_page != None:
        max_page = int(n_page.get('href').split("=")[-1])
        
        print(max_page)
    else:
        max_page = 1
    print(max_page)

    #1タイトルにおけるreview情報のURL全部
    p_urls = []
    for p in range(1, max_page+1):
        p_url = title_url + '?page=' + str(p)
        p_urls.append(p_url)

    id_ = title_url.split("/")[-1] #映画情報固有のURLの末尾数桁

    save_title_url(genre, id_, p_urls)

def save_title_url(genre, id_, p_urls):
    #print(p_urls)

    save_path = r'C:\Users\mkou0\Desktop\movie_search\review_urls'

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path = r'C:\Users\mkou0\Desktop\movie_search\review_urls\{}'.format(genre)
    if not os.path.exists(save_path):
        os.mkdir(save_path) 
    
    save_file = save_path + r'\id_{}.pickle'.format(id_)

    with open(save_file, mode='wb') as f:
        pickle.dump(p_urls,f)

    return "Saved the reviews of id:{}".format(id_)

def open_title_url(genre, id_):
    
    save_path = r'C:\Users\mkou0\Desktop\movie_search\review_urls\{}\id_{}.pickle'.format(genre, id_)

    with open(save_path, mode='wb') as f:
        p_urls = pickle.dump(save_path, f)

    return p_urls

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
    

#「平均スコア」がついているかのcheck >> 「-点」となっていたら今後上映予定の映画
def check(df):
    df = df.copy() 
    df = df[df["平均スコア"] != "-点"]

    return df 



if __name__ == "__main__":

    genres = [
    "SF","ドラマ","恋愛","ホラー",
    "戦争","音楽","ミュージカル", "スポーツ",
    "青春", "コメディ", "アクション", "アドベンチャー・冒険",
    "クライム", "バイオレンス", "サスペンス", "単発ドラマ",
     "ミステリー", "ファミリー", "ファンタジー", "スリラー",
    "歴史", "時代劇", "西部劇","オムニバス","伝記",
    "ドキュメンタリー","パニック"
            ]
    for i,g in enumerate(genres):
        print("{}:{}".format(g,i))
    
    num = int(input("スクレイピングしたジャンルの番号を入力してください>>"))
    
    genre = genres[num]

    csv_dir = r'C:\Users\mkou0\Desktop\movie_search\csv'

    csv_name = csv_dir + r"\{}.csv".format(genre)
    data = pd.read_csv(csv_name)
    #あらすじが書かれている映画のみを扱う
    data = check(data)
    urls = data["URL"].values
    #data["title"] = data["タイトル(日本名)"] + data["タイトル(英名)"]

    #data["url"]をつかう
    for url in tqdm(urls):
        get_urls_per_page(url, genre)
    
    print("全てのタイトルについて完了しました")

    #open_title_url(p_url, "SF")         
