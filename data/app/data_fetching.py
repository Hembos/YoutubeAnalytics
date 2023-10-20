from config.quota_size import *
from core.youtube import Youtube
from queue import Queue
import logging
from db.db import DataBase
from core.requests_func import requests_func, requests_quota_size
from googleapiclient.errors import HttpError

# Обновить апи
#
# Если очередь видео пуста, то запросить видео и заполнить ее (для этого сначала посчитать сколько нужно квоты и найти подходящий апи ключ)
# Получить следующий элемент из очереди и скачать информацию о видео и его комментарии (для этого сначала посчитать сколько нужно квоты и найти подходящий апи ключ)
# Обновить квоту в базе данных и вставить новое видео и его комментарии

# Для заполнения очереди:
# делаем поиск по одной из категорий
# Получаем id каналов и запрашиваем их с последующим добавлением в бд
# Получаем все id видео с каналов
# Добавляем эти id в очередь

# В будущем при смене апи ключа менять также прокси
# Для этого парсить https://free-proxy-list.net/
# Делать проверку на работоспособность прокси


def fetch(db: DataBase):
    youtube_api = None
    youtube = None

    while True:
        try:
            db.reset_api_quota()

            request = db.get_scraper_request()
            print(request)

            if not request:
                continue

            request_quota_size = requests_quota_size[request["type"]]
            new_youtube_api = db.get_available_api(
                requests_quota_size[request["type"]])

            if not new_youtube_api:
                continue

            if youtube_api == None or youtube_api["key"] != new_youtube_api["key"]:
                youtube_api = new_youtube_api

                youtube = Youtube(youtube_api["key"])

            requests_func[request["type"]](youtube, request["data"], db)

            youtube_api["quota"] = youtube_api["quota"] - request_quota_size
            db.update_api_quota(youtube_api["key"], youtube_api["quota"])

            request["tasks_left"] -= 1
            db.update_scraper_request(request)
        except HttpError as e:
            print(e)
            # db.update_api_quota(youtube_api["key"], 0)
        # if requests_queue.empty():
        #     category = db.get_available_category()

        #     if not category:
        #         continue

        #     requests_queue.put(
        #         Request(SEARCH_REQUEST, GET_CHANNELS_BY_CATEGORY, {"category": category}))

        # execute_requests(requests_queue, db)

        # if requests_queue.empty():
        #     db.complete_category(category)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        filename="data/data.log", format="%(asctime)s %(levelname)s %(message)s")

    print("To exit the application, press Ctrl-c")

    db = DataBase()
    db.create_connection()

    try:
        fetch(db)
    except KeyboardInterrupt:
        logging.info("Ctrl-c was pressed")

    db.close_connection()
