import nltk
import string
import autocorrect
import re
nltk.download('stopwords')
from nltk.corpus import stopwords
import emoji
from autocorrect import Speller

# convert emoji to words
def convert_emojis(text):
    return emoji.demojize(text)


# correct spelling
spell = Speller()
def correct_spellings(text):
    return spell.autocorrect_sentence(text)


def clean_text(text):
    """
    params: 
        - text : text data
    returns: cleaned text

    """
    STOPWORDS = stopwords.words('english')
    custom =["http", "https", "com", "twitter", "facebook", "reddit", "google", "api", "instagram", "www", 'gmail', "yahoo", "proton"]
    STOPWORDS += custom
    # convert text to lowercase
    text = text.strip().lower()

   

    # conveert 
    # remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # remove the characters [\], ['] and ["] , 
    text = re.sub(r"\\", " ", text)    
    text = re.sub(r"\'", " ", text)    
    text = re.sub(r"\"", " ", text)
    text = re.sub(" \d+", " ", text)
    
    # remove nums
    text = re.sub('[0-9]+', '', text)
    
    # remove white spaces 
    text = re.sub(r"\s{2,}", " ", text)

    # replace emoji with words
    text = convert_emojis(text)
    
    # replace punctuation characters with spaces
    filters='!"\'#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    translate_dict = dict((c, " ") for c in filters)
    translate_map = str.maketrans(translate_dict)
    text = text.translate(translate_map)

     
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    # text = correct_spellings(text)

    return text