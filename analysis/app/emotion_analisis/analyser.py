from pysentimiento import create_analyzer
from pysentimiento.preprocessing import preprocess_tweet
from transformers import pipeline


class Analyser:
    def __init__(self, lang='en'):
        self._emotion_analyzer = create_analyzer(task="emotion", lang=lang)
        self._hate_speech_analyzer = create_analyzer(task="hate_speech", lang=lang)
        self._sentiment_analyzer = create_analyzer(task="sentiment", lang=lang)
        self._language_recognizer = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")
        # self._translator = Translator()
        self.result = None

    def recognise_lang(self, text: str) -> str:
        return self._language_recognizer(text)

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
            # todo add translation
            text = entry['textOriginal']
            if len(text) > 200:
                text = text[:200]
            lang = self.recognise_lang(text)
            # if lang not in ['es', 'en', 'it', 'pt']:
            # text = self.translate(text)
            # lang = 'en'
            sentiment = self.analyse_sentiment(text)
            hate = self.analyse_hate_speech(text)
            emotion = self.analyse_emotion(text)
            ans = {"emotion": emotion, "sentiment":
                sentiment, "hate": hate, "lang": lang}
            res[entry['id']] = ans
        self.result = res
        return res


