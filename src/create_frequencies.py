import os
import pathlib
import spacy
import re
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models.phrases import Phrases, Phraser

ROOT_DIR = pathlib.Path(__file__).parent.parent


# Set directories and create them if necessary
plain_text_dir = pathlib.Path().joinpath(ROOT_DIR,"data","plaintext")
structured_data_dir = pathlib.Path().joinpath(ROOT_DIR,"data","structured")
logging_dir = pathlib.Path().joinpath(ROOT_DIR,"logs")


nlp = spacy.load("es_core_news_sm", disable=['parser', 'ner'])
nlp.Defaults.stop_words |= {"y","a","o"}
nlp.add_pipe(nlp.create_pipe('sentencizer'))

files = os.listdir(plain_text_dir)
paths = [ plain_text_dir.joinpath(file) for file in files]

# Get list of all sentences
sentences = list()
for path in paths:
    # Open text file
    with open(path,"r",encoding="UTF-8") as f: 
        text = f.read()
        
    # Load as spacy object
    doc = nlp(text)
    for sent in doc.sents:
        # convert to lemma and remove punctuation, spaces, stop words and proper nouns
        sent = [t.lemma_.lower() for t in sent if not (t.is_punct or t.is_space or t.is_stop or t.pos_ == "PROPN")]
        sent = [ re.sub("^\W+|\W+$","",lemma) for lemma in sent ] 
        
        for old,new in [("casar","casa"),("callar","calle"),("finar","fin"),("manir","mano")]:
            sent = [ re.sub(old,new,lemma) for lemma in sent ]
            
        sentences.append(sent) 
        
# get all unigrams
ugrams = [ item for sublist in sentences for item in sublist]
ugrams_freq = pd.Series(ugrams).value_counts()
path = structured_data_dir.joinpath("unigrams_freq.tsv")
ugrams_freq.to_csv(path,sep="\t")

# get all bigrams
phrases = Phrases(sentences, min_count=1, threshold=1)
w_bigrams = [phrases[x] for x in sentences]
bigrams = [ item for sublist in w_bigrams for item in sublist if item.count("_") == 1]
bigrams_freq = pd.Series(bigrams).value_counts()
path = structured_data_dir.joinpath("bigrams_freq.tsv")
bigrams_freq.to_csv(path,sep="\t")

# get all trigrams
trigram_model = Phrases(w_bigrams, min_count=1, threshold=1)
w_trigrams = [trigram_model[x] for x in w_bigrams]
trigrams = [ item for sublist in w_trigrams for item in sublist if item.count("_") == 2]
trigrams_freq = pd.Series(trigrams).value_counts()
path = structured_data_dir.joinpath("trigrams_freq.tsv")
trigrams_freq.to_csv(path,sep="\t")