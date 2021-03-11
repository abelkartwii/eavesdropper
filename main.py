import tweepy
import json
import sys
from afinn import Afinn
import configparser
import argparse
from pathlib import Path
from tweepy import OAuthHandler
from eavesdropper import Eavesdropper

parser = argparse.ArgumentParser(description = 'Analyze a Twitter topic!')

def main():
    # processes twitter API keys
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # parses command line arguments and language
    args = parser.parse_args()
    word = [str(args.topic)]
    language = ['en']

    # parses sentiments
    afinn = Afinn()

    # creates a twitter stream to filter based on argument
    twitter_stream = Stream(auth, Eavesdropper())
    twitter_stream.filter(languages = language, track = word)

if __name__ == "__main__":
    # reads config files for twitter API keys
    config = configparser.ConfigParser()
    config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))
    consumer_key = config['keys']['consumer_key']
    consumer_secret = config['keys']['consumer_secret']
    access_token = config['keys']['access_token']
    access_secret = config['keys']['access_secret']

    # argument parser
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument("topic", help = "Type the word you would like to analyze.", nargs = '+')
    main()