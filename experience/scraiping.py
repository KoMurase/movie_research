import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

"""
やりたいこと
・スコア(★の数)を回帰分析すること
・どの監督とどの脚本が一番スコアが高いか
・監督と俳優陣に相性はあるのか
欲しい情報
・スコア (= y1)
・見た人 (= y2)
・タイトル
・出演俳優 (on-hot化する予定→メモリがやばいかもしれない)
・制作国 
・上映日
・監督
・脚本
・映画賞・映画祭りの有無
・上映時間
・ジャンル

・感想 review
"""

"""
------方針 ----------

0. ジャンルを指定する   50%　引数渡して自動化したい
1. ページごとのURL取得  100%
2. 1ページ当たりの映画情報の取得 100%
3. 以下の情報をcsv化 (ページごとに行う)
・スコア (= y1)
・見た人 (= y2)
・タイトル
・出演俳優 (on-hot化する予定→メモリがやばいかもしれない)
・制作国 
・上映日
・監督
・脚本
・映画賞・映画祭りの有無
・上映時間
・ジャンル
"""
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

url = "https://filmarks.com" #/

path = r'C:\Users\mkou0\Desktop\film_search\genre_url.pickle'
save_dir = r'C:\Users\mkou0\Desktop\film_search\htmls'
with open(path, mode='rb') as f:
    data = pickle.load(f)
    #print(data)
    #print(type(data))


#保存先のディレクトリの作成
save_dir = save_dir+'\html_SF' 
os.makedirs(save_dir, exist_ok=True)

g = 'SF'
print(data[g])
g_url = data[g]
g_r = requests.get(g_url)
g_soup = BeautifulSoup(g_r.text, 'lxml')

#<h3 class="p-content-cassette__title">インセプション</h3>
titles_list = []
titles = g_soup.find_all('h3',class_="p-content-cassette__title")
for title in titles:
    t = title.text 
    titles_list.append(t)
print(len(titles_list))

# [title : url(read_more)] を作る
#<a class="" href="/movies/83512">&gt;&gt;詳しい情報を見る</a>
more_info_urls = []
#target_div = g_soup.find_all('div',class_="p-content-cassette__people__readmore")
content_info = g_soup.find_all('a', class_="p-content-cassette__readmore")
for i in content_info:
    if 'reviews' in i.get('href'):   ### reiew情報はここで省く
        continue
    #print(i.get('href'))
    more_info_urls.append(url + i.get('href'))
    
print(set(more_info_urls))
print(len(set(more_info_urls)))

#titles = content_info.find_all('h3',class_="p-content-cassette__title")
#read_more = content_info.find_all('a',class_="p-content-cassette__readmore")

dummy = {}
for i,title in enumerate(titles_list):
    dummy.update({title : more_info_urls[i]}  )

print(dummy)
print(len(dummy))

###　以上のコードをページごとに行う   ###


""" 
###　ページの最大値の取得とページごとのURLの取得

#最大ページの取得
pgnation =g_soup.find('a', class_='c-pagination__last')
max_page = int(pgnation.get('href').split('=')[-1])
print("max_page : ",max_page)

#ページごとのhtmlを取得
for p in tqdm(range(1, max_page+1)):
    p_url = g_url + '?page=' + str(p)
    urllib.request.urlretrieve(p_url, '{}/{}.html'.format(save_dir, p))
    time.sleep(1)

    print(p_url)

#### done 

"""



