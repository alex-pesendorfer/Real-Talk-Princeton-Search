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

# print(openai.Engine.list())  # check we have authenticated

MODEL = "text-embedding-ada-002"

res = get_embedding(
    "Sample document text goes here",
    engine="text-embedding-ada-002"
)

print(len(res))
# pinecone.delete_index("rtp-index")

# pinecone.create_index("rtp-index", dimension=len(res))
print(pinecone.list_indexes())

index = pinecone.Index("rtp-index")

# index.upsert([('vec_0', res, {"question":"q", "answer":"a"})])

datafile_path = "real-talk-princeton_with_embeddings_10000.csv"
df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(eval).apply(np.array)
df["combined"] = df.combined
df["Question"] = df.Question
df["Answer"] = df.Answer

# print(df["combined"][0])
# print(df["embedding"][0])

vecs = []
count = 0
for i in range(len(df["embedding"])):
    if count == 100:
        index.upsert(vecs)
        vecs = []
        count = 0

    name = "vec_" + str(i)
    vecs.append((name, list(df["embedding"][i]), {"Question":df["Question"][i], "Answer":df["Answer"][i]}))
    # vecs.append((name, list(df["embedding"][i]), {"combined":df["combined"][i], "Question":df["Question"][i], "Answer":df["Answer"][i]}))
    count += 1

# test = index.query(
#   vector=res,
#   top_k=3,
#   include_values=True
# )
# print(test)