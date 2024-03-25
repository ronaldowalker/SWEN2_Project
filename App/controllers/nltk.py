import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def setup_nltk():
    nltk.download('vader_lexicon')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    return

from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def analyze_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]  # Remove punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    processed_text = ' '.join(tokens)
    return processed_text

def analyze_sentiment(text):
    processed_text = analyze_text(text)

    scores = analyzer.polarity_scores(processed_text)
    print("scores: "+ str(scores))
    return scores

