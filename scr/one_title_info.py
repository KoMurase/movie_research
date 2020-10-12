
import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

import re 

import pandas as pd 



def scraiping_from_url(url):
    print(url)

    title_url = url
    #title_url = "https://filmarks.com//movies/81472"
    t_r = requests.get(title_url)
    t_soup = BeautifulSoup(t_r.text, 'lxml')


    meta_tag = t_soup.find("meta", content=lambda x: x and "レビュー数：" in x)

    # レビュー数：99806件 ／ 平均スコア：★★★★4.0点 から正規表現で件数だけ取り出す。
    #print(meta_tag["content"])
    n_review = re.search(r"([0-9]*件)|([^0-9]点)", meta_tag["content"]).group(1)
    #print(n_review)

    #meta_tag = t_soup.find("meta", content=lambda x: x and "平均スコア" in x)
    #print(meta_tag)
    n_score = re.search(r"([0-9]*.[0-9]*点)|([^0-9]点)", meta_tag["content"]).group(1)
    #print(n_score)

    #タイトル (ja)
    title_j = ""
    li = t_soup.find_all("li")
    for i in li:
        #print(i)
        if "の映画情報・感想・評価・動画配信" in i.text:
            #print(i.text)
            title_j = i.text.replace("の映画情報・感想・評価・動画配信", "")
            print(title_j)
    #タイトル (en)
    title_e = t_soup.find("p", class_ = "p-content-detail__original").text
    #print(title_e)

    #製作された年
    wh_created = ""
    small =  t_soup.find_all("h2", class_="p-content-detail__title") 
    for s in small:
        
        if s.find_all("a") != []:
            wh_created = s.find_all("a")[0].text
    
    #print(wh_created)

    #公開された年日
    w = ""
    www = t_soup.find_all("div", class_="p-content-detail__other-info")
    #print(www)
    for ww in www:
        #print(ww.text)

        w  = ww.text
    #print(w)
    year = ""
    month = ""
    day = ""
    place = ""
    show_time = ""
    
    #上映日：製作国：上映時間の情報が映画ごとに違うため
    ex_col = w 
    print(ex_col)

    
    if "上映日：" in w ==True and len(w)>0:
        #when_shown = w.split("／")[0].replace('上映日：','')
        #print(re.search(r"(\d*)年",w))
        if re.search(r"月(\d*)", w) != None:
            day = re.search(r"月(\d*)", w).group(1)
        if re.search(r"(\d*)月", w) != None:
            month = re.search(r"(\d*)月", w).group(1)
        if re.search(r"(\d*)年", w) != None:
            year = re.search(r"(\d*)年",w).group(1)
                
        
    #print(year, month, day)
    if "製作国：" in w:
        #place = w.split("／")[0].replace("製作国：",'')
        place = re.search("製作国："+r"(.+)", w).group(0)
        if "／" in place:
            place = place.split("／")[0]
        #place = place.replace("製作国：","").replace("／", "")
        #w = w.split("／")[1].replace('製作国：','')
    if "上映時間：" in w:
        show_time = re.search(r"(\d*)分", w).group(1)
    #print(year, month, day)
    #print( place, show_time)

    #ジャンル
    genre = t_soup.find_all("div", class_="p-content-detail__genre")
    genre = genre[0].text.replace("ジャンル：", "")
    #print(genre)

    #あらすじ
    summary2 = t_soup.find("div", class_="p-content-detail__synopsis")
    sum3=""
    summary = ""
    #print(type(summary2))
    if summary2 != None:
        for i in summary2:
            #print(type(i))
            #print(str(i))
            if "content-detail-synopsis :is-over-limit-length" in str(i) :
                #print('str',i)
                sum3 = str(i)

        sum3 = sum3.replace('"', "")
        sum3 = sum3.split("outline=")[1]
        summary = sum3.split(":truncated")[0]
    #print("summary:",summary)


    # 監督　脚本　原作
    people = t_soup.find_all("div", class_="p-content-detail__people-list-others")#others__wrapper")
    kantoku = []
    kyakuhon = []
    gensaku = []

    for p in people:
        #print(type(p))
        #print(p)
        #print(p.find("h3", class_="p-content-detail__people-list-term").text)
        job_type = p.find("h3", class_="p-content-detail__people-list-term").text
        if job_type == "監督":
            li = p.find_all("li", class_="p-content-detail__people-list-desc")
            #print(li)
            for l in li:
                name = l.find("a", class_="c-label").text
                #print("name",name)
                kantoku.append(name)
            #print(job_type, name)

        elif job_type == "脚本":
            li = p.find_all("li", class_="p-content-detail__people-list-desc")
            for l in li:
                name = l.find("a", class_="c-label").text
                #name = p.find("li", class_="p-content-detail__people-list-desc").text
                kyakuhon.append(name)
            #print(job_type, name)
        
        elif job_type == "原作":
            #name = p.find("li", class_="p-content-detail__people-list-desc").text
            #gensaku.append(name)
            li = p.find_all("li", class_="p-content-detail__people-list-desc")
            for l in li:
                name = l.text
                gensaku.append(name)
            #name = p.find("li", class_="p-content-detail__people-list-desc").text
            #print(job_type, name)
    
    #print("kantoku",kantoku)
    #print("kyakuhon",kyakuhon)
    #print("gensaku",gensaku)
    casts = []
    li = t_soup.find_all("li", class_="p-content-detail__people-list-desc")
    for l in li:
        cast = l.find("a", class_="c-label").text
        #print(cast)
        casts.append(cast)

    return n_review, n_score, title_j, title_e, wh_created,ex_col,year,month,day, \
        place, show_time, genre, summary, kantoku, kyakuhon, gensaku, casts, title_url 

def pickle_load(file_):

    with open(file_, mode='rb') as f:
        data = pickle.load(f)
    print("{}のファイルを読み込みました".format(file_))
   
    return data

if __name__ == '__main__':
    genres = [
    "SF","ドラマ","恋愛","ホラー",
    "戦争","音楽","ミュージカル", "スポーツ",
    "青春", "コメディ", "アクション", "アドベンチャー・冒険",
    "クライム", "バイオレンス", "サスペンス", "単発ドラマ",
    "ミステリー", "ファミリー", "ファンタジー", "スリラー",
    "歴史", "時代劇", "西部劇","オムニバス","伝記",
    "ドキュメンタリー","パニック","実験"
            ]
    genres2 = [
    "SF","Drama","Romance","Horror",
    "War","Music","Musical", "Sports",
    "TeenFilm", "Comedy", "Actions", "Adventures",
    "Crime", "Violence", "Suspense", "One_Shot_Dramas",
     "Mistery", "Family", "Fantasy", "Thriller",
    "History", "Zidaigeki", "WesternMovies","Omnibus","Biography",
    "Documentary","Pannic"
            ]
    for i,g in enumerate(genres):
        print("{}:{}".format(g,i))
    num = int(input("スクレイピングしたジャンルの番号を入力してください>> "))
    genre = genres2[num]
    print("{}の映画情報をCSVファイルにまとめていきまSHOW TIME !!".format(genre))

    save_dir = r'C:\Users\mkou0\Desktop\movie_research\urls'
    path = save_dir + r"\url_{}".format(genre)

    pickle_files = os.listdir(path)
    print(pickle_files)

    urls = []
    for file_ in pickle_files:
        #print(file_[0:2])
        if file_[0:len(genre)] == genre:
            urls.extend(pickle_load(path +"\{}".format(str(file_))) )

    print('URLs',urls)
    print("ジャンル{}の{}作品をcsvにまとめます".format(genre,len(urls)))


    columns = [
        "レビュー数", "平均スコア","タイトル(日本名)","タイトル(英名)","製作日",
        "上映日：製作国：上映時間","年(上映日)","月(上映日)","日(上映日)","製作国", "上映時間","ジャンル","あらすじ",
        "監督", "脚本", "原作", "キャスト" ,"URL"
        ] 
    #csvの保存先
    save_csv_dir = r"C:\Users\mkou0\Desktop\movie_research\csv"
    os.makedirs(save_csv_dir, exist_ok=True) 
    genre_data = pd.DataFrame()
    
    for i, url in enumerate(tqdm(urls)):
        
        n_review, n_score, title_j, title_e, wh_created,ex_col,year,month,day, \
        place, show_time, genre, summary, kantoku, kyakuhon, gensaku, casts, title_url= scraiping_from_url(url)


        data = [n_review, n_score, title_j, title_e, wh_created, \
                ex_col,year, month, day, place, show_time, genre, summary, \
                kantoku, kyakuhon, gensaku, casts, title_url]

        #print(len(data))
        #print([k for k in data])
        #print(len(columns))

        #result = {}
        #for j, d in enumerate(data):
        #    result.update({columns[j]:d})

        #data = pd.DataFrame(result)
        #for k, v in result.items():
        #    print(k, v[0:1])
        #print(data)
        data = pd.DataFrame(data).T
        data.columns = columns
        genre_data = pd.concat([genre_data, data], axis=0)

        time.sleep(1)

        genre_data.to_csv(save_csv_dir + "\{}.csv".format(genres2[num]), encoding = 'utf-8', index=False) #念のためセーブ


    genre_data.to_csv(save_csv_dir + "\{}.csv".format(genres2[num]), encoding = 'utf-8', index=False) #最後にセーブ

    print(pd.read_csv(save_csv_dir + "\{}.csv".format(genres2[num])))
    print("{}の映画をCSVにまとめました".format(genres2[num]))