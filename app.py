import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import json
import pickle
import math
from scrape import c
from Related_news import find

vectorizer = pickle.load(open("tfidf_vectorizer.pickle",'rb'))
model = pickle.load(open("PA.pickle",'rb'))


import re
import string
def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text
def getfakeness(num):
  num = num * 100
  if(num > 90):
    return 'Real'
  elif(num > 75):
    return 'Mostly Real'
  elif(num > 50):
    return 'May be Real'
  elif(num > 40):
    return 'Mostly Fake'
  else:
    return 'Fake'

app = Flask(__name__)

@app.route("/predict",methods = ['POST'])
def predict():
    data = request.json
    link = data["link"]
    test = c(link)
    test_x = wordopt(test[0])
    tfidf_x = vectorizer.transform([test_x])
    pred = model.predict(tfidf_x)
    result =[]
    result.append(math.ceil(model._predict_proba_lr(tfidf_x)[0][1]*100))
    output = {'results': result[0],'head':test[1]}
    #print(getfakeness(model._predict_proba_lr(tfidf_x)[0][1]))
    return jsonify(results=output['results'],heading = output['head'])

@app.route("/related",methods = ['POST'])
def related():
    data = request.json
    link = data["link"]
    result = find(link)
    for dic in result:
      l = dic["link"]
      test = c(l)
      test_x = wordopt(test[0])
      tfidf_x = vectorizer.transform([test_x])
      pred = model.predict(tfidf_x)
      real_fake =[]
      real_fake.append(math.ceil(model._predict_proba_lr(tfidf_x)[0][1]*100))
      dic["real"] = real_fake[0]

    return jsonify(news_1 = result[3], news_2 = result[2], news_3 = result[1],news_4 = result[0])


if __name__ == '__main__':
    app.run(debug=True)