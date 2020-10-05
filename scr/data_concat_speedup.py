#pandas.read_csv map multiprocessing
import time
import glob
import numpy as np 
import pandas as pd
import os
from multiprocessing import Pool

#map_multiprocessing(pd.concat)
def readcsv_map_multi(fileslist):
    p = Pool(os.cpu_count())
    df = pd.concat(p.map(pdreadcsv, fileslist))
    p.close()
    return df

#csv1個読み込み(map関数用)
def pdreadcsv(csv_path):
    try : 
        return pd.read_csv(csv_path)
    except :
        print("error {}".format(csv_path))
    
if __name__ == "__main__":

    path = "/Users/mkou0/Desktop/movie_research/review_csv/trouble_folder"
    folders = os.listdir(path)
    csv_folders=[]
    for folder in folders:
        csv_folders.append(path+'/'+folder)

    csv_files = []
    for folder in csv_folders:
        files = os.listdir(folder)
        for file in files:
            csv_files.append(folder+'/'+file)
    
  
    start = time.time()
    df = readcsv_map_multi(csv_files)
    df.to_csv("/Users/mkou0/Desktop/movie_research/review_csv/SF_data_2.csv", index=False)
    process_time = time.time() - start
    print('csv読み込み時間：{:.3f}s'.format(process_time))