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

# def html_to_plaintext(html):
#     plaintext = html.replace("<p>", "")
#     plaintext = html.replace("<\p>", "")
#     return plaintext

# response = client.posts('realtalk-princeton.tumblr.com')
# posts = response['posts']

# retrieve 20 posts for testing
# for post in posts:
#     print("q", strip_tags(post["question"]))
#     print("a", strip_tags(post["answer"]))

def get_posts(client, blog, offset=0, max_posts=100):
    initial_offset = offset
    max_posts = max_posts + initial_offset
    while offset < max_posts:
        response = client.posts(blog, limit=20, offset=offset, reblog_info=True, notes_info=True)

        # Get the 'posts' field of the response        
        posts = response['posts']

        if not posts: return

        for post in posts:
            yield post

        # move to the next offset
        offset += 20


# client = pytumblr.TumblrRestClient('secrety-secret')
# blog = 'staff'

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


# Writes returned posts from get_posts to csv
with open('real-talk-princeton_last80_id_date_url.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['count', 'id', 'timestamp', 'post_url'])
    count = 0
    for post in get_posts(client, blog, offset=9919, max_posts=150):
        print(count)
        # print(post)
        id = post["id"]
        timestamp = post["timestamp"]
        post_url = strip_tags(html.unescape(post["post_url"]))

        writer.writerow([count, id, timestamp, post_url])
        count += 1


# Writes returned posts from get_posts to csv
# with open('real-talk-princeton_19439_20000.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Time', 'Question', 'Answer'])
#     count = 0
#     for post in get_posts(client, blog, 19439, 20000):
#         print(count)
#         print(post)
#         if "question" in post:
#             question = strip_tags(html.unescape(post["question"]))
#             # print("q", question)
#             answer = strip_tags(html.unescape(post["answer"]))
#             # print("a", answer) 
#         elif "body" in post:
#             question = ""
#             answer = strip_tags(html.unescape(post["body"]))
#         elif "url" in post and "description" in post:
#             question = strip_tags(html.unescape(post["description"]))
#             answer = strip_tags(html.unescape(post["url"]))

#         writer.writerow([count, question, answer])
#         count += 1