# -*- coding: utf-8 -*-
"""reva_hack_tww_centimental_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14hSj5M5rsyKvH5lXPrsBa-Eo-3DFiA7M
"""

# !pip install transformers

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
 
 
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# Tasks:
# emoji, emotion, hate, irony, offensive, sentiment
# stance/abortion, stance/atheism, stance/climate, stance/feminist, stance/hillary

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)


# download label mapping
labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]


# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.save_pretrained(MODEL)

def sentmm(text):
    # text = """you are a  boy"""
    respp=[]
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores

# !pip install snscrape

import statistics
import snscrape.modules.twitter as sntwitter
import pandas as pd
zzz=[]

def tweett(query,limit):
  tweets = []
  tweetscore = []
  zzz1=[]

  for tweet in sntwitter.TwitterSearchScraper(query).get_items():
      # print(tweet.content)
      # break
      if len(tweets) == limit:
          break
      else:
          tweets.append([tweet.date, tweet.content])
          x=sentmm(tweet.content)
          tweetscore.append([x[0],x[1],x[2]])

  sc = pd.DataFrame(tweetscore, columns=['-ve', '*','+ve'])
  df = pd.DataFrame(tweets, columns=['Date', 'Tweet'])
  # print(df)
  # mn=statistics.mean(tweetscore)
  zzz1.append([sc["-ve"].mean(),sc["*"].mean(),sc["+ve"].mean()])
  zzz1
  return zzz1


# !pip install pyngrok

from flask import Flask, redirect, url_for
from flask import Flask, render_template ,send_file
from pyngrok import ngrok
from flask import request

port_no = 5000
app = Flask(__name__)
ngrok.set_auth_token("1msOb6Pmqpiqu93U0whQYK2QcP4_QgVjEAfLjZw8Bcw1QEAX")
public_url =  ngrok.connect(port_no).public_url
print(f"To acces the Gloable link please click {public_url}")


@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       if first_name != '':
         X=tweett(first_name,20)
         return render_template("in2.html",xnn=X)
        #  return send_file(X, mimetype='image/png')
      #  # getting input with name = lname in HTML form
      #  last_name = request.form.get("lname")
      #  return "Your name is "+first_name + last_name
    return render_template("index.html")

if __name__ == "__main__":
  
	app.run(port=port_no)

# <!doctype html>
# <html>
#     <head>
#         <title>Home page</title>
#     </head>
#     <body>
#         <h1>twitter centimental analysys</h1>
#         <form action="{{ url_for("gfg")}}" method="post">
#         <label for="firstname">Enter the topic on twitter</label>
#         <input type="text" id="firstname" name="fname" placeholder="txet">
#         <button type="submit">analyse</button>
#  <br> <br>
#  <p>positive=</p>{{ xnn[0][0] }}
#  <br> <br>
#  <p>neutral=</p>{{ xnn[0][1] }}
#  <br> <br>
#  <p>negative=</p>{{ xnn[0][2] }}

#     </body>
# </html>