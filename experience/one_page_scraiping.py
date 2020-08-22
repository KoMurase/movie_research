import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 


page_url = "https://filmarks.com//list/genre/42?page=1" #/
filmarks_url = "https://filmarks.com/"

path = r'C:\Users\mkou0\Desktop\film_search\genre_url.pickle'
save_dir = r"C:\Users\mkou0\Desktop\film_search\htmls\html_SF"

#保存先のディレクトリの作成
save_dir = save_dir+"_"+page_url[-1] 
os.makedirs(save_dir, exist_ok=True)

g_r = requests.get(page_url)
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
    more_info_urls.append(filmarks_url + i.get('href'))
    
print(set(more_info_urls))
print(len(set(more_info_urls)))   ### これだと元の配列の順序を無視されてしまう
more_info_urls = list(dict.fromkeys(more_info_urls))
#titles = content_info.find_all('h3',class_="p-content-cassette__title")
#read_more = content_info.find_all('a',class_="p-content-cassette__readmore")

dummy = {}
for i,title in enumerate(titles_list):
    dummy.update({title : more_info_urls[i]}  )

print(dummy)
print(len(dummy))
""" 
確認用
for i, v in dummy.items():
    print(i, v)
""" 

