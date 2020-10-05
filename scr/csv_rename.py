import glob
import os
 


#error /Users/mkou0/Desktop/movie_search/review_csv/SF/ミムジー 〜未来からのメッセージ〜/ミムジー未来からのメッセージ.csv
#error /Users/mkou0/Desktop/movie_search/review_csv/SF/世界侵略ロサンゼルス決戦/世界侵略

def change_filename(filename):
    path1 = filename 
    path2 = filename.replace('／', "")

    # ファイル名の変更 
    os.rename(path1, path2) 
    
    # ファイルの存在確認 
    print(os.path.exists(path2))

if __name__ == "__main__":
    path = "/Users/mkou0/Desktop/movie_search/review_csv/trouble_folder"
    folders = os.listdir(path)
    csv_folders=[]
    for folder in folders:
        csv_folders.append(path+'/'+folder)

    csv_files = []
    for folder in csv_folders:
        files = os.listdir(folder)
        for file in files:
            csv_files.append(folder+'/'+file)
    for file in csv_files:
        change_filename(file)