from core.twitter import get_twitter_data


def get_data(amount, interval, start_date):
    return get_twitter_data("search_recent_tweets", amount, interval)
