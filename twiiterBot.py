import requests
import tweepy
import os
import json
from os import environ

#config twitter credentials
API_KEY = environ["API_KEY"]
API_SECRET_KEY = environ["API_SECRET_KEY"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]
ACCESS_SECRET_TOKEN = environ["ACCESS_SECRET_TOKEN"]

#config graphql the graph uniswap
request_url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
query = """ {
    swaps(first: 1, orderBy: timestamp, orderDirection: desc) {
      transaction {
        id
        timestamp
      }
      id
      pair {
        token0 {
          id
          symbol
        }
        token1 {
          id
          symbol
        }
      }
      amount0In
      amount0Out
      amount1In
      amount1Out
      amountUSD
      to
    }
} """

def connect_to_twitter() :
  auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
  api = tweepy.API(auth, wait_on_rate_limit=True,
      wait_on_rate_limit_notify=True)
  return api

def tweet(api, status) :
  api.update_status(status)

while true :
  r = requests.post(request_url, json = {'query' : query})
  raw_data = r.json()
  if r.status_code == 200 :
    data = raw_data['data']['swaps'][0]
    