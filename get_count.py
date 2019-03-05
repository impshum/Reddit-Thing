from psaw import PushshiftAPI


target_sub = 'recycledrobot'

api = PushshiftAPI()


def get_submission_count(user):
    submissions = api.search_comments(
        subreddit=target_sub, author=user, aggs='subreddit')
    for x in submissions:
        return x['subreddit'][0]['doc_count']


def get_comment_count(user):
    comments = api.search_submissions(
        subreddit=target_sub, author=user, aggs='subreddit')
    for x in comments:
        return x['subreddit'][0]['doc_count']


print(get_submission_count('impshum'))
print(get_comment_count('impshum'))
