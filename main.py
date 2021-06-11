import tweepy
import json
import sys
import argparse
from pathlib import Path
from tweepy import OAuthHandler, Stream
from eavesdropper import Eavesdropper
from configparser import ConfigParser

parser = argparse.ArgumentParser(description = 'Analyze a Twitter topic!')

def main():
    # processes twitter API keys
    auth_keys = OAuthHandler(consumer_key, consumer_secret)
    auth_keys.set_access_token(access_token, access_secret)

    # parses command line arguments and language
    args = parser.parse_args()
    word = str(args.topic)
    language = ['en']
    jakarta = [-6.1249, 106.6668, -6.3048, 106.9571]

    # creates a twitter stream to filter based on argument
    # connects to kafka using Eavesdropper object
    twitter_stream = Stream(auth = auth_keys, 
                            listener = Eavesdropper(topic = str(args.topic)))
    twitter_stream.filter(languages = language, track = word, locations = jakarta)

if __name__ == "__main__":
    # reads config files for twitter API keys
    config = ConfigParser()
    config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))
    consumer_key = config['twitter']['consumer_key']
    consumer_secret = config['twitter']['consumer_secret']
    access_token = config['twitter']['access_token']
    access_secret = config['twitter']['access_secret']

    # argument parser
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument("topic", help = "Type the word you would like to analyze.", nargs = '+')
    main()