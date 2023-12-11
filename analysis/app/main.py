from db.db import DataBase
from requests_func import requests_func


# comments = db.get_comments("5UeVOUgtkyM", {"id": 1, "textDisplay": 1})
# comments_size = np.ndarray((len(comments))).astype("int")
# for i, comment in enumerate(comments):
#     comments_size[i] = len(comment["textDisplay"])

#     if comments_size[i] > 5000:
#         print(comment["id"])

# n, x, _ = plt.hist(comments_size, 1000, density=False)
# plt.show()


def process(db: DataBase):
    while True:
        request = db.get_scraper_request(7, 10)

        if not request:
            continue

        requests_func[request["type"]](request["data"], db)

        request["tasks_left"] -= 1
        db.update_scraper_request(request)


if __name__ == "__main__":
    print("To exit the application, press Ctrl-c")

    db = DataBase()
    db.create_connection()

    process(db)

    db.close_connection()
