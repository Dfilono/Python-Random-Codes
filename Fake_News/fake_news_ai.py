import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

input_file = ''

# Read in data
df = pd.read_csv(input_file)
labels = df.label

# Split the dataset
x_train, x_test, y_train, y_test = train_test_split(df['text'], labels, test_size = 0.2, random_state = 7)

# Init TfidfVectroizer
tfidf = TfidVectorizer(stop_words = 'english', max_df = 0.7)

# Fit and transform train set
tfidf_train = tfidf.fit_transform(x_train)

# Transform test set
tfidf_test = tfidf.transform(x_test)

# Init PassiveAgressiveClassifier
pac = PassiveAggressiveClassifier(max_iter = 50)
pac.fit(tfidf_train, y_train)

# Predict on test set
y_pred = pac.predict(tfidf_test)

# Calculate accuracy
score = accuracy_score(y_test, y_pred)
print(f'Accuracy: {round(score*100, 2)}%')

# Build Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels = ['FAKE', 'REAL'])
print(cm)