import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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
    # sample output: {'neg': 0.0, 'neu': 0.608, 'pos': 0.392, 'compound': 0.7003}
    points = 0 
    print(scores)
    if((scores['pos'] >= 0.5) or (scores['compound'] >= 0.1)):  #  means that the text is mostly positive
      points = scores['pos'] * 10
    else:
      points = scores['neg'] * -10
    print("points: "+ str(points))
    # return points
  
    return points
