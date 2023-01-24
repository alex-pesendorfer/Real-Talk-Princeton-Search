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
    "Most popular professors public policy",
    engine="text-embedding-ada-002"
)

print(len(res))

pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment="us-west1-gcp")

index = pinecone.Index('rtp-index')

test = index.query(
  vector=res,
  top_k=3,
  include_values=False,
  include_metadata=True,
)
print(test['matches'][0])