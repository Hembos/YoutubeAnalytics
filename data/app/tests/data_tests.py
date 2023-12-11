import unittest

from analysis.app.emotion_analisis.analyser import Analyser
from analysis.app.metrics.loader import Loader
from data.app.config.requests_types import GET_ANALYSIS_OF_TIME
from data.app.core.requests_func import get_time_analisis, get_lang_analisis, get_emotion_analisis, \
    get_likes_vs_replies_analisis, get_neq_pos_analisis
from data.app.db.db import DataBase


class TestLoading(unittest.TestCase):
    def test_time_analisis(self):
        v_id = 'g_sA8hYU3b8'
        ch_id = 'UConVfxXodg78Tzh5nNu85Ew'
        loader = Loader([ch_id])
        comments = loader.get_all_comments(ch_id, v_id)
        data = {
            'comments': comments,
            'videoId': v_id,
            'channelId': ch_id
        }
        db = DataBase()
        db.create_connection()
        get_time_analisis(data, db)
        db.close_connection()

    def test_lang_analisis(self):
        v_id = 'g_sA8hYU3b8'
        ch_id = 'UConVfxXodg78Tzh5nNu85Ew'
        loader = Loader([ch_id])
        analyser = Analyser()
        comments = loader.get_all_comments(ch_id, v_id)
        data = {
            'comments': comments,
            'videoId': v_id,
            'channelId': ch_id
        }
        db = DataBase()
        db.create_connection()
        get_lang_analisis(data, db, analyser)
        db.close_connection()

    def test_emotion_analisis(self):
        v_id = 'g_sA8hYU3b8'
        ch_id = 'UConVfxXodg78Tzh5nNu85Ew'
        loader = Loader([ch_id])
        analyser = Analyser()
        comments = loader.get_all_comments(ch_id, v_id)
        data = {
            'comments': comments,
            'videoId': v_id,
            'channelId': ch_id
        }
        db = DataBase()
        db.create_connection()
        get_emotion_analisis(data, db, analyser)
        db.close_connection()

    def test_likes_vs_replies_analisis(self):
        v_id = 'g_sA8hYU3b8'
        ch_id = 'UConVfxXodg78Tzh5nNu85Ew'
        loader = Loader([ch_id])
        comments = loader.get_all_comments(ch_id, v_id)
        data = {
            'comments': comments,
            'videoId': v_id,
            'channelId': ch_id
        }
        db = DataBase()
        db.create_connection()
        get_likes_vs_replies_analisis(data, db)
        db.close_connection()

    def test_neq_pos_analisis(self):
        v_id = 'g_sA8hYU3b8'
        ch_id = 'UConVfxXodg78Tzh5nNu85Ew'
        loader = Loader([ch_id])
        comments = loader.get_all_comments(ch_id, v_id)
        analyser = Analyser()
        data = {
            'comments': comments,
            'videoId': v_id,
            'channelId': ch_id
        }
        db = DataBase()
        db.create_connection()
        get_neq_pos_analisis(data, db, analyser=analyser)
        db.close_connection()