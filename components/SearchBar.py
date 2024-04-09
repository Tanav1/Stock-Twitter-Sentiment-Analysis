import tweepy
import re
import pandas as pd
from textblob import TextBlob
from flask import Flask, request, jsonify, render_template
import requests
import json
import yfinance as yf
from stocksymbol import StockSymbol

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search_tweets():
    query = request.form['query']

    query = query.upper()
   
    yfinance_query = query.replace("$", "")
    api_key = '9d0766b6-882e-4280-bb06-a38404aae4db'
    ss = StockSymbol(api_key)


    stocksymbol_api_key = '9d0766b6-882e-4280-bb06-a38404aae4db'
    ss = StockSymbol(stocksymbol_api_key)
    symbol_list_us = ss.get_symbol_list(market="US", symbols_only=True) # "us" or "america" will also work

    valid_stock = False
    if yfinance_query in symbol_list_us:
        valid_stock = True
    #     pass
    # elif yfinance_query not in symbol_list_us:
    #     valid_stock = False
    # else:
    #     pass
    if valid_stock:
        url = f'https://api.nasdaq.com/api/quote/{yfinance_query}/info?assetclass=stocks'

        headers = {
            'User-Agent': 'Mozilla/5.0',
            'X-NASDAQ-REQUEST-TIME': '2022-03-28T00:00:00.000Z',
            'X-NASDAQ-REQUESTED-WITH': 'XMLHttpRequest',
            'X-NASDAQ-API-KEY': 'cpsP7E4SwZoRJNVUfexs',
        }

        response = requests.get(url, headers=headers)

        if response.ok:
            data = json.loads(response.text)
            current_price = data['data']['primaryData']['lastSalePrice']
            volume_str = data['data']['primaryData']['volume']
            volume = (volume_str.replace(',', ''))
        else:
            print("Error fetching data from NASDAQ API")

        ticker = yf.Ticker(yfinance_query)
        rsi_data = ticker.history(period='6mo').loc[:, ['Close']].rename(columns={'Close': 'price'})
        rsi_data['delta'] = rsi_data['price'].diff()
        rsi_data.dropna(inplace=True)

        # Calculate the 14-day RSI using a simple moving average
        up_prices, down_prices = rsi_data['delta'].copy(), rsi_data['delta'].copy()
        up_prices[up_prices < 0] = 0
        down_prices[down_prices > 0] = 0
        avg_gain = up_prices.rolling(window=14).mean()
        avg_loss = abs(down_prices.rolling(window=14).mean())
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

        current_rsi = rsi.iloc[-1]

        ma_data = ticker.history(period='max').loc[:, ['Close']]
        ma_data['MA50'] = ma_data['Close'].rolling(window=50).mean()
        ma50 = ma_data['MA50'].iloc[-1]

        ma_data['MA200'] = ma_data['Close'].rolling(window=200).mean()
        ma200 = ma_data['MA200'].iloc[-1]

        print(query)
        CONSUMER_KEY = "4B5GY48zWTjJAKhjHfUbjhQ0I"
        CONSUMER_SECRET = "L8s5a8UCLcVtX1oI1uJF2XOx4XCCRFr7RJDmxHCCkrHcDGhXIy"
        ACCESS_TOKEN = "2990641845-rFGtRNud780aUwBMudhcQDHMOjLOwasbvRxZhyS"
        ACCESS_TOKEN_SECRET = "SqFMTHD1ZlfqP47n6dHPQCnqZVBoBttZUJKEk7S2txuNv"

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # build a api object, and the introduction about the rate limit will be cover in next lab
        api = tweepy.API(auth)
        tweets = []

        # call twitter api to fetch tweets

        fetched_tweets = api.search(q=query, count=1000)

        for tweet in fetched_tweets:
            if tweet.lang == 'en':
                # cleaning the tweets
                tweet = tweet.text
                tweet = tweet.lower()
                tweet = re.sub(r"[^\w$#\s]+", "", tweet)
                # getting the sentiment from textblob
                analysis = TextBlob(tweet)
                # Removing Punctuations, Numbers, and Special Characters

                senti = analysis.sentiment.polarity
                # labeling the sentiment
                if senti < 0: 
                    emotion = "NEG"
                elif senti > 0:
                    emotion = "POS"
                else:
                    emotion = "NEU"
                # appending all data
                tweets.append((tweet, senti, emotion))
                df = pd.DataFrame(tweets, columns=['tweets', 'senti', 'emotion'])
                df = df.drop_duplicates(subset=['tweets'])
                keywords = ['community', 'chatroom', 'discord', 'subscriber', 'alert', 'member', 'traders', 'minimize',
                            'join', 'learn', 'link', 'thanks', 'chat']
                df = df[~df['tweets'].str.lower().str.contains('|'.join(keywords))]
                score = df['senti'].mean()
                score = score*100
                score = round(score, 2)

                # print("Error fetching data from NASDAQ API")

    
        return render_template('results.html', df=df, query=query, score=score, current_price=current_price, volume=volume,
                           rsi=current_rsi, ma50=ma50, ma200=ma200, valid_stock=valid_stock)
    else:
        return render_template('index.html', valid_stock=valid_stock)


   




#     def current_stock_price(stock_symbol):

# 	symbol = stock_symbol  # Replace with the desired stock symbol

# 	url = f'https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks'

# 	headers = {
# 	    'User-Agent': 'Mozilla/5.0',
# 	    'X-NASDAQ-REQUEST-TIME': '2022-03-28T00:00:00.000Z',
# 	    'X-NASDAQ-REQUESTED-WITH': 'XMLHttpRequest',
# 	    'X-NASDAQ-API-KEY': 'cpsP7E4SwZoRJNVUfexs',
# 	}

# 	response = requests.get(url, headers=headers)

# 	if response.ok:
# 	    data = json.loads(response.text)
# 	    current_price = data['data']['primaryData']['lastSalePrice']
# 	    print(f"The current price of {symbol} is {current_price}")
# 	else:
# 	    print("Error fetching data from NASDAQ API")


# 	return current_price


# def current_volume(stock_symbol):
# 	symbol = stock_symbol  # Replace with the desired stock symbol

# 	url = f'https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks'

# 	headers = {
# 	    'User-Agent': 'Mozilla/5.0',
# 	    'X-NASDAQ-REQUEST-TIME': '2022-03-28T00:00:00.000Z',
# 	    'X-NASDAQ-REQUESTED-WITH': 'XMLHttpRequest',
# 	    'X-NASDAQ-API-KEY': 'cpsP7E4SwZoRJNVUfexs',
# 	}

# 	response = requests.get(url, headers=headers)

# 	if response.ok:
# 	    data = json.loads(response.text)
# 	    volume_str = data['data']['primaryData']['volume']
# 	    volume = int(volume_str.replace(',', ''))
# 	    print(f"The volume of {symbol} is {volume}.")
# 	else:
#     	print("Error fetching data from NASDAQ API")

#     return current_volume



#  def current_rsi(stock_symbol):
#  	symbol = stock_symbol  # Replace with the desired stock symbol

# 	ticker = yf.Ticker(symbol)
# 	rsi_data = ticker.history(period='6mo').loc[:, ['Close']].rename(columns={'Close': 'price'})
# 	rsi_data['delta'] = rsi_data['price'].diff()
# 	rsi_data.dropna(inplace=True)

# 	# Calculate the 14-day RSI using a simple moving average
# 	up_prices, down_prices = rsi_data['delta'].copy(), rsi_data['delta'].copy()
# 	up_prices[up_prices < 0] = 0
# 	down_prices[down_prices > 0] = 0
# 	avg_gain = up_prices.rolling(window=14).mean()
# 	avg_loss = abs(down_prices.rolling(window=14).mean())
# 	rs = avg_gain / avg_loss
# 	rsi = 100.0 - (100.0 / (1.0 + rs))

# 	current_rsi = rsi.iloc[-1]
	
# 	return current_rsi


# def current_50_MA(stock_symbol):

# 	symbol = 'AAPL'  # Replace with the desired stock symbol

# 	ticker = yf.Ticker(symbol)
# 	ma_data = ticker.history(period='max').loc[:, ['Close']]

# 	# Calculate the 50-day and 200-day moving averages
# 	ma_data['MA50'] = ma_data['Close'].rolling(window=50).mean()

# 	current_price = ma_data['Close'].iloc[-1]
# 	ma50 = ma_data['MA50'].iloc[-1]

# 	return ma50



# def current_200_MA(stock_symbol):

# 	symbol = 'AAPL'  # Replace with the desired stock symbol

# 	ticker = yf.Ticker(symbol)
# 	ma_data = ticker.history(period='max').loc[:, ['Close']]

# 	# Calculate the 50-day and 200-day moving averages
# 	ma_data['MA200'] = ma_data['Close'].rolling(window=200).mean()

# 	current_price = ma_data['Close'].iloc[-1]
# 	ma200 = ma_data['MA200'].iloc[-1]

# 	return ma200



if __name__ == '__main__':
    app.run(debug=True)
