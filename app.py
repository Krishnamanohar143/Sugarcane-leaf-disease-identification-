from flask import Flask, render_template, request
import numpy as np
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from keras.preprocessing.text import Tokenizer
import pickle
from tensorflow.python.keras import utils
from tensorflow.python.keras.models import load_model
from flask_session import Session
app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))
MAX_LEN = 100  
model = load_model(r'my_model.h5')

tokenizer = None  


def text_preprocess(text, stop_words=False):
    text = re.sub(r'\W+', ' ', text).lower()
    tokens = word_tokenize(text)
    
    if stop_words:
        tokens = [token for token in tokens if token not in STOPWORDS]
    
    return tokens


def predict_sentiment(text):
    text_prepr = text_preprocess(text)
    sequence = tokenizer.texts_to_sequences([text_prepr])
    pad = utils.pad_sequences(sequence, maxlen=MAX_LEN)
    prediction = model.predict(pad)[0]
    label = labels_to_emotions[prediction.argmax()]
    return label

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.form['text']
    sentiment = predict_sentiment(text)
    return sentiment

if __name__ == '__main__':
    # Load the tokenizer here
    DICT_SIZE=1000
    tokenizer = Tokenizer(num_words=DICT_SIZE)
    tokenizer.word_index = {'word': 1, 'another': 2, 'example': 3}  # Replace with your tokenizer
    
    # Define emotions to labels mapping here
    labels_to_emotions = {0: 'anger', 1: 'love', 2: 'fear', 3: 'joy', 4: 'sadness', 5: 'surprise'}
    
    app.run(debug=True)
