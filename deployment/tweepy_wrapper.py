import tweepy
import signal
import sys
import time

# http://docs.tweepy.org/en/latest/streaming_how_to.html

CONSUMER_KEY = 'XXX'
CONSUMERS_SECRET = 'XXX'
ACCESS_KEY = 'XXX'
ACCESS_SECRET = 'XXX'

streamListener = None
stream = None


class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        self.running = True
        super(MyStreamListener, self).__init__()

    def on_status(self, status):
        if not self.running:
            return False

        print(status.id_str)
        text = ""
        if hasattr(status, "retweeted_status"):
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text

        print(text)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

    def cancel(self):
        print("Canceling stream")
        self.running = False
        self.on_error(420)


def signal_handler(sig, frame):
    print(f'Received {signal.Signals(sig).name}')
    streamListener.cancel()


def get_auth(consumer_key, consumer_secret, access_key, accesss_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, accesss_secret)
    api = tweepy.API(auth)
    return api


def create_stream():
    global stream
    global streamListener
    signal.signal(signal.SIGINT, signal_handler)

    streamListener = MyStreamListener()

    api = get_auth(CONSUMER_KEY, CONSUMERS_SECRET, ACCESS_KEY, ACCESS_SECRET)
    stream = tweepy.Stream(
        auth=api.auth, listener=streamListener, tweet_mode='extended')

    time.sleep(2)


def run_stream(tags):
    global stream
    stream.filter(track=tags, is_async=True)
    streamListener.running = True
    time.sleep(2)


def cancel_stream():
    global streamListener
    streamListener.cancel()
    time.sleep(2)


if __name__ == "__main__":
    create_stream()
    tags = ["wehrpflicht"]
    run_stream(tags)
    time.sleep(5)
    cancel_stream()
    time.sleep(5)
    tags = ["Trump"]
    run_stream(tags)
    time.sleep(10)
    cancel_stream()
