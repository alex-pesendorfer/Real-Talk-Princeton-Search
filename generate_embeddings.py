# imports
import pandas as pd
import tiktoken
import os

from openai.embeddings_utils import get_embedding

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# load & inspect dataset
input_datapath = "Combined_real-talk-princeton_10000_19439.csv"  # to save space, we provide a pre-filtered dataset
df = pd.read_csv(input_datapath, index_col=0)
df = df[["Question", "Answer", "id", "timestamp", "post_url"]]
df["combined"] = (
    "Question: " + df.Question.str.strip() + "; Answer: " + df.Answer.str.strip()
)
df = df.dropna()
print(df.head(5))

# subsample to 1k most recent reviews and remove samples that are too long
# top_n = 10000
# df = df.sort_values("Time").tail(top_n * 2)  # first cut to first 2k entries, assuming less than half will be filtered out
# df.drop("Time", axis=1, inplace=True)

encoding = tiktoken.get_encoding(embedding_encoding)

# omit reviews that are too long to embed
df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))
df = df[df.n_tokens <= max_tokens]
# df = df[df.n_tokens <= max_tokens].tail(top_n)
len(df)

# Ensure you have your API key set in your environment per the README: https://github.com/openai/openai-python#usage

# This may take a few minutes
df["embedding"] = df.combined.apply(lambda x: get_embedding(x, engine=embedding_model))
df.to_csv("rtp_10000_20000_embedded.csv")