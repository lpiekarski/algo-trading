import pandas as pd
import tweepy

from core.env import require_env


def get_twitter_data(search_fn: str, amount: int, interval: str):
    import nltk
    nltk.downloader.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    vader = SentimentIntensityAnalyzer()

    token = require_env("TWITTER_BEARER_TOKEN")
    client = tweepy.Client(token)
    dfs = []
    next_token = None
    while True:
        res = getattr(client, search_fn)(
            "SP500 lang:en",
            max_results=500,
            tweet_fields="text,created_at,entities,author_id,public_metrics",
            expansions="author_id",
            user_fields="public_metrics,verified",
            next_token=next_token
        )
        user_dict = {user.id: user for user in res.includes["users"]}
        texts = [data.text for data in res.data]
        polarity_scores = [vader.polarity_scores(text) for text in texts]
        df = pd.DataFrame(
            data=dict(
                sentiment_neg=[score["neg"] for score in polarity_scores],
                sentiment_pos=[score["pos"] for score in polarity_scores],
                sentiment_neu=[score["neu"] for score in polarity_scores],
                sentiment_compound=[score["compound"] for score in polarity_scores],
                author_id=[data.author_id for data in res.data],
                retweet_count=[data.public_metrics["retweet_count"] for data in res.data],
                reply_count=[data.public_metrics["reply_count"] for data in res.data],
                like_count=[data.public_metrics["like_count"] for data in res.data],
                quote_count=[data.public_metrics["quote_count"] for data in res.data],
                author_verified=[user_dict[data.author_id].verified for data in res.data],
                author_followers_count=[user_dict[data.author_id].public_metrics["followers_count"] for data in res.data],
                author_following_count=[user_dict[data.author_id].public_metrics["following_count"] for data in res.data],
                author_tweet_count=[user_dict[data.author_id].public_metrics["tweet_count"] for data in res.data]
            ),
            index=pd.DatetimeIndex([data.created_at for data in res.data]))
        df = df.resample(interval).agg("last")
        dfs.append(df)
        if "next_token" not in res.meta:
            break
        else:
            next_token = res.meta["next_token"]
    return pd.concat(dfs, axis=0)
