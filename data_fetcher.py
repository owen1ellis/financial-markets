import pandas as pd
from copy import copy

earnings_df = pd.read_csv("earnings.csv")
earnings_df["date"] = pd.to_datetime(earnings_df["date"])
earnings_df = earnings_df.sort_values(by="date")

income_df = pd.read_csv("income.csv")
# income_df["date"] = pd.to_datetime(income_df["date"])

extraction_df = pd.read_csv("extraction.csv")

class IncomeData:

    def __init__(self):
        self.data = income_df

    def get_data(self, isin_number: str=None, ticker: str=None):
        if isin_number is None: #this is for the case where isin is none
            return copy(self.data[self.data["symbol"]==ticker])
        
        return copy(self.data[self.data["isin"]==isin_number])
    

class EarningsData:

    def __init__(self):
        self.data = earnings_df

    def get_eps(self, isin_number: str=None, ticker: str=None):
        if isin_number is None:
            return copy(self.data[self.data["symbol"]==ticker])
        
        return copy(self.data[earnings_df["isin"]==isin_number])
    

    
e_test = EarningsData()
isin = "US0378331005"
# print(e_test.get_eps(isin))


e_test = IncomeData()
isin = "US0378331005"
# print(e_test.get_data(isin))

news_df = pd.read_csv("news.csv")
news_df = news_df[["isin", "ticker", "source", "content"]]
print(news_df)

class NewsData:

    def __init__(self):
        self.data = news_df

    def get_news(self, isin_number: str=None, ticker: str=None):
        if isin_number is None:
            return copy(self.data[self.data["symbol"]==ticker])
        
        return copy(self.data[news_df["isin"]==isin_number]) 

class ExtractionData:

    def __init__(self):
        self.data = extraction_df[["isin", "ticker", "news"]]

    def get_data(self, isin_number: str=None, ticker: str=None):
        if isin_number is None:
            return copy(self.data[self.data["symbol"]==ticker])
        
        return copy(self.data[extraction_df["isin"]==isin_number])
    

