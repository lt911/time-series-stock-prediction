__author__ = 'ktc312'

from datetime import *
import pandas as pd
from yahoo_finance import Share
from dateutil.relativedelta import relativedelta

def get_ticker_list():
    # get the all the ticker symbols from the csv file
    # can update the ticker symbols by replacing this file
    df = pd.read_csv('Yahoo Ticker Symbols - Jan 2015.csv')
    ticker_list = df['Ticker'].drop_duplicates().values.tolist()
    return ticker_list

def get_ticker_to_name_dict():
    # get the all the ticker symbols from the csv file
    df = pd.read_csv('Yahoo Ticker Symbols - Jan 2015.csv')
    ticker_to_name_dict = df.set_index('Ticker')['Name'].drop_duplicates().to_dict()
    return ticker_to_name_dict

def get_company_name(ticker_symbol):
    ticker = ticker_symbol.upper()
    name_dict = get_ticker_to_name_dict()
    return name_dict[ticker]

def get_today():
    # get the date of today
    today = datetime.now().strftime("%Y-%m-%d")
    return today


def get_data(ticker_symbol, start_date, end_date):
    # get and clean historical stock price data

    stock = Share(ticker_symbol)
    data = pd.DataFrame(stock.get_historical(start_date,end_date))[['Date','Adj_Close']]

    data['Adj_Close'] = pd.to_numeric(data['Adj_Close'])
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by = 'Date', ascending = True)


    return data


def test_ticker(ticker_symbol):
    # test if there are data available for the user entered ticker symbol
    today = datetime.now()
    from_date = today - relativedelta(months=2)
    today = today.strftime("%Y-%m-%d")
    from_date = from_date.strftime("%Y-%m-%d")
    stock = Share(ticker_symbol)
    test = stock.get_historical(from_date, today)
    if not test:
        return False
    return True
