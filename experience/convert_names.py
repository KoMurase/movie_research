import pandas as pd 
import gc 
import os
from tqdm import tqdm
from multiprocessing import Pool, Process  
#from pandarallel import pandarallel
#pandarallel.initialize(progress_bar=True)

 
def text_process(df, profession:list, word:str ):
    df = df.copy() 
    
    profession = set(profession) #リストを集合に変換 
    for p in tqdm(profession):
        df['review'] = df['review'].replace(p, word)
    return df 
"""
def text_process2(text):
    #df = df.copy() 
    word = 'DIRECTOR'
    profession = set(directors) #リストを集合に変換
    del directors

    for p in profession:
        #df['review'] = df['review'].replace(p, word)
        text = text.replace(p, word)
    return text

def text_process3(text):

    #df = df.copy() 
    word = 'WRITER'
    profession = set(writers) #リストを集合に変換
    del writers
    for p in profession:
        #df['review'] = df['review'].replace(p, word)
        text = text.replace(p, word)
    return text

"""
if __name__=='__main__':
    path = r'C:\Users\mkou0\Desktop\movie_research'
    data_review = pd.read_csv(path + r'\review_csv\SF_data\SF_data.csv', usecols = {"score","review"})
    data_review_2 = pd.read_csv(path + r'\review_csv\SF_data\SF_data_2.csv')

    data_review = pd.concat([data_review, data_review_2], axis=0)
    del data_review_2
    gc.collect() 
    print('Reading Dataset is done.')
    print('{}'.format( data_review.__len__() ))
    writers = pd.read_pickle(path+r'\エンドロールに出てくる人たち\writers.pkl')
    directors = pd.read_pickle(path+r'\エンドロールに出てくる人たち\directors.pkl')
    casts = pd.read_pickle(path+r'\エンドロールに出てくる人たち\casts.pkl')

    #casts = get_worker(path+r'\エンドロールに出てくる人たち\casts.pkl')
    data_review = text_process(data_review,profession=casts, word='CAST')
    #data_review.review = data_review.review.parallel_apply(text_process)
    #data_review.review = data_review.review.apply(text_process)
    print('Done')
    data_review = text_process(data_review,profession=directors, word='DIRECTOR')
    #data_review.review = data_review.review.parallel_apply(text_process2)
    #data_review.review = data_review.review.apply(text_process2)
    print('Done')
    data_review = text_process(data_review,profession=writers, word='WRITER')
    #data_review.review = data_review.review.parallel_apply(text_process3)
    #data_review.review = data_review.review.apply(text_process3) 
    print('Done')

    data_review.to_csv(path+r'\review_csv\SF_data_preprocess.csv', index=False)
