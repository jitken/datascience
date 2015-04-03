import sys
import json
import re
from operator import itemgetter

# Goal:  Your script should print output to stdout. Each line of output should contain a term, followed by a space, followed by the frequency of that term in the entire file.
# More Details: See assignment1.html

# Sentiment_Metric(Word) = Sum_Over_Tweets(Tweet_Sentiment_Score * Frequency(Word)_In_Tweet)/Total_Frequency(Word)
# -- We will ignore all Tweets with Sentiment Score of 0

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

# Compute Frequency for each word 
def compute_freq(tweet_file):
  tweets = open(tweet_file)

  cw_dict = {}

  for ln in tweets:
    curr_ln = json.loads(ln)
   
    # checking if the current line is a tweet
    if 'text' in curr_ln:
      if curr_ln['lang'] == 'en':

        filtered_tweet = filter_tweet(curr_ln['text'], curr_ln['entities'])  
        # making tweet all lowercase - sentiments dict is in lower case
        filtered_tweet = filtered_tweet.lower()

        tokens = re.findall(r"[\w']+", filtered_tweet)

        # Count Tokens
        for token in tokens:
          if token in cw_dict:
            cw_dict[token] += 1
          else:
            cw_dict[token] = 1

  tweets.close()
  
  terms_sorted = sorted(cw_dict.items(), key=itemgetter(1))

  # Print to stdout as per assignment goal
  for k,v in terms_sorted:
    print "%s %d" % (k ,v)

def main():
    tweet_file = sys.argv[1]
    compute_freq(tweet_file)

if __name__ == '__main__':
    main()
