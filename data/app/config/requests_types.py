GET_CHANNELS_BY_CATEGORY = 0
GET_CHANNEL_BY_ID = 1
GET_VIDEOS_BY_CHANNEL_ID = 2


class Request:
    def __init__(self, quota_size: int, type: int, header: dict) -> None:
        self.quota_size = quota_size
        self.type = type
        self.header = header
