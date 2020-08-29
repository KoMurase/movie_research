import pandas as pd
import os 
from tqdm import tqdm
path = "/Users/mkou0/Desktop/movie_search/review_csv/SF"
folders = os.listdir(path)
csv_folders=[]
for folder in folders:
    csv_folders.append(path+'/'+folder)

csv_files = []
for folder in csv_folders:
    files = os.listdir(folder)
    for file in files:
        csv_files.append(folder+'/'+file)

data = pd.DataFrame()
for csv in tqdm(csv_files):
    #print(csv)
    try:
        df = pd.read_csv(csv)
        data = pd.concat([data, df], axis=0)
        data.to_csv("/Users/mkou0/Desktop/movie_search/review_csv/SF_data.csv", index=False)

    except Exception:
        print("error {}".format(csv))
        continue

#data.to_csv(path + "./SF_data.csv", index=False)

