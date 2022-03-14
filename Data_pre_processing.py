import numpy as np 
import pandas as pd
import string
import re
import pyarabic.araby as araby
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.isri import ISRIStemmer #arabic stemmer

#read_data
data = pd.read_csv("new_dialect_dataset.csv")

def remove_Emojis(text) :
    re_exp_emoj_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F" 
        u"\U0001F300-\U0001F5FF"   
        u"\U0001F680-\U0001F6FF"   
        u"\U0001F1E0-\U0001F1FF"   
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  
        u"\u3030"
        u"\u26AB"
        u"\uF51E"
        u"\uF534"
        u"\u200f"                             
        u"\u23F0"
                    "]+",flags = re.UNICODE)
    return re.sub(re_exp_emoj_pattern, '', str(text))

def remove_username(text): 
  #Remove @username 
    text = re.sub('@[^\s]+', ' ', text)
    return text                        
                 
def remove_links(text): 
  #Remove www.* or https?://* to " "
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',text)
    return text

def remove_tags(text): 
   # Remove  #words
    text = re.sub(r'#([^\s]+)', r'\1', text)
    return text

def remove_punctuations(text):
    
    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ٪'''
    english_punctuations = string.punctuation
    all_punctuations = arabic_punctuations + english_punctuations
    translator = str.maketrans('', '', all_punctuations)
    
    return text.translate(translator)    


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)

def remove_other_punctuations (text):
    other_pun = re.compile(pattern = "["
       "\n" #new line 
       "+18"
       "18+"
       "+17"
       "17+"
       "\\n"
       "/n"
       "//n"
           "]+",flags = re.UNICODE)
    return re.sub(other_pun , '', str(text))

def remove_number(text) :
    numbers = [r'[0-9]+','[\u0660-\u0669]'] #regular expression of [English numbers , Arabic numbers]
    for i in numbers:
        text = re.sub(i,'',text)
    return text

def remove_eng_words (text):
    eng = ['[A-Z]*','[a-z]*','ğ','ı'] #regular expression of [English char , other latin char in tweets ]
    for i in eng :
        text = re.sub(i, '',text)
    return text 

def remove_stop_words(text):
    st = ISRIStemmer()
    text = word_tokenize(text) #tokenization
    stopwords_list = stopwords.words('arabic')
    more_stop_Words = ["و","ان","في","او","الي","انا","انت"]
    for i in more_stop_Words :
          stopwords_list.append(i)
    text = [st.stem(araby.strip_diacritics(w)) for w in text if araby.strip_diacritics(w) not in stopwords_list]
    return ' '.join(text)

def clean(text) :    
   #call all funcations
    data['text'] = data.text.map(lambda x:remove_Emojis(x))
    data['text'] = data.text.map(lambda x:remove_username(x))
    data['text'] = data.text.map(lambda x:remove_links(x))
    data['text'] = data.text.map(lambda x:remove_tags(x))
    data['text'] = data.text.map(lambda x:remove_punctuations(x))
    data['text'] = data.text.map(lambda x:remove_repeating_char(x))
    data['text'] = data.text.map(lambda x:remove_other_punctuations(x))
    data['text'] = data.text.map(lambda x:remove_number(x))
    data['text'] = data.text.map(lambda x:remove_eng_words(x))
    data['text'] = data.text.map(lambda x:remove_stop_words(x))
    
    return data['text'] 
