# from core.youtube import Youtube, get_first_available_key

# yt = Youtube()
# yt.read_videos_from_file("backend/data/videos.json")

# yt.fetch_video("ku7uAFfdejc")

# yt.save_videos_to_file("backend/data/videos.json")

# print(get_first_available_key(50))

from db.db import DataBase
import logging


def fetch():
    while True:
        db.reset_api_quota()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO,
    #                     filename="backend/backend.log", format="%(asctime)s %(levelname)s %(message)s")

    db = DataBase()
    db.create_connection()

    try:
        fetch()
    except KeyboardInterrupt:
        logging.info("Ctrl-c was pressed")

    db.close_connection()
