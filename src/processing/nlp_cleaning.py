import re

def clean_news_content(raw_content):
    """
    Cleans the raw content of news articles by removing URLs, image galleries, share links, and other irrelevant text.
    """
    cleaned_content = re.sub(r'http\S+', '', raw_content)

    cleaned_content = re.sub(r'Share\s+this\s+.*?via\s+.*?\n', '', cleaned_content, flags=re.IGNORECASE)

    cleaned_content = re.sub(r'image\s+gallery.*?\n', '', cleaned_content, flags=re.IGNORECASE)

    cleaned_content = re.sub(r'on\s+(Facebook|Twitter|via\s+text\s+message|via\s+email)\s+', '', cleaned_content, flags=re.IGNORECASE)

    cleaned_content = re.sub(r'\b(more|gallery|on Facebook|on Twitter|Share|via\s+.*?|Mandatory Credit:.*?|more\n\n)+', '', cleaned_content, flags=re.IGNORECASE)

    cleaned_content = re.sub(r'\n+', '\n', cleaned_content).strip()

    return cleaned_content
raw_article = """
The Atlanta Falcons and Kansas City Chiefs faced off in prime time on NBC's Sunday Night Football.
Despite a close game, the Chiefs escaped with a 22-17 win over the Falcons.
https://thefalconswire.usatoday.com/gallery/falcons-chiefs-kelce-swift-nfl/
image gallery
on Facebook on Twitter via text message via email
more
Share this image gallery
"""
cleaned_article = clean_news_content(raw_article)
print(cleaned_article)
