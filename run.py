import praw
import pickledb
from time import sleep
from psaw import PushshiftAPI

test_mode = True

client_id = 'XXXX'
client_secret = 'XXXX'
reddit_user = 'XXXX'
reddit_pass = 'XXXX'

target_sub = 'The_Donald'
secret_sub = 'XXXX'
target_flairs = ['SUPER ELITE', 'OVER 9000 LEGS!!']

message_title = 'XXXX'
message_text = 'XXXX'


flairs = pickledb.load('data/flairs.db', False)
messaged = pickledb.load('data/messaged.db', False)
invited = pickledb.load('data/invited.db', False)


reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='Flair finder/pokerer/invitererer (by /u/impshum)',
                     username=reddit_user,
                     password=reddit_pass)


def gather():
    api = PushshiftAPI()
    submissions = api.search_submissions(
        subreddit=target_sub, aggs='author+author_flair_css_class')
    comments = api.search_comments(
        subreddit=target_sub, aggs='author+author_flair_css_class')

    for switch in [submissions, comments]:
        for post in switch:
            author = post.author
            flair = post.author_flair_text
            if flair in target_flairs:
                if not flairs.exists(author):
                    flairs.set(author, flair)
                    flairs.dump()
                    print(author, flair)


def message():
    for author in flairs.getall():
        if not messaged.exists(author):
            flair = flairs.get(author)
            messaged.set(author, flair)
            messaged.dump()
            if not test_mode:
                reddit.redditor(author).message(message_title, message_text)
            print(author, flair)
            sleep(100)


def invite():
    for author in flairs.getall():
        if not invited.exists(author):
            flair = flairs.get(author)
            invited.set(author, flair)
            invited.dump()
            if not test_mode:
                reddit.subreddit(secret_sub).contributor.add(author)
            print(author, flair)
            sleep(100)


gather()
message()
invite()
