from .utilities import clean_str
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import Word
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sys import argv

data = pd.read_csv(argv[1])
news = data['news'].tolist()
categories = data['category'].tolist()

for index, value in enumerate(news):
    news[index] = ' '.join([Word(word).lemmatize() for word in clean_str(value).split()])

vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
features = vectorizer.fit_transform(news)
labels = np.array(categories)
joblib.dump(vectorizer, 'vectorizer.pkl')

model = RandomForestClassifier(n_estimators=300, max_depth=150, n_jobs=1)
model.fit(features, labels)
joblib.dump(model, 'model.pkl')
