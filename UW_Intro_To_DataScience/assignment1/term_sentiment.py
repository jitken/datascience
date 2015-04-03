import sys
import json
import re
from operator import itemgetter

# Goal:  You work backwards to deduce the sentiment of the non-sentiment carrying words that do not appear in AFINN-111.txt.
# Assumptions: You can assume the sample file will only include English tweets and no other types of streaming messages.
# Example: python tweet_sentiment.py AFINN-111.txt output.txt
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


# Helper Function - Count Word In the Non-Sentiment Dictionary
def count_word(word, score, cw_dict):
  if word in cw_dict:
    curr_score, curr_freq = cw_dict[word]
    cw_dict[word] = (curr_score+score, curr_freq+1)
  else:
    cw_dict[word] = (score, 1)

# Print Sentiment Score for each tweet using sentiment dict
def compute_terms_sentiment(tweet_file, s_dict):
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

        # Compute Sentiment Score for current tweet
        scores = [s_dict.get(token, 0) for token in tokens]
        sentiment_score = sum(scores)

        if sentiment_score != 0:
          # Counting Up the total tweet score per word and it's frequency 
          for token in tokens:
            if token not in s_dict:
              count_word(token, sentiment_score, cw_dict)

  tweets.close()

  # Compute Sentiment Metric for terms
  terms_dict = {k:float(v[0])/v[1] for k,v in cw_dict.items()}
  
  terms_sorted = sorted(terms_dict.items(), key=itemgetter(1))

  # Print to stdout as per assignment goal
  for k,v in terms_sorted:
    print "%s %0.2f" % (k ,v)

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    s_dict = parse_sentiment(sent_file)
    compute_terms_sentiment(tweet_file, s_dict)

if __name__ == '__main__':
    main()
