import pickle
rest_save_path = r"C:\Users\mkou0\Desktop\movie_search\review_urls\rest.pickle"
with open(rest_save_path, mode='rb') as f:
    p_urls = pickle.load(f)

print(p_urls)