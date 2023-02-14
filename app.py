# from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
from flask import url_for
import json
import os
import pandas as pd
import pinecone
import requests
import pandas as pd
import numpy as np
import datetime
import pytumblr
import html
import tiktoken
import sys

from openai.embeddings_utils import get_embedding, cosine_similarity

from apscheduler.schedulers.background import BackgroundScheduler

from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_post(offset):

    client = pytumblr.TumblrRestClient(
        os.environ.get('TUMBLR_CONSUMER_KEY'),
        os.environ.get('TUMBLR_CONSUMER_SECRET'),
        os.environ.get('TUMBLR_TOKEN'),
        os.environ.get('TUMBLR_TOKEN_SECRET'),
    )
    blog = "realtalk-princeton"

    # retrieve newest post
    response = client.posts(blog, limit=1, offset=offset, reblog_info=True, notes_info=True)

    # Get the 'posts' field of the response        
    posts = response['posts']
    if not posts: return

    for post in posts:
        if "question" in post:
            question = strip_tags(html.unescape(post["question"]))
            # print("q", question)
            answer = strip_tags(html.unescape(post["answer"]))
            # print("a", answer) 
        elif "body" in post:
            question = ""
            answer = strip_tags(html.unescape(post["body"]))
        elif "url" in post and "description" in post:
            question = strip_tags(html.unescape(post["description"]))
            answer = strip_tags(html.unescape(post["url"]))
        
        id = post["id"]
        timestamp = post["timestamp"]
        post_url = strip_tags(html.unescape(post["post_url"]))

        
        return {"id":id, "timestamp":timestamp, "post_url":post_url, "Question":question, "Answer":answer}

def embed_post(post):
    # embedding model parameters
    embedding_model = "text-embedding-ada-002"
    embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
    max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

    df = pd.DataFrame(post, index=[0])
    df["combined"] = (
        "Question: " + df.Question.str.strip() + "; Answer: " + df.Answer.str.strip()
    )   
    df = df.dropna()
    encoding = tiktoken.get_encoding(embedding_encoding)
    # omit reviews that are too long to embed
    df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))
    df = df[df.n_tokens <= max_tokens]

    df["embedding"] = df.combined.apply(lambda x: get_embedding(x, engine=embedding_model))
    df["embedding"] = df.embedding.apply(np.array)
    df["combined"] = df.combined
    df["Question"] = df.Question
    df["Answer"] = df.Answer
    df["id"] = df.id.astype(str)
    df["timestamp"] = df.timestamp.astype(str)
    df["post_url"] = df.post_url

    return df



def retrieve_posts():

    index = initialize_pinecone()

    """Function that runs every 6 hours"""
    print("Scheduler is alive")
    
    offset = 0

    while True:
        post = get_post(offset)
        print("offset: ", offset)
        
        # Check if post is already in pinecone
        name = 'vec_' + str(post["id"])
        results = index.fetch([name])
        
        # Check if database is up to date
        if results['vectors']:
            print(type(results['vectors']))
            print("reached!")
            print("The post I'm at: ", post["post_url"])
            break

            
        else:
            # embed and insert new post
            df_post = embed_post(post)
            
            # trim Answer if too long
            Answer = df_post["Answer"][0]
            if sys.getsizeof(Answer) > 9000:
                Answer = Answer[0:1500]
            
            index.upsert([(name, list(df_post["embedding"][0]), {"Question":df_post["Question"][0], "Answer":Answer,
                                                  "id" : df_post["id"][0], "timestamp" : df_post["timestamp"][0],
                                                  "post_url" : df_post["post_url"][0]})])

        offset += 1


    # else: insert into pinecone and add next post with offset = 0

def initialize_pinecone():
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    pinecone.init(api_key=PINECONE_API_KEY)
    index = pinecone.Index('rtp-index')

    return index
    # print(pinecone.describe_index('rtp-index'))

def get_results(index, query, n=5):
    
    res = get_embedding(
        query,
        engine="text-embedding-ada-002"
    )   

    results = index.query(
        vector=res,
        top_k=n,
        include_values=False,
        include_metadata=True,
    )

    return results

app = Flask(__name__)
sched = BackgroundScheduler(daemon=True)
sched.add_job(retrieve_posts, 'interval', hours=2)
sched.start()

@app.template_filter('ETDateTime')
def ETDateTime(s):
    x = datetime.datetime.fromtimestamp(int(s))
    return x.strftime("%B") + ' ' + x.strftime("%d") + ', ' + x.strftime("%Y") + ' at ' + x.strftime("%I") + ':' + x.strftime("%M") + ' ' + x.strftime("%p")


@app.route("/", methods=["GET"])
@app.route('/index', methods=['GET'])
def index():

    index = initialize_pinecone()
    stats = index.describe_index_stats()

    query_data = ""
    if request.method == "GET":
        query_data = request.args.get('search')
        if query_data is None or query_data.strip() == "":
            results = ""
        else:
            results = get_results(index, query_data)
            html = render_template("search_results.html", results = results, query_data = query_data)
            response = make_response(html)
            return response

            # print(results)
        
        html = render_template("pinecone_index.html", results = results, stats = stats)
        response = make_response(html)
        return response

