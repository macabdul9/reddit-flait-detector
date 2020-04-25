import praw
import string
import re
import emoji
from autocorrect import Speller

# create a list of stopwrods manually  it will save nltk(or similar package) import 

STOPWORDS =  ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
"you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 
'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 
'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 
'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 
"aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 
'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', 
"wouldn't", "it's", "http", "https", "com", "twitter", "reddit", "www"]


# convert emoji to words
def convert_emojis(text):
    return emoji.demojize(text)


# correct spelling
spell = Speller()
def correct_spellings(text):
    return spell.autocorrect_sentence(text)


def clean_text(text):
    """
    Function to perform some cleaning removing the stop words
    params: 
        text : text data
    returns: cleaned text
    """
    # STOPWORDS = stopwords.words('english')
    # custom =["http", "https", "com", "twitter", "facebook", "reddit", "google", "api", "instagram", "www", 'gmail', "yahoo", "proton"]
    # STOPWORDS += custom
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

def scrap_comments(sub, limit=10):
    """
        Function to scrap the top-10 comments(as it was done in data collection for training data)
        Params
            sub: submission instance
        Returns: top-10(if num_comments > 10 or top x) comments combined into single string with space
    """
    # agg into a list
    comments_body = []

    if sub.num_comments > 0:
        for i, comment in enumerate(sub.comments.list()):
            # There may be some comments which has no body
            try : 
                comments_body.append(comment.body)
            except:
                comments_body.append('')
            if i==limit:
                break

    return " ".join(comments_body)


def scrap_data(sub):
    """
        Function to collect submission data(except comment)
        Params
            sub: submission instance
        Returns: collected text data      
    """
    data = " ".join([sub.title, sub.url, sub.selftext])
    flair = sub.link_flair_text
    comments = scrap_comments(sub)
    # print(comments)
    data = data + " " + comments
    return clean_text(data), flair
    

def get_data(url):
    """
        Function to scrap the submission from url
        Params
            url: url/link of a submission 
        Returns: scrapped data
    """
    api = praw.Reddit(
        client_id='pw8WCM92ySUjsQ', 
        client_secret='y0MJFMWBtHXMLW2-3B2upsU2jYQ', 
        user_agent='reddit-scrap', 
        username='macabdul9', 
        password='Sudo$0#1'
    )
    subm = api.submission(url=url)
    return scrap_data(subm)