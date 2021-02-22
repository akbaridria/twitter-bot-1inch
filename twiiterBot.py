import requests
import tweepy
import os
import json
import math
import datetime
from os import environ

#create twitter bot and deploy to heroku

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
          decimals
        }
        token1 {
          id
          symbol
          decimals
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

#config 1inch api
url_1inch = "https://api.1inch.exchange/v2.0/quote"


def connect_to_twitter() :
  auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
  api = tweepy.API(auth, wait_on_rate_limit=True,
      wait_on_rate_limit_notify=True)
  return api

def tweet(api, status) :
  api.update_status(status)

prevStatus = ""
while True :
  r = requests.post(request_url, json = {'query' : query})
  raw_data = r.json()
  if r.status_code == 200 :
    data = raw_data['data']['swaps'][0]
    ticker0Symbol = data['pair']['token0']['symbol']
    ticker1Symbol = data['pair']['token1']['symbol']
    amountOut = data['amount0Out']
    decimal0Token = data['pair']['token0']['decimals']
    decimal2Token = data['pair']['token1']['decimals']
    parameter1inch = {
        "fromTokenAddress" : data['pair']['token0']['id'],
        "toTokenAddress" : data['pair']['token1']['id'],
        "amount" : int(float(math.pow(10, int(decimal0Token))) * float(amountOut))
    }
    r3 = requests.get(url_1inch, params=parameter1inch)
    uniswapValue = data['amount1In']
    print('bot is running')
    inch1Value = float(r3.json()['toTokenAmount'])/math.pow(10, int(decimal2Token))
    if inch1Value > float(uniswapValue) :
        tx = data['transaction']['id']
        timestamp = datetime.datetime.fromtimestamp(int(data['transaction']['timestamp']))
        waktu = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        status = "The swap transaction were carried out at Uniswap on {} from token {} {} for token {} {} tx : {}, \n \n if using 1inch protocol you will get {} {} for {} {}.".format(waktu, amountOut, ticker0Symbol, uniswapValue, ticker1Symbol, tx,  inch1Value, ticker1Symbol, amountOut, ticker0Symbol)
        if prevStatus != status :
            api = connect_to_twitter()
            tweet(api, status)
            prevStatus = status

    