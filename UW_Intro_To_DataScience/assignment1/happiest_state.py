import sys
import json
import re
from operator import itemgetter

# Goal:  Your script should print the two letter state abbreviation of the state with the highest average tweet sentiment to stdout.
# Assumptions: You can assume the sample file will only include English tweets and no other types of streaming messages.
# Example: python tweet_sentiment.py AFINN-111.txt output.txt
# More Details: See assignment1.html

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

states_reverselookup = {v.lower():k for k,v in states.items()}

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


# Helper Function - For given state, update total score and # of tweets
def track_score_per_state(state, score, cw_dict):
  if state in cw_dict:
    curr_score, curr_freq = cw_dict[state]
    cw_dict[state] = (curr_score+score, curr_freq+1)
  else:
    cw_dict[state] = (score, 1)

# from string, discern state
def state_lookup(string):

  if string.strip() == "":
    return None

  # See if any of the tokens are in the string
  tokens = re.findall(r"[\w]+", string)
  for token in tokens:
    if token.upper() in states:
      return token.upper()

  # Checking if any of the state name is in the string
  string_lower = string.lower()
  for state_name in states_reverselookup.keys():
    if state_name in string_lower:
      return states_reverselookup[state_name]

  return None

# Print Sentiment Score for each tweet using sentiment dict
def compute_happiest_state(tweet_file, s_dict):
  tweets = open(tweet_file)

  cw_dict = {}

  for ln in tweets:
    curr_ln = json.loads(ln)
   
    # checking if the current line is a tweet
    if 'text' in curr_ln:
      if curr_ln['lang'] == 'en':

        # If this tweet is not from the US, continue
        tweet_state = None
        if curr_ln['place'] != None:
          if curr_ln['place']['country_code'] != 'US':
            continue
          else:
            tweet_state = state_lookup(curr_ln['place']['full_name'])
        else:
            tweet_state = state_lookup(curr_ln['user']['location'])

        # If we are unable to discern the tweet state, ignore current tweet
        if tweet_state == None:
          continue

        filtered_tweet = filter_tweet(curr_ln['text'], curr_ln['entities'])  
        
        # making tweet all lowercase - sentiments dict is in lower case
        filtered_tweet = filtered_tweet.lower()

        tokens = re.findall(r"[\w']+", filtered_tweet)

        # Compute Sentiment Score for current tweet
        scores = [s_dict.get(token, 0) for token in tokens]
        sentiment_score = sum(scores)

        # Counting Up # of tweets associated with each state and its total sentimental score 
        track_score_per_state(tweet_state, sentiment_score, cw_dict)

  tweets.close()

  # Compute Sentiment Metric for terms
  state_score_dict = {k:float(v[0])/v[1] for k,v in cw_dict.items()}
  
  state_score_sorted = sorted(state_score_dict.items(), key=itemgetter(1), reverse=True)

  if len(state_score_sorted) > 0:
    print state_score_sorted[0][0]
  else:
    print "Error - No USA Tweets found in the tweet file %s" % tweet_file

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    s_dict = parse_sentiment(sent_file)
    compute_happiest_state(tweet_file, s_dict)

if __name__ == '__main__':
    main()
