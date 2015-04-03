import sys
import json
import re

# Goal:  Your script should print to stdout the sentiment of each tweet in the file, one numeric sentiment score per line.
# Assumptions: You can assume the sample file will only include English tweets and no other types of streaming messages.
# Example: python tweet_sentiment.py AFINN-111.txt output.txt
# More Details: See assignment1.html

# Parse the sentiment files and return a dict
def parse_sentiment(file):
  afinnfile = open(file)
  scores = {} # initialize an empty dictionary
  for line in afinnfile:
    term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.

  afinnfile.close()
  return scores

# Remove entities (url, hashtag, usernames) from tweet
def filter_tweet(tweet, entities):
  tweet_indices = [True] * len(tweet)

  for key in entities.keys():
    for entry in entities[key]:
      s_idx = entry['indices'][0]
      e_idx = entry['indices'][1]
      tweet_indices[s_idx:e_idx] = [False] * (e_idx - s_idx)

  filtered_tweet = [tweet[ii] for ii,item in enumerate(tweet_indices) if item]      

  return "".join(filtered_tweet)

# Print Sentiment Score for each tweet using sentiment dict
def print_sentiment(tweet_file, s_dict):
  tweets = open(tweet_file)

  for ln in tweets:
    curr_ln = json.loads(ln)
   
    # checking if the current line is a tweet
    if 'text' in curr_ln:
      if curr_ln['lang'] == 'en':
        filtered_tweet = filter_tweet(curr_ln['text'], curr_ln['entities'])  

        # making tweet all lowercase - sentiments dict is in lower case
        filtered_tweet = filtered_tweet.lower()
        tokens = re.findall(r"[\w']+", filtered_tweet)
        scores = [s_dict.get(token, 0) for token in tokens]
        print sum(scores)

    else:
      # For non-english tweets, return 0
      print 0

  tweets.close()

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    s_dict = parse_sentiment(sent_file)
    print_sentiment(tweet_file, s_dict)

if __name__ == '__main__':
    main()
