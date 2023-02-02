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

datafile_path = "real-talk-princeton_with_embeddings_10000.csv"
df = pd.read_csv(datafile_path)

df["embedding"] = df.embedding.apply(eval).apply(np.array)
df["combined"] = df.combined
df["Question"] = df.Question
df["Answer"] = df.Answer

print(len(df["combined"]))

