from nltk.stem import SnowballStemmer, WordNetLemmatizer, wordnet
import re
import nltk


# nltk.download(wordnet)

# The goal is to tokenize the arxiv.json file
# apply it to the summary(abstract),title  getting it ready for the inverted index


class Tokenizer:
    def __init__(self, stemming: bool = False, lemmatization: bool = False):
        if stemming and lemmatization:
            raise ValueError("Stemming and lemmatization can't be both True !")
        # \W+ regex  finds any non "word" such as spaces ,symbols,punctuations etc...
        self.pattern = re.compile(r"\W+")
        self.stemming = stemming
        self.lemmatization = lemmatization

        self.stemmer = SnowballStemmer(language="english") if stemming else None
        self.lemmatize = WordNetLemmatizer() if lemmatization else None

    def _validate_input(self):
        pass

    def tokenize(self, text: str) -> list[str]:
        if not text:
            return []

        text_lwc = text.lower()
        tokens = self.pattern.split(text_lwc)

        # Removes empty tokens
        processed_tokens = []
        for token in tokens:
            if not token:
                continue
            if self.stemming and self.stemmer is not None:
                token = self.stemmer.stem(token)
            if self.lemmatization and self.lemmatize is not None:
                # add POS tag  later
                token = self.lemmatize.lemmatize(token)
            processed_tokens.append(token)

        return processed_tokens
