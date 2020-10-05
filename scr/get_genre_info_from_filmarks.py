import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

import sys

score = []
view = [] #見た人
wanto_view = [] #見たい人
title = []
actors = [] #俳優陣
production_ = [] #制作国
when_shown = [] #いつ放送されたか
director = [] #監督
scriptwriter = [] #脚本家
prize = [] #受賞の有無
timely = [] #上映の有無
genre = [] #ジャンル


def get_genre_info(genre, path):
    
    #ジャンルごとのURLを
    #返す関数

    urls = []
    url = "https://filmarks.com" #/

    #あらかじめ取得したジャンルごとのURL情報の保存先
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        print(data)
        #print(type(data))

    print(data[genre])
    g_url = data[genre]
    g_r = requests.get(g_url)
    g_soup = BeautifulSoup(g_r.text, 'lxml')

    ###　ページの最大値の取得とページごとのURLの取得

    #最大ページの取得
    pgnation =g_soup.find('a', class_='c-pagination__last')
    max_page = int(pgnation.get('href').split('=')[-1])
    print("max_page : ",max_page)

    #ページごとのurlを取得
    for p in tqdm(range(1, max_page+1)):
        p_url = g_url + '?page=' + str(p)
        #urllib.request.urlretrieve(p_url, '{}/{}.html'.format(save_dir, p))
        time.sleep(1)
        urls.append(p_url)

    return urls

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

    genres2 = [
    "SF","Drama","Romance","Horror",
    "War","Music","Musical", "Sports",
    "TeenFilm", "Comedy", "Actions", "Adventures",
    "クライム", "バイオレンス", "サスペンス", "One_Shot_Dramas",
     "Mistery", "Family", "Fantasy", "Thriller",
    "History", "Zidaigeki", "WesternMovies","Omnibus","Biography",
    "Documentary","Pannic"
            ]

    for i,g in enumerate(genres):
        print("{}:{}".format(g,i))
    
    num = int(input("スクレイピングしたいジャンルの番号を入力してください>>"))
        
    if num == 0: genre = "SF"
    elif num == 1: genre = "ドラマ"
    elif num == 2: genre = "恋愛"
    elif num == 3: genre = "ホラー"
    elif num == 4: genre = "戦争"
    elif num == 5: genre = "音楽"
    elif num == 6: genre = "ミュージカル"
    elif num == 7: genre = "スポーツ"
    elif num == 8: genre = "青春"
    elif num == 9: genre = "コメディ"
    elif num == 10: genre = "アクション"
    elif num == 11: genre = "アドベンチャー・冒険"
    elif num == 12: genre = "クライム"
    elif num == 13: genre = "バイオレンス"
    elif num == 14: genre = "サスペンス"
    elif num == 15: genre = "単発ドラマ"
    elif num == 16: genre = "ミステリー"
    elif num == 17: genre = "ファミリー"
    elif num == 18: genre = "ファンタジー"
    elif num == 19: genre = "スリラー"
    elif num == 20: genre = "歴史"
    elif num == 21: genre = "時代劇"
    elif num == 22: genre = "西部劇"
    elif num == 23: genre = "オムニバス"
    elif num == 24: genre = "伝記"
    elif num == 25: genre = "ドキュメンタリー"
    elif num == 26: genre = "パニック"

    url_path = r'C:\Users\mkou0\Desktop\movie_search\genre_url.pickle'
    print("{}の映画情報がわかるURLをスクレイピングします...".format(genre))
    urls = get_genre_info(genre ,url_path)
    print(urls)

    save_dir = r'C:\Users\mkou0\Desktop\movie_search\urls'
    os.makedirs(save_dir, exist_ok=True) 
    #保存先のディレクトリの作成
    save_dir = save_dir+r'\url_{}'.format(genre) 
    os.makedirs(save_dir, exist_ok=True)

    path = save_dir+r"\urls_{}.pickle".format(genre)

    with open(path, mode='wb') as f:
        pickle.dump(urls,f)

    print("Saving urls is done!")

    with open(path, mode='rb') as f:
        data = pickle.load(f)
    print("result>>")
    print(data)