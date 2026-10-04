import re
import nltk

from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


stemmer = PorterStemmer()
stop_words = set(ENGLISH_STOP_WORDS)


def preprocess_text(text):
    """
    Clean and normalize text for NLP processing.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Tokenization
    words = text.split()

    # Remove stopwords
    words = [
        word for word in words
        if word not in stop_words
    ]

    # Stemming using NLTK
    words = [
        stemmer.stem(word)
        for word in words
    ]

    return " ".join(words)