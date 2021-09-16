from os import link
import flask
from flask.globals import request
from flask import Flask, render_template
import numpy as np

from inputExtractor import InputExtractor
from textFormater import TextFormater
# library used for prediction
import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle

import sys
import logging

app = Flask(__name__, template_folder = 'templates')

link_active = None
# render home template
@app.route('/')
def main():
    return(render_template('home.html', title = 'Home'))

# load nn model    
model = load_model('model/full_bi_lstm_model.h5')
# load pickle file
phrases_vectorizer, context_vectorizer = pickle.load(open('model/custom_vectorizer.pkl', 'rb'))

def limitElement(x, avg_element):
    '''
    We will cut all of the input into a the average length of the whole training set
    '''
    len_x = len(x)
    if len_x < avg_element:
        diff = avg_element-len_x
        result = x[:len_x] + [None]*diff

    elif len_x >= avg_element:
        result = x[:avg_element]
    return result
    
def encoding(x, vectorizer, avg_element):
    '''
    Encoder of the text input
    '''
    encoded = []
    final_features = limitElement(x, avg_element)
    for feature in final_features:
        if feature in vectorizer.keys():
            encoded.append(vectorizer[feature])
        elif feature not in vectorizer.keys():
            encoded.append(vectorizer['Unknown'])
        else:
            encoded.append(vectorizer[None])
    return encoded

def my_func(arg):
    '''
    Convert to tensorflow tensor format
    '''
    arg = tf.convert_to_tensor(arg, dtype=tf.int32)
    return arg

def input_pipeline(text):
    skills_extractor = InputExtractor(1)
    text_formater = TextFormater()

    text_formatted = text_formater.formats(text)
    phrases_text, context_text = skills_extractor.extract(text_formatted)

    avg_element_length_phrases = 113
    avg_element_length_context = 113

    phrases_text_encoded = [encoding(phrases_text, phrases_vectorizer, avg_element_length_phrases)]
    context_text_encoded = [encoding(context_text, context_vectorizer, avg_element_length_context)]

    text_phrases_input = my_func(phrases_text_encoded)
    text_context_input = my_func(context_text_encoded)
    return text_phrases_input, text_context_input

@app.route('/form')
def form():
    show_prediction = False
    link_active = 'Form'
    return(render_template('form.html', title = 'Form', show_prediction = show_prediction, link_active = link_active))

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering prediction result.
    '''
    link_active = 'Result'
    show_prediction = True

    # retrieve data
    skills = request.form.get('skills_input')
    
    phrases_input, context_input = input_pipeline(skills)

    prediction = model.predict({'phrases_inputs':phrases_input, 'context_inputs':context_input})
    prob_res = float(prediction.max())
    prob = round(prob_res, 3)

    output = {
        0:'Data Analyst', 1:'Data Engineer', 2:'Data Scientist'
    }
    prediction_res = output[np.argmax(prediction)]

    return render_template('form.html', title = 'Prediction', show_prediction = show_prediction, prediction_class = prediction_res, prediction_prob = prob, skills = skills, link_active = link_active)

if __name__ == '__main__':
    app.run(debug = True)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
