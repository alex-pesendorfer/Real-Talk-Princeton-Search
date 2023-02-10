import csv
import html
import os
import pytumblr

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

def get_post(client, blog, offset=0):
    response = client.posts(blog, limit=20, offset=offset, reblog_info=True, notes_info=True)
    # Get the 'posts' field of the response        
    posts = response['posts']
    if not posts: return
    for post in posts:
        yield post

TUMBLR_CONSUMER_KEY = os.environ.get('TUMBLR_CONSUMER_KEY')
TUMBLR_CONSUMER_SECRET = os.environ.get('TUMBLR_CONSUMER_SECRET')
TUMBLR_TOKEN = os.environ.get('TUMBLR_TOKEN')
TUMBLR_TOKEN_SECRET = os.environ.get('TUMBLR_TOKEN_SECRET')

client = pytumblr.TumblrRestClient(
    TUMBLR_CONSUMER_KEY,
    TUMBLR_CONSUMER_SECRET,
    TUMBLR_TOKEN,
    TUMBLR_TOKEN_SECRET,
)
blog = "realtalk-princeton"




# # Writes returned posts from get_posts to csv
# with open('real-talk-princeton_16400_19439_id_date_url.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['count', 'id', 'timestamp', 'post_url'])
#     count = 16400
#     for post in get_posts(client, blog, offset=10000+56+6486, max_posts=19439):
#         print(count)
#         # print(post)
#         id = post["id"]
#         timestamp = post["timestamp"]
#         post_url = strip_tags(html.unescape(post["post_url"]))

#         writer.writerow([count, id, timestamp, post_url])
#         count += 1


# Writes returned posts from get_posts to csv
'Id', 'Timestamp', 'Post_url', 'Question', 'Answer'
count = index.describe blah blah # fix
def retrieve(offset):
    for post in get_posts(client, blog, offset):
            print(count)
            print(post)
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

            writer.writerow([count, id, timestamp, post_url, question, answer])
            count += 1