import sys
import json
from operator import itemgetter

# Goal: computes the ten most frequently occurring hashtags. 
#       Script should print output to stdout. Each line of output should contain a hashtag, followed by a space, followed by the frequency of that hashtag in the entire file.
# More Details: See assignment1.html

# Sentiment_Metric(Word) = Sum_Over_Tweets(Tweet_Sentiment_Score * Frequency(Word)_In_Tweet)/Total_Frequency(Word)

# Helper Function - Count Word In the Non-Sentiment Dictionary
def count_word(word, score, cw_dict):
  if word in cw_dict:
    curr_score, curr_freq = cw_dict[word]
    cw_dict[word] = (curr_score+score, curr_freq+1)
  else:
    cw_dict[word] = (score, 1)

# Print Sentiment Score for each tweet using sentiment dict
def compute_top10_hashtag(tweet_file):
  tweets = open(tweet_file)

  hashtag_dict = {}

  for ln in tweets:
    curr_ln = json.loads(ln)
   
    # checking if the current line is a english tweet
    if 'entities' in curr_ln and curr_ln['lang'] == 'en':
      hashtags = curr_ln['entities']['hashtags']

      # Tracking the frequency for each hashtag
      for hashtag in hashtags:
        text = hashtag['text']
        if hashtag['text'] in hashtag_dict:
          hashtag_dict[text] += 1
        else:
          hashtag_dict[text] = 1

  tweets.close()

  hashtag_sorted = sorted(hashtag_dict.items(), key=itemgetter(1), reverse=True)

  for hashtag, freq in hashtag_sorted[0:10]:
    print "%s %d" % (hashtag, freq)

def main():
    tweet_file = sys.argv[1]
    compute_top10_hashtag(tweet_file)

if __name__ == '__main__':
    main()
