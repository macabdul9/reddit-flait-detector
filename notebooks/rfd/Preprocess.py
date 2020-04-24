import nltk
from emot import EMOTICONS, EMO_UNICODE, UNICODE_EMO
import string
import autocorrect
import re
nltk.download('stopwords')
from nltk.corpus import stopwords
import emoji
from autocorrect import Speller


# convert emotion to words
# def convert_emoticons(text):
#     for emot in EMOTICONS:
#         text = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), text)
#     return text 

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
    if not text or len(text) < 1:
        return " "
    STOPWORDS = stopwords.words('english')
    custom =["http", "https", "www", "com", "reddit", "r", "html", "php", "png", "jpg", "gif", "jpeg"]
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

    # replace emoji/emoticons with words
    # text = convert_emoticons(text)
    # text = convert_emojis(text)
    
    # replace punctuation characters with spaces
    filters='!"\'#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    translate_dict = dict((c, " ") for c in filters)
    translate_map = str.maketrans(translate_dict)
    text = text.translate(translate_map)

     
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    # text = correct_spellings(text)

    return text