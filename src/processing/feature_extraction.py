import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")

analyzer = SentimentIntensityAnalyzer()

def extract_entities(text):
    """
    Extracts named entities such as players, teams, and game stats from the article text.
    Focuses on Atlanta Falcons and Philadelphia Eagles content.
    """
    doc = nlp(text)
    entities = {
        "players": [],
        "teams": [],
        "game_stats": []
    }

    # Extract relevant entities like players and teams
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["players"].append(ent.text)
        elif ent.label_ == "ORG" and ("falcons" in ent.text.lower() or "eagles" in ent.text.lower()):
            entities["teams"].append(ent.text)

    # Manually extract game stats based on custom patterns (e.g., 65-yard run, touchdown)
    tokens = [token.text for token in doc]
    for i, token in enumerate(tokens):
        if "yard" in token or "touchdown" in token:
            entities["game_stats"].append(" ".join(tokens[max(i-3, 0):i+1]))  # Capture surrounding tokens for context

    return entities

def extract_context(text):
    """
    Extracts context around key events by parsing dependencies between named entities and their actions.
    Example: "Saquon Barkley rushed for 65 yards."
    """
    doc = nlp(text)
    actions = []

    for token in doc:
        # Focus on relevant actions like scoring, rushing, running, intercepting, etc.
        if token.pos_ == "VERB" and token.lemma_ in ["score", "rush", "run", "intercept", "tackle"]:
            subject = [child for child in token.children if child.dep_ == "nsubj"]
            obj = [child for child in token.children if child.dep_ == "dobj"]

            if subject and obj:
                actions.append(f"{subject[0].text} {token.text} {obj[0].text}")
            elif subject:
                actions.append(f"{subject[0].text} {token.text}")

    return actions

def analyze_sentiment(text):
    """
    Performs sentiment analysis on the text to determine the tone behind specific events.
    """
    sentiment = analyzer.polarity_scores(text)
    return sentiment

def process_article(text):
    """
    Main function to extract entities, context, and sentiment from an article's text.
    """
    entities = extract_entities(text)
    context = extract_context(text)
    sentiment = analyze_sentiment(text)

    return {
        "entities": entities,
        "context": context,
        "sentiment": sentiment
    }

