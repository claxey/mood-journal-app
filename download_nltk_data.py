import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """Download required NLTK data for the application."""
    required_data = [
        'punkt',
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords'
    ]
    
    for item in required_data:
        try:
            nltk.download(item, quiet=True)
            print(f"Successfully downloaded {item}")
        except Exception as e:
            print(f"Error downloading {item}: {str(e)}")

if __name__ == "__main__":
    download_nltk_data() 