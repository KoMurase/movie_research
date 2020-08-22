from bs4 import BeautifulSoup 
import requests 
import pickle

url = "https://filmarks.com/"

r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

c_list_line = soup.find_all('ul', class_='c-list-line')

genre = soup.find_all('ul', class_='c-list-line')[-2]
# a属性をすべて取得
genre_links = genre.find_all('a')
# ジャンル名：URL　となる辞書を作成する
genre_link_dic = {}
for link in genre_links:
    genre_url = url + link.get('href')
    name = link.text
    genre_link_dic[name] = genre_url # 辞書に追加

path = r'C:\Users\mkou0\Desktop\film_search\genre_url.pickle'

with open(path, mode='wb') as f:
    pickle.dump(genre_link_dic, f)

#Load 
#with open(path, mode='rb') as f:
#    data = pickle.load(f)
#    print(data)
#    print(type(data))

