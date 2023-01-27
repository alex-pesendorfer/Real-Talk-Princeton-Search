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

from openai.embeddings_utils import get_embedding, cosine_similarity

app = Flask(__name__)

# pinecone_index_name = "question-answering-chatbot"
# DATA_DIR = "tmp"
# DATA_FILE = f"{DATA_DIR}/quora_duplicate_questions.tsv"
# DATA_URL = "https://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"

# test with amazone fine-food data
# datafile_path = "amazon-fine-food-reviews/fine_food_reviews_with_embeddings_100.csv"
datafile_path = "real-talk-princeton_with_embeddings_10000.csv"
df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(eval).apply(np.array)

# search through the reviews for a specific product
def search_reviews(df, product_description, n=3, pprint=True):
    product_embedding = get_embedding(
        product_description,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, product_embedding))

    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
        .combined.str.replace("Title: ", "")
        .str.replace("; Content:", ": ")
    )
    if pprint:
        for r in results:
            print(r[:200])
            print()
    return results


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

@app.route("/", methods=["GET"])
@app.route('/index', methods=['GET'])
def index():

    index = initialize_pinecone()

    query_data = ""
    if request.method == "GET":
        query_data = request.args.get('search')
        if query_data is None or query_data.strip() == "":
            results = ""
        else:
            results = get_results(index, query_data)
            print(results)
        
        html = render_template("pinecone_index.html", results = results)
        response = make_response(html)
        return response


# @app.route("/", methods=["GET"])
# @app.route('/index', methods=['GET'])
# def index():

#     query_data = ""
#     if request.method == "GET":
#         query_data = request.args.get('search')
#         if query_data is None or query_data.strip() == "":
#             results = ""
#         else:
#             # print("query_data", query_data)
#             results = search_reviews(df, query_data, n=5, pprint=False)
#             # print(len(results))
#             # for item in results:
#             #     print(item)
#             #     results = item
#             output = []
#             for item in results:
#                 output.append(item)
#             print(output)
#             results = output
#         html = render_template("index.html", results = results)
#         response = make_response(html)
#         return response
    

# @app.route("/api/search", methods=["POST", "GET"])
# def search():
#     if request.method == "POST":
#         return query_pinecone(request.form.question)
#     if request.method == "GET":
#         return query_pinecone(request.args.get("question", ""))
#     return "Only GET and POST methods are allowed for this endpoint"