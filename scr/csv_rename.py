import glob
import os
 

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


def chage_filename(filename):
    path1 = filename 
    path2 = filename.replace('／', "")

    # ファイル名の変更 
    os.rename(path1, path2) 
    
    # ファイルの存在確認 
    print(os.path.exists(path2))