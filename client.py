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

# use our function
# with open('{}-posts.txt'.format(blog), 'w') as out_file:
#     for post in get_all_posts(client, blog):
#         print >>out_file, post
#         # if you're in python 3.x, use the following
#         # print(post, file=out_file)


with open('real-talk-princeton_19439_20000.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Question', 'Answer'])
    count = 0
    for post in get_posts(client, blog, 19439, 20000):
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

        writer.writerow([count, question, answer])
        count += 1