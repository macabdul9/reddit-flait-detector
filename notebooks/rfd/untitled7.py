import re
import string
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk import pos_tag


import pandas as pd
import os
import re
import numpy as np
import gc
import json
from tqdm import tqdm 
from edm import report
import collections 
from collections import Counter

#NLTK
import nltk
from nltk.corpus import stopwords
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams

# spaCy based imports
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
eng_stopwords = STOP_WORDS


#Etc
import matplotlib.pyplot as plt 
import seaborn as sns
import time
import operator 

def count_regexp_occ(regexp="", text=None):
    """ Simple way to get the number of occurence of a regex"""
    return len(re.findall(regexp, text))

def numerical_features(df):
    
    eng_stopwords = stopwords.words()
    
    print(">> Generating Numerical Features For Text")
    print("Calculating char_count ...")
    df['char_count'] = df['text'].apply(len)   
    
    df['num_words'] = df['text'].apply(lambda comment: len(comment.split()))

  
    df['capitals'] = df['text'].apply(lambda comment: sum(1 for c in comment if c.isupper()))
    
    df['caps_vs_length'] = df.apply(lambda row: float(row['capitals'])/float(row['char_count']),
                                axis=1)
    df['num_exclamation_marks'] = df['text'].apply(lambda comment: comment.count('!'))
    
    df['num_question_marks'] = df['text'].apply(lambda comment: comment.count('?'))
    print("Calculating num_punctuation ...")
    df['num_punctuation'] = df['text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]))
    
    
    df["num_stopwords"] = df["text"].apply(lambda x: len([w for w in str(x).lower().split() if w in eng_stopwords]))

    
    df['num_symbols'] = df['text'].apply(
    lambda comment: sum(comment.count(w) for w in '*&$%'))
    
    print("Calculating mean_word_len ...")
    df['mean_word_len'] = df['text'].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
    
    df['num_unique_words'] = df['text'].apply(
    lambda comment: len(set(w for w in comment.split())))
    
    df['words_vs_unique'] = df['num_unique_words'] / df['num_words']
    print("Calculating num_smiles ...")
    df['num_smilies'] = df['text'].apply(
    lambda comment: sum(comment.count(w) for w in (':-)', ':)', ';-)', ';)')))
    
    # Count number of \n
    df["ant_slash_n"] = df["text"].apply(lambda x: count_regexp_occ(r"\n", x))
    
    # Check for time 
    print("Calculating timstamp ...")
    df["has_timestamp"] = df["text"].apply(lambda x: count_regexp_occ(r"\d{2}|:\d{2}", x))
    
    # Check for http links
    print("Calculating https ...")
    df["has_http"] = df["text"].apply(lambda x: count_regexp_occ(r"http[s]{0,1}://\S+", x))

    return df

# call in that order 

def tag_part_of_speech(text):
    text_splited = text.split(' ')
    text_splited = [''.join(c for c in s if c not in string.punctuation) for s in text_splited]
    text_splited = [s for s in text_splited if s]
    pos_list = pos_tag(text_splited)
    noun_count = len([w for w in pos_list if w[1] in ('NN','NNP','NNPS','NNS')])
    adjective_count = len([w for w in pos_list if w[1] in ('JJ','JJR','JJS')])
    verb_count = len([w for w in pos_list if w[1] in ('VB','VBD','VBG','VBN','VBP','VBZ')])
    return[noun_count, adjective_count, verb_count]

def pos_features(df):
    print(">> Generating POS Features")
    for df in ([df]):
        print("Calculating nouns ...")
        df['nouns'], df['adjectives'], df['verbs'] = zip(*df['text'].apply(
            lambda comment: tag_part_of_speech(comment)))
        df['nouns_vs_length'] = df['nouns'] / df['char_count']
        df['adjectives_vs_length'] = df['adjectives'] / df['char_count']
        print("Calculating verb_vs_length ...")
        df['verbs_vs_length'] = df['verbs'] /df['char_count']
        df['nouns_vs_words'] = df['nouns'] / df['num_words']
        print("Calculating nouns ...")
        df['adjectives_vs_words'] = df['adjectives'] / df['num_words']
        print("Calculating verb_vs_words ...")
        df['verbs_vs_words'] = df['verbs'] / df['num_words']
        # More Handy Features
        df["count_words_title"] = df["text"].apply(lambda x: len([w for w in str(x).split() if w.istitle()]))
        print("Calculating punc_percent ...")
        df['punct_percent']= df['num_punctuation']*100/df['num_words']
        
    return df