
from db.db import DataBase
from requests_func import requests_func


def process(db: DataBase):
    while True:
        request = db.get_scraper_request(7, 12)

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
