import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

import re 

import pandas as pd 


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

"""
#個々のレビューと評価値（星の数）を取得する
t_soup.find_all("")
#個々のレビュー <div class="p-mark__review">自分が知ってるキャラ...</div>
#星の数<div class="c-rating__score">3.5</div>
reviews = t_soup.find_all("")

"""

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

def get_urls_per_page(url):
    url = "https://filmarks.com/movies/63747"

    title_url = url
    t_r = requests.get(title_url)
    t_soup = BeautifulSoup(t_r.text, 'lxml')

    #レビューのページネーションを取得してサンプルとしていくつか取得する
    #<a class="c-pagination__last" href="/movies/63747?page=10343">&gt;|</a>

    n_page = t_soup.find("a", class_ = "c-pagination__last")
    max_page = int(n_page.get('href').split("=")[-1])
    print(max_page)

    p_urls = []

    for p in tqdm(range(1, max_page+1)):
        p_url = title_url + '?page=' + str(p)
        p_urls.append(p_url)

    return p_urls

#タイトルがあるかどうかのcheck
def check_title(df):
    df = df.copy() 
    df["flg_title"] = 0
    if df["タイトル（日本名）"] != "":
        df["flg_title"] = 1
    if df["タイトル（英名）"] != "":
        df["flg_title"] = 1 
    
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
    
    #num = int(input("スクレイピングしたジャンルの番号を入力してください>>"))
    
    #genre = genres[num]

    #csv_dir = r'C:\Users\mkou0\Desktop\movie_search\csv'

    #csv_name = csv_dir + r"\{}.csv".format(genre)
    #data = pd.read_csv(csv_name)
    #あらすじが書かれている映画のみを扱う
    #data = data[data["あらすじ"] != ""]
    #urls = data["URL"].values

    data["タイトル（日本名）"] != ""

    #dir:urls にあるurlを使うかもう一度スクレイピングしてそこからURLを取得するか
    for url in urls:
        p_urls = get_urls_per_page(url)

           
