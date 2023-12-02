from pysentimiento import create_analyzer
from pysentimiento.preprocessing import preprocess_tweet


class Analyser:
    def __init__(self, lang='en'):
        self._emotion_analyzer = create_analyzer(task="emotion", lang=lang)
        self._hate_speech_analyzer = create_analyzer(task="hate_speech", lang=lang)
        self._sentiment_analyzer = create_analyzer(task="sentiment", lang=lang)

    def analyse_emotion(self, data: str, lang='en'):
        data = preprocess_tweet(data, lang=lang)
        return self._emotion_analyzer.predict(data)

    def analyse_hate_speech(self, data: str, lang='en'):
        data = preprocess_tweet(data, lang=lang)
        return self._hate_speech_analyzer.predict(data)

    def analyse_sentiment(self, data: str, lang='en'):
        data = preprocess_tweet(data, lang=lang)
        return self._sentiment_analyzer.predict(data)

    def analyse_comments(self, comments: dict):
        res = dict()
        for entry in comments.values():
            # todo add lang recognition and translation
            text = entry['textOriginal']
            sentiment = self.analyse_sentiment(text)
            hate = self.analyse_hate_speech(text)
            emotion = self.analyse_emotion(text)
            ans = [emotion, sentiment, hate]
            res[entry['id']] = ans
        return res
