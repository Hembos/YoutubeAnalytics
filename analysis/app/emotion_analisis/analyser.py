from collections import defaultdict

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

    def analyse_comments(self, comments: dict, analysis_types: dict):
        res = dict()
        frequency = defaultdict(int)
        for entry in comments.values():
            # todo add translation
            text = entry['textOriginal']
            ans = dict()
            if len(text) > 200:
                text = text[:200]
            if analysis_types.get('lang') is not None:
                lang = self.recognise_lang(text)
                ans['lang'] = lang
            # if lang not in ['es', 'en', 'it', 'pt']:
            # text = self.translate(text)
            # lang = 'en'
            if analysis_types.get('sentiment') is not None:
                sentiment = self.analyse_sentiment(text)
                ans['sentiment'] = sentiment
            if analysis_types.get('hate') is not None:
                hate = self.analyse_hate_speech(text)
                ans['hate'] = hate
            if analysis_types.get('emotion') is not None:
                emotion = self.analyse_emotion(text)
                ans['emotion'] = emotion
            if analysis_types.get('word_count') is not None:
                words = "".join(c for c in text if c.isalnum() or c.isspace())
                words = words.lower().split()
                for word in words:
                    frequency[word] += 1
            res[entry['id']] = ans
        if analysis_types.get('word_count') is not None:
            res['word_count'] = frequency
        self.result = res
        return res


