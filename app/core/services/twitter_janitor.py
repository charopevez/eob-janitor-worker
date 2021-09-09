
import pandas as pd
import numpy as np
import json, re, nltk
from nltk.stem.porter import PorterStemmer

def clean_users(dataframe):
    """ extect users mentioned in tweet """
    # get mentions list
    dataframe['mentions'] = np.vectorize(
        extract_pattern)(dataframe['full_text'], "@[\w]*")
    #dataframe['mentions'] = dataframe['mentions'].apply(convert_to_list)
    dataframe['clean_text'] = np.vectorize(
        remove_pattern)(dataframe['full_text'], "@[\w]*")
    return dataframe


def clean_character(dataframe):
    """ clean special characters """
    dataframe['clean_text'] = dataframe['clean_text'].str.lower().str.replace("[^a-zA-Z#]", " ")
    return dataframe


def clean_stopword(dataframe):
    """clean stop words"""
    dataframe['clean_text']=dataframe['clean_text'].apply(lambda x: " ".join(w for w in x.split() if len(w)>3 ))
    return dataframe

def clean_url(dataframe):
    # delete urls list
    #dataframe['clean_text'] = dataframe['clean_text'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')
    dataframe['urls'] = np.vectorize(
        extract_pattern)(dataframe['clean_text'], "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    #dataframe['urls'] = dataframe['urls'].apply(convert_to_list)
    dataframe['clean_text'] = np.vectorize(
        remove_pattern)(dataframe['clean_text'], "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    return dataframe


def tokenize(dataframe):
    """ tokenize tweets """
    tokens = dataframe['clean_text'].apply( lambda x: x.split())
    # stemmerized tokens
    streamer= PorterStemmer()
    dataframe['tokens']= tokens.apply(lambda sentence: [streamer.stem(word) for word in sentence ])
    return dataframe

def get_hashtags(dataframe):
    """ extract hashtags from tweets """
    dataframe['hashtags'] = np.vectorize(
        extract_pattern)(dataframe['full_text'], "#[\w]*")
    #dataframe['hashtags'] = dataframe['hashtags'].apply(convert_to_list) 
    return dataframe

def clean(data):
    """ start data cleaning """
    #! create dataframe from dictionary
    df=pd.DataFrame(data)
    #? clean twitter users
    df_users = clean_users(df)
    #?clean urls
    df_urls = clean_url(df_users)
    #? clean special characters
    df_cleaned_chars = clean_character(df_urls)
    #? clean stopwords
    df_cleaned_stopwords = clean_stopword(df_cleaned_chars)
    #? tokenize msg
    df_tokenized=tokenize(df_cleaned_stopwords)
    #? get used hashtags
    ready_to_use=get_hashtags(df_tokenized)
    #? return prepared data
    return ready_to_use.to_dict('records')


def extract_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    input_txt = ""
    for word in r:
        input_txt += word+','
    return input_txt


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for word in r:
        input_txt = re.sub(word, "", input_txt)
    return input_txt

def convert_to_list(text)->[]:
    v_list=text.split(',')
    return [string for string in v_list if string != ""]

