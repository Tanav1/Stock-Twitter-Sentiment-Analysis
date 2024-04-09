from flask import Flask, request, jsonify
from textblob import TextBlob
import subprocess

app = Flask(__name__)

@app.route('/api/sentiment-analysis')
def get_sentiment_score():
    # Get the stock name from the query parameter
    stock_name = request.args.get('stock_name')

    # Run the sentiment analysis script with the stock name as argument
    result = subprocess.check_output(['python', 'SearchBar.py', stock_name])

    # Parse the result and return it as JSON
    score = float(result.strip())
    response = {'sentiment_score': score}
    return jsonify(response)