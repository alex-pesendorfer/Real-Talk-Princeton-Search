import pytumblr
client = pytumblr.TumblrRestClient(
    'BdQxCsKzTTa6TJUBA5aRgQen9bFzvIOxZhrJ0POYK7aVJGUJV0',
    'zLkfS4zvvVbRkTxpJxzRrJ9Iqxnp6XjOmqwIwpIVZDy8whYw44',
    'vIU3PspwwnEgbZHYxoaBqn4ZkIWbMKAubuGQ3oZe6mkd6MCSsH',
    'zLkfS4zvvVbRkTxpJxzRrJ9Iqxnp6XjOmqwIwpIVZDy8whYw44',
)

response = client.posts('realtalk-princeton.tumblr.com')
posts = response['posts']

for post in posts:
    print(post)

# def get_all_posts(client, blog):
#     offset = 0
#     while True:
#         response = client.posts(blog, limit=20, offset=offset, reblog_info=True, notes_info=True)

#         # Get the 'posts' field of the response        
#         posts = response['posts']

#         if not posts: return

#         for post in posts:
#             yield post

#         # move to the next offset
#         offset += 20


# client = pytumblr.TumblrRestClient('secrety-secret')
# blog = 'staff'

# # use our function
# with open('{}-posts.txt'.format(blog), 'w') as out_file:
#     for post in get_all_posts(client, blog):
#         print >>out_file, post
#         # if you're in python 3.x, use the following
#         # print(post, file=out_file)
