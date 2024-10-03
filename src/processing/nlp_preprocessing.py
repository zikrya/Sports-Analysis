import spacy
import re
import string
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """
    Cleans up the text by removing unnecessary content such as stopwords, punctuation,
    and irrelevant sections like image credits or social media links.
    """
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    text = re.sub(r"share.*?via.*?email", "", text)
    text = re.sub(r"mandatory credit.*?(?:images|photos)?", "", text)
    text = re.sub(r"(http|https)://[^\s]+", "", text)
    text = re.sub(r"\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}", "", text)
    text = ''.join([char for char in text if char not in string.punctuation])
    text = re.sub(r'\d+', '', text)

    return text

def tokenize_text(text):
    """
    Tokenizes the text into individual words using spaCy's tokenizer and filters out low-relevance tokens.
    """
    doc = nlp(text)
    tokens = [token.text for token in doc if token.text not in STOP_WORDS and token.is_alpha and len(token.text) > 2]

    keywords = set(['game', 'team', 'match', 'score', 'win', 'loss', 'yard', 'pass', 'touchdown'])
    tokens = [token for token in tokens if token not in keywords]

    return list(set(tokens))

def extract_entities(text):
    """
    Extracts named entities like player names, team names, and game events using spaCy's NER.
    Filters only relevant entity types and discards repeated entries.
    """
    doc = nlp(text)
    relevant_labels = ['PERSON', 'ORG', 'DATE', 'GPE']

    entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in relevant_labels]

    unique_entities = list(set(entities))

    return unique_entities

def preprocess_article(article_content):
    """
    Takes in the raw article content, cleans it, tokenizes it, and performs NER to extract relevant entities.
    """
    cleaned_text = clean_text(article_content)
    tokens = tokenize_text(cleaned_text)
    entities = extract_entities(cleaned_text)

    return {
        "cleaned_text": cleaned_text,
        "tokens": tokens,
        "entities": entities
    }
