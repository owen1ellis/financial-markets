import pandas as pd
from copy import copy
from loguru import logger

class DataSource:
    __data: pd.DataFrame

    def __init__(self):
        pass

    def get_data(self, isin_number: str=None, ticker: str=None):
        pass

    def filter_df(self, df: pd.DataFrame, start_date: str=None, end_date: str=None):
        if "date" not in df:
            return df
        try:  
            if not (start_date is None or start_date == ""):
                start_date = pd.to_datetime(start_date)
                df = df[df["date"] >= start_date]
            if not (end_date is None or end_date == ""):
                end_date = pd.to_datetime(end_date)
                df = df[df["date"] <= end_date]
            return df
        except Exception as e:
            logger.error("Failed to Filter on Date {}", e)
            return df

class IncomeData:

    def __init__(self):
        self.data = pd.read_csv("income.csv")

    def get_data(self, isin_number: str=None, ticker: str=None):
        if isin_number is None: #this is for the case where isin is none
            df = copy(self.data[self.data["symbol"]==ticker])
        else:
            df = copy(self.data[self.data["isin"]==isin_number])
        return df
    

class EarningsData(DataSource):

    def __init__(self):
        self.data = pd.read_csv("earnings.csv")
        self.data["date"] = pd.to_datetime(self.data["date"])
        self.data = self.data.sort_values(by="date")

    def get_eps(self, isin_number: str=None, ticker: str=None, start_date_str: str=None, end_date_str: str=None):
        if isin_number is None:
            df = copy(self.data[self.data["symbol"]==ticker])
        else:
            df = copy(self.data[self.data["isin"]==isin_number])
        return self.filter_df(df, start_date_str, end_date_str)
    

    
class NewsData(DataSource):

    def __init__(self):
        self.data = pd.read_csv("news.csv")
        self.data = self.data[["isin", "ticker", "source", "content"]]

    def get_data(self, isin_number: str=None, ticker: str=None):
        if isin_number is None:
            return copy(self.data[self.data["symbol"]==ticker])
        
        return copy(self.data[self.data["isin"]==isin_number]) 

class ExtractionData:

    def __init__(self):
        self. data =  pd.read_csv("extraction.csv")
        self.data = self.data[["isin", "ticker", "news"]]

    def get_data(self, isin_number: str=None, ticker: str=None):
        if isin_number is None:
            return copy(self.data[self.data["symbol"]==ticker])
        
        return copy(self.data[self.data["isin"]==isin_number])
    

isin = "US0378331005"
# print(e_test.get_eps(isin, start_date_str="2003-01-30"))

e_test = IncomeData()
isin = "US0378331005"
# print(e_test.get_data(isin))

    

    

