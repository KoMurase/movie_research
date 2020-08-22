import requests 
import pickle 
from bs4 import BeautifulSoup 
import os 
import urllib

from tqdm import tqdm 
import time 

def get_title_url(page_url):
    #page_url = "https://filmarks.com//list/genre/42?page=1" #/

    filmarks_url = "https://filmarks.com/" 
    g_r = requests.get(page_url)
    g_soup = BeautifulSoup(g_r.text, 'lxml')

    #<h3 class="p-content-cassette__title">インセプション</h3>
    titles_list = []
    titles = g_soup.find_all('h3',class_="p-content-cassette__title")
    for title in titles:
        t = title.text 
        titles_list.append(t)
    

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
        
    #print(set(more_info_urls))
    #print(len(set(more_info_urls)))   ### これだと元の配列の順序を無視されてしまう
    more_info_urls = list(dict.fromkeys(more_info_urls))  ###重複削除
    #titles = content_info.find_all('h3',class_="p-content-cassette__title")
    #read_more = content_info.find_all('a',class_="p-content-cassette__readmore")
    #print(len(titles_list))
    #print(len(more_info_urls))
    #print(page_url)
    #print(titles_list)
    #print(more_info_urls)

    del g_soup, g_r, titles_list

    return more_info_urls



def save_title_url(genre, n_page, data):
    
    save_path = r'C:\Users\mkou0\Desktop\film_search\urls\url_{}\{}_page_{}.pickle'.format(genre, genre, n_page)

    with open(save_path, mode='wb') as f:
        pickle.dump(data,f)


    return "Saved the title of URL on page {} ".format(n_page)

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

    save_dir = r'C:\Users\mkou0\Desktop\film_search\urls'
    save_dir = save_dir+r'\url_{}'.format(genre)

    print("url_{}ディレクトリを探索します".format(genre))
    path = save_dir + r"\urls_{}.pickle".format(genre)
    
    #ジャンルごとのURLを保存先のpickleファイルから取得
    with open(path, mode='rb') as f:
        data = pickle.load(f)
    print("result>>")
    print(data)

    print("{}に分類される映画1作品における情報がわかるURLをスクレイピングします...".format(genre))

    for page_url in tqdm(data):
        
        more_info_urls = get_title_url(page_url)

        n_page = page_url.split('=')[-1]
        save_title_url(genre, n_page, more_info_urls)  #urlの保存

    
    #保存先のディレクトリの確認　
    files = os.listdir(save_dir)
    print(files)

    