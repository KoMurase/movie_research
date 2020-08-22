
import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

import re 

title_url = "https://filmarks.com/movies/63747" #レディプレイヤー1をサンプルに使用。ちなみに単体作品では一番好きな作品。
#title_url = "https://filmarks.com/movies/5603"
filmarks_url = "https://filmarks.com/" 


t_r = requests.get(title_url)
t_soup = BeautifulSoup(t_r.text, 'lxml')


"""review_count = t_soup.find_all("span", class_= "c-content__count")
for rc in review_count:
    print(rc.text)
    print()

これでは 
{{ viewingMarkCount }}
{{ viewingClipCount }}
    が多数返ってくる。

理由は, Javascriptで後から挿入しているためである.
    """


meta_tag = t_soup.find("meta", content=lambda x: x and "レビュー数" in x)

# レビュー数：99806件 ／ 平均スコア：★★★★4.0点 から正規表現で件数だけ取り出す。
print(meta_tag["content"])
n_review = re.search(r"(\d*)件", meta_tag["content"]).group(1)
print(n_review)

meta_tag = t_soup.find("meta", content=lambda x: x and "平均スコア" in x)
n_score = re.search(r"(\d*\.\d*)点", meta_tag["content"]).group(1)
print(n_score)

#タイトル
#レディ・プレイヤー1の映画情報・感想・評価・動画配信

li = t_soup.find_all("li")
for i in li:
    #print(i)
    if "の映画情報・感想・評価・動画配信" in i.text:
        print(i.text)
        title = i.text.replace("の映画情報・感想・評価・動画配信", "")
        print(title)

title_e = t_soup.find("p", class_ = "p-content-detail__original").text
print(title_e)
#制作された年
small =  t_soup.find("small") 
wh_created = small.text
print(wh_created)


#公開された年日

#<div class=><h3 class="p-content-detail__other-info-title">上映日：2018年04月20日</h3> ／ <h3 class="p-content-detail__other-info-title">製作国：</h3><ul><li><a href="/list/country/5">アメリカ</a></li></ul> ／ <h3 class="p-content-detail__other-info-title">上映時間：140分</h3></div>
www = t_soup.find_all("div", class_="p-content-detail__other-info")
#print(www)
for ww in www:
    print(ww.text)
    w  = ww.text

when_shown = w.split("／")[0].replace('上映日：','')
where_created = w.split("／")[1].replace("製作国：",'')
show_time = w.split("／")[2].replace("上映時間：",'')
print(when_shown, where_created, show_time)

#<div class=><h3 class="p-content-detail__genre-title">ジャンル：</h3><ul><li><a href="/list/genre/5">アクション</a></li><li><a href="/list/genre/39">アドベンチャー・冒険</a></li><li><a href="/list/genre/42">SF</a></li></ul></div>

#ジャンル
genre = t_soup.find_all("div", class_="p-content-detail__genre")
genre = genre[0].text.replace("ジャンル：", "")
print(genre)

#あらすじ

#div class="p-content-detail__synopsis"
summary2 = t_soup.find("div", class_="p-content-detail__synopsis",)
#print(summary2.text)
#print(summary2["content-detail-synopsis :is-over-limit-length="])

sum3=""
for i in summary2:
    #print(type(i))
    #print(str(i))
    if "content-detail-synopsis :is-over-limit-length" in str(i) :
        print('str',i)
        sum3 = str(i)

sum3 = sum3.replace('"', "")
sum3 = sum3.split("outline=")[1]
summary = sum3.split(":truncated")[0]
print("summary:",summary)
print()

people = t_soup.find_all("div", class_="p-content-detail__people-list-others")#others__wrapper")
kantoku = []
kyakuhon = []
gensaku = []

for p in people:
    print(type(p))
    print(p)
    print(p.find("h3", class_="p-content-detail__people-list-term").text)
    job_type = p.find("h3", class_="p-content-detail__people-list-term").text
    if job_type == "監督":
        name = p.find("li", class_="p-content-detail__people-list-desc").text
        kantoku.append(name)
        print(job_type, name)
    elif job_type == "脚本":
        name = p.find("li", class_="p-content-detail__people-list-desc").text
        kyakuhon.append(name)
        print(job_type, name)
    
    elif job_type == "原作":
        gensaku.append(name)
print(kantoku)
print(kyakuhon)
print(gensaku)

casts = []
#<li class="p-content-detail__people-list-desc"><a href="/people/53361" class="c-label">レオナルド・ディカプリオ</a></li>
li = t_soup.find_all("li", class_="p-content-detail__people-list-desc")
for l in li:
    cast = l.find("a", class_="c-label").text
    print(cast)
    casts.append(cast)


