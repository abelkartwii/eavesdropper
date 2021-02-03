import tweepy
import json
import sys
import afinn
import configparser
import parser
from eavesdropper import Eavesdropper

config = configparser.ConfigParser()
config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
access_token = config['access_token']
access_secret = config['access_secret']

def main():
    args = parser.parse_args()
    afinn = Afinn()
    twitter_stream = tweepy.Stream(auth, Eavesdropper())
    twitter_stream.filter(languages = ['en'], track = [word])

if __name__ == "__main__":
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument(help = "Type the word you would like to analyze.")
    main()