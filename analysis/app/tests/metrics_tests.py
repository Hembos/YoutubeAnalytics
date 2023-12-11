import unittest

from analysis.app.emotion_analisis.analyser import Analyser


class TestAnalisis(unittest.TestCase):
    def test_sentiment(self):
        test_comment_text = 'Love this video'
        analyser = Analyser()
        res = analyser.analyse_sentiment(test_comment_text)

if __name__ == '__main__':
    unittest.main()