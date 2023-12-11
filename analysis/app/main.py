from db.db import DataBase
import matplotlib.pyplot as plt
import numpy as np
from time import time

db = DataBase()
db.create_connection()

comments = db.get_comments("5UeVOUgtkyM", {"id": 1, "textDisplay": 1})
comments_size = np.ndarray((len(comments))).astype("int")
for i, comment in enumerate(comments):
    comments_size[i] = len(comment["textDisplay"])

    if comments_size[i] > 5000:
        print(comment["id"])

n, x, _ = plt.hist(comments_size, 1000, density=False)
plt.show()

db.close_connection()
