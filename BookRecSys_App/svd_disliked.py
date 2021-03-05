import pandas as pd
import numpy as np
from numpy import genfromtxt
# from sklearn.decomposition import TruncatedSVD
# SVD = TruncatedSVD(n_components=12, random_state=17)
# X = user_rating_pivot.values.T
# matrix = SVD.fit_transform(X)
import warnings

def svdmodel_dislike(book):
    user_rating_pivot = pd.read_csv('D:/Coding Project/Fyp/User_Rating_Pivot.csv')
    #matrix = genfromtxt('D:/Coding Project/Fyp/matrix.csv', delimiter=',')
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    corr = np.loadtxt('D:/Coding Project/Fyp/corr.txt')
    booksindex = []
    reclist = []
    booktitle = user_rating_pivot.columns
    book_list = list(booktitle)

    for i in book:
        book_index = book_list.index(i)
        booksindex.append(book_index)

    for j in booksindex:
        temp = int(j)
        reclist.append(list(booktitle[(corr[temp] > 0.97)]))

    # finalreclist = []
    # for k in reclist:
    #     isexist = False
    #     for l in reclist:
    #         if k == l:
    #             isexist = True
    #             break
    #         else:
    #             isexist = False
    #
    #     if isexist is False:
    #         finalreclist.append(k)

    return reclist
