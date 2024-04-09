
# TrendyTrader

TrendyTrader is an innovative web application designed for real-time stock market analysis. It leverages Twitter sentiment analysis and financial indicators like RSI and moving averages to provide users with comprehensive insights into stock performances. Developed as a capstone project, TrendyTrader showcases advanced data science techniques applied to financial markets.

## Features

- **Sentiment Analysis**: Analyzes Twitter data for sentiment related to specific stocks, offering a sentiment score that reflects public opinion.
- **Financial Indicators**: Displays key financial indicators including current stock price, volume, Relative Strength Index (RSI), and moving averages (MA50 & MA200) to assist in technical analysis.
- **Stock Validation**: Checks if the stock symbol is valid and listed on the US market before fetching and displaying data.

## Getting Started

These instructions will help you set up a copy of TrendyTrader running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- npm (Node.js package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your_username/TrendyTrader.git
```

2. Navigate to the project directory:
```bash
cd TrendyTrader
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install NPM packages and build the React frontend (if applicable):
```bash
npm install
npm run build
```

5. Set up environment variables for API keys (replace 'your_api_key' with your actual API keys):
```bash
export TWITTER_API_KEY='your_api_key'
export STOCKSYMBOL_API_KEY='your_api_key'
```

### Running the Application

To start the Flask backend server:
```bash
flask run
```
or
```bash
python app.py
```


## License

Distributed under the MIT License. See `LICENSE` for more information.



