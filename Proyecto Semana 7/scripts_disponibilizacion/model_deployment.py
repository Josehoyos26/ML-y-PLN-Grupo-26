#!/usr/bin/python
from tensorflow.keras.models import load_model
import pandas as pd
import joblib
import sys
import os
import json
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Se obtiene el dataset con el que se entreno el Tfidf Vectorizer desde un repositorio externo o localmente
# dataTraining = pd.read_csv('https://github.com/albahnsen/MIAD_ML_and_NLP/raw/main/datasets/dataTraining.zip', encoding='UTF-8', index_col=0)
dataTraining = pd.read_csv('dataTraining.csv', encoding='UTF-8', index_col=0)

stop_words_ = list(set(stopwords.words('english')))
wordnet_lemmatizer = WordNetLemmatizer()
lemmatizer = WordNetLemmatizer()
def split_into_lemmas(text):
    text = text.lower()
    words = text.split()
    return [wordnet_lemmatizer.lemmatize(word) for word in words]

cols = ['p_Action', 'p_Adventure', 'p_Animation', 'p_Biography', 'p_Comedy', 'p_Crime', 'p_Documentary', 'p_Drama', 'p_Family',
        'p_Fantasy', 'p_Film-Noir', 'p_History', 'p_Horror', 'p_Music', 'p_Musical', 'p_Mystery', 'p_News', 'p_Romance',
        'p_Sci-Fi', 'p_Short', 'p_Sport', 'p_Thriller', 'p_War', 'p_Western']

# Vectorizamos los comentarios 
vect = TfidfVectorizer(max_features=10000,stop_words=stop_words_,analyzer=split_into_lemmas)
X_dtm = vect.fit_transform(dataTraining['plot'])

# Carga del Vectorizador entrenado
# vect = joblib.load(os.path.dirname(__file__) + '/vect_gender_movies.pkl') 

# Carga del Modelo
clf = load_model(os.path.dirname(__file__) + '/clf_gender_movies.h5') 

def clf_gender_movie(year, title, plot):

    # Input Crudo
    raw_data = pd.DataFrame([[year, title, plot]], columns=['year', 'title', 'plot'])

    # Forma de Input que entiende el modelo de clasificacion:
    x = vect.transform(raw_data['plot'])
    x = x.toarray()
    # x = raw_data

    # Make prediction
    p1 = clf.predict(x)
    p1 = pd.DataFrame(p1, columns=cols)
    p1 = p1.to_json(orient='records')
    p1 = json.loads(p1)
    return p1


if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print('Please add the correct movie features: Year, title and plot.')
    else:
        year = sys.argv[1]
        title = sys.argv[2]
        plot = sys.argv[3]        
        result = clf_gender_movie(year, title, plot)
