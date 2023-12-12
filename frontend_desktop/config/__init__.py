from decouple import config


API_URL = config('API_URL')

GET_CHANNELS_BY_CATEGORY = 0
GET_CHANNEL_BY_ID = 1
GET_VIDEOS_BY_CHANNEL_ID = 2
GET_VIDEO_BY_ID = 3
GET_COMMENTS_BY_VIDEO_ID = 4
GET_CHANNEL_BY_URL = 5
GET_CHANNEL_BY_VIDEO_ID = 6

type_request_str = {
    GET_CHANNELS_BY_CATEGORY: "Скачать данные канала по категориям",
    GET_CHANNEL_BY_ID: "Скачать данные канала по id",
    GET_VIDEOS_BY_CHANNEL_ID: "Скачать данные видео по id канала",
    GET_VIDEO_BY_ID: "Скачать данные видео по его id",
    GET_COMMENTS_BY_VIDEO_ID: "Скачать данные комментариев по id видео",
    GET_CHANNEL_BY_URL: "Скачать данные канала по url",
    GET_CHANNEL_BY_VIDEO_ID: "Скачать данные канала по видео id"
}


