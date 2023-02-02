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


# Update metadata
# datafile_path = "real-talk-princeton_10000_19439_id_date_url.csv"
# df = pd.read_csv(datafile_path)


# for i in range(len(df["id"])):
# name = "vec_" + str(10000)
# index.update(name, set_metadata={"id" : df["id"][0], "timestamp" : df["timestamp"][0], "post_url" : df["post_url"][0]})



# index.upsert([('vec_0', res, {"question":"q", "answer":"a"})])

datafile_path = "rtp_10000_embedded.csv"
df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(eval).apply(np.array)
df["combined"] = df.combined
df["Question"] = df.Question
df["Answer"] = df.Answer
df["id"] = df.id.astype(str)
df["timestamp"] = df.timestamp.astype(str)
df["post_url"] = df.post_url

print(df["combined"][9300])
print(df["embedding"][9300])
print(df["Question"][9300])
print(df["Answer"][9300])
print(df["id"][9300])
print(df["timestamp"][9300])
print(df["post_url"][9300])

print(len(df["embedding"]))
print(len(df["id"]))


vecs = []
count = 0
for i in range(len(df["embedding"])):
    if count == 100 or i == len(df["embedding"]) - 1:
        index.upsert(vecs)
        vecs = []
        count = 0

    name = "vec_" + str(9940 + i)
    vecs.append((name, list(df["embedding"][i]), {"Question":df["Question"][i], "Answer":df["Answer"][i],
                                                  "id" : df["id"][i], "timestamp" : df["timestamp"][i],
                                                  "post_url" : df["post_url"][i]}))
    # vecs.append((name, list(df["embedding"][i]), {"combined":df["combined"][i], "Question":df["Question"][i], "Answer":df["Answer"][i]}))
    count += 1



# # test = index.query(
# #   vector=res,
# #   top_k=3,
# #   include_values=True
# # )
# # print(test)