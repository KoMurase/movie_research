from bs4 import BeautifulSoup 
import requests 
import pickle
import os 
from tqdm import tqdm 
import urllib 
import time 


path = r'C:\Users\mkou0\Desktop\film_search\genre_url.pickle'

with open(path, mode='rb') as f:
    genre_link_dic = pickle.load(f)
"""    
print(type(genre_link_dic))
jenre = []
urls = []
for k in genre_link_dic.items():
    jenre.append(k[0])
    urls.append(k[1])

url = urls[0]
print(url)

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

# a というところにページ情報が入っている
pgnation = soup.find('a', class_='c-pagination__last')
#print(pgnation)
# >> <a class="c-pagination__last" href="/list/genre/61?page=87">&gt;|</a>

# 最大ページ
max_page = pgnation.get('href').split('=')[-1]
print(max_page)
"""

html_dir = path = r'C:\Users\mkou0\Desktop\film_search'

for g in genre_link_dic:

    #保存先のディレクトリの作成
    save_dir = html_dir +"\html_" + g 
    os.makedirs(save_dir, exist_ok=True)
    
    g_url = genre_link_dic[g]
    g_r = requests.get(g_url)
    g_soup = BeautifulSoup(g_r.text, 'lxml')

    #最大ページ
    pgnation =g_soup.find('a', class_='c-pagination__last')
    max_page = int(pgnation.get('href').split('=')[-1])

    for p in tqdm(range(1, max_page+1)):
        p_url = g_url + '?page=' + str(p)
        urllib.request.urlretrieve(p_url, '{}/{}.html'.format(save_dir, p))
        time.sleep(1)