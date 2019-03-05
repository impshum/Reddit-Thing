import praw
import pickledb
from time import sleep
from psaw import PushshiftAPI
import schedule
from config import *


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


print(f"""{C.Y}
╦═╗╔═╗╔╦╗╔╦╗╦╔╦╗  ╔═╗╔═╗╦
╠╦╝║╣  ║║ ║║║ ║   ╠╣ ╠═╝║
╩╚═╚═╝═╩╝═╩╝╩ ╩   ╚  ╩  ╩ v1.0
{C.W}""")

flairs = pickledb.load('data/flairs.db', False)
messaged = pickledb.load('data/messaged.db', False)
invited = pickledb.load('data/invited.db', False)


reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='Flair finder/pokerer/invitererer (by /u/impshum)',
                     username=reddit_user,
                     password=reddit_pass)

api = PushshiftAPI()


def gather():
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
                    print(f'{C.G}Added {author} {flair}{C.W}')
                    flairs.set(author, flair)
                    flairs.dump()
                else:
                    print(f'{C.R}Exists {author} {flair}{C.W}')


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
            print(f'{C.G} Invited {author} {flair}{C.W}')
            sleep(100)


def get_submission_count(user, api):
    submissions = api.search_comments(
        subreddit=target_sub, author=user, aggs='subreddit')
    for x in submissions:
        return x['subreddit'][0]['doc_count']


def get_comment_count(user, api):
    comments = api.search_submissions(
        subreddit=target_sub, author=user, aggs='subreddit')
    for x in comments:
        return x['subreddit'][0]['doc_count']


def check_count():
    removal = []
    for author in flairs.getall():
        s_count = get_submission_count(author, api)
        c_count = get_comment_count(author, api)
        if s_count + c_count >= total_posts:
            print(f'{C.G}{author} survived the cut{C.W}')
        else:
            removal.append(author)
            print(f'{C.R}{author} has been cut{C.W}')
    return removal


def clean():
    removal_list = check_count()
    for x in removal_list:
        flairs.rem(x)
    flairs.dump()


def main():
    if gather_users:
        gather()
    if clean_users:
        clean()
    if message_users:
        message()
    if invite_users:
        invite()


schedule.every().day.at("00:00").do(main)

if __name__ == '__main__':
    main()
    while True:
        schedule.run_pending()
        sleep(1)
