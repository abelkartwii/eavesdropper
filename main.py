import tweepy
import json
import sys
from afinn import Afinn
import configparser
import argparse
from pathlib import Path
from eavesdropper import Eavesdropper

config = configparser.ConfigParser()
config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))
consumer_key = config['keys']['consumer_key']
consumer_secret = config['keys']['consumer_secret']
access_token = config['keys']['access_token']
access_secret = config['keys']['access_secret']

parser = argparse.ArgumentParser(description = 'Analyze a Twitter topic!')

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    args = parser.parse_args()
    afinn = Afinn()
    word = str(args.topic)
    twitter_stream = tweepy.Stream(auth, Eavesdropper())
    twitter_stream.filter(languages = ['en'], track = [word])

if __name__ == "__main__":
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument("topic", help = "Type the word you would like to analyze.", nargs = '+')
    main()