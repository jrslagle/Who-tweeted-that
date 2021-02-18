import spacy

class NLP():
    def __init__(self):
        # Load English pipeline
        self.nlp = spacy.load('en_core_web_sm')  # small model, 2.6 s load time (output vector.shape = (96,))
        # self.nlp = spacy.load('en_core_web_trf')  # big model, 3.9 s load time, vector doesn't work
        # https://spacy.io/models

    def tweet_to_vec(self, tweet_text):
        # print(f"Tweet: '{tweet_text}'")
        doc = self.nlp(tweet_text)
        # print([(w.text, w.pos_) for w in doc])  # prints each word and it's part of speech
        return doc.vector
