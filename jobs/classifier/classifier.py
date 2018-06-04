import re
from sklearn.externals import joblib
from .utilities import clean_str
from textblob import Word

model = joblib.load('model.pkl')
vect = joblib.load('vectorizer.pkl')

def classify(article):
    '''Classifies an article using the already trained prediction model'''
    article = [' '.join([Word(word).lemmatize() for word in clean_str(article).split()])]
    features = vect.transform(article)

    return model.predict(features)[0]
