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
import slackweb
import re

import config

#slack_url = config.slack_url

def open_title_url(genre, url):

    print(url)
    id_ = url.split('/')[-1]
    
    save_path = r'C:\Users\mkou0\Desktop\movie_search\review_urls\{}\id_{}.pickle'.format(genre, id_)

    with open(save_path, mode='wb') as f:
        p_urls = pickle.dump(save_path, f)

    return p_urls

def get_reviews(genre, p_url):

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

    csv_name = p_url.split('/')[-1]

    names = []
    time_ = []
    reviews = []
    scores = []
    url_dummy = []
    title_dummy =[]
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
        url_dummy.append(p_url)
        title_dummy.append(title_j+'|'+title_e)
        #print(name)
        #print(time)
        #print(review)
        #print(score)

    li = t_soup.find_all("h2", class_="p-content-detail__title")
    for l in li:
        title = l.find("span").text

    
    code_regex = re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')
    cleaned_text = code_regex.sub('', title)
    cleaned_text = cleaned_text.replace("　", " ")
    #￥　／　：　＊　？　”　＜　＞　｜
    cleaned_text = cleaned_text.replace("/", "").replace(":","")

    data = [title_dummy, names, time_, reviews, scores,url_dummy ]
    cols = ["title","name", "time", "review", "score","URL"]

    data = pd.DataFrame(data).T
    data.columns = cols

    save_path = r'C:\Users\mkou0\Desktop\movie_search\review_csv'
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    save_path = r'C:\Users\mkou0\Desktop\movie_search\review_csv\{}'.format(genre)
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    save_path = save_path + r'\{}'.format(cleaned_text)
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True) 

    data.to_csv(save_path + r"\{}_{}.csv".format(cleaned_text, page), index=False)
    
    return '{}からの情報をcsvにしました'.format(p_url)


#「平均スコア」がついているかのcheck >> 「-点」となっていたら今後上映予定の映画
def check(df):
    df = df.copy() 
    df = df[df["平均スコア"] != "-点"]

    return df 

def pickle_load(file_):

    with open(file_, mode='rb') as f:
        data = pickle.load(f)
    print("{}のファイルを読み込みました".format(file_))
   
    return data

def save_title_path(path, save_files):
    #print(p_urls)

    with open(path, mode='wb') as f:
        pickle.dump(save_files,f)

    return "Save"

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
    
    num = int(input("スクレイピングしたジャンルの番号を入力してください>>"))
    genre = genres2[num]

    #csv_dir = r'C:\Users\mkou0\Desktop\movie_search\csv'
    csv_name = r'C:\Users\mkou0\Desktop\movie_search\csv\{}.csv'.format(genre)
    data = pd.read_csv(csv_name)

    data = check(data)
    #urls = data["URL"].values
    #data["title"] = data["タイトル(日本名)"] + data["タイトル(英名)"]

    save_path = r'C:\Users\mkou0\Desktop\movie_search\review_urls\{}'.format(genre)
    pickle_files = os.listdir(save_path)

    #slackに通知
    #slack = slackweb.Slack(url=slack_url)
    #slack.notify(text=text)

    print(len(pickle_files))

    #エラーが出たとき用のセーブ
    rest_save_path = r"C:\Users\mkou0\Desktop\movie_search\review_urls\rest.pickle"
    pickle_files = pickle_load(rest_save_path)
    print("rest:",len(pickle_files))

    c=0
    for file_ in tqdm(pickle_files):
        text = '\n{}を開けています'.format(file_)
        print(text)
        #slack = slackweb.Slack(url=slack_url)
        #slack.notify(text=text)
        urls=pickle_load(save_path +"\{}".format(str(file_)))

        for url in tqdm(urls):
            get_reviews(genre, url)

            #text = "Open {}!".format(url)
            #slack.notify(text=text)
        
        pickle_files.remove(file_)
        #print(pickle_files)
        save_title_path(rest_save_path, pickle_files)

        #残り表示
        text = "\n{} / {}".format(c, len(pickle_files))
        print(text)
        c += 1

