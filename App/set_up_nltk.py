import nltk
import os

def setup_nltk():
    nltk.data.path.append(os.path.abspath("nltk_data"))  # Adjust path as needed
    nltk.download('vader_lexicon', download_dir="nltk_data")

if __name__ == "__main__":
    setup_nltk()
