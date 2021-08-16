import yfinance as yf
import pandas as pd

class Company:
    def __init__(self, name):
        self.name = name.upper()
        self.ticker = yf.Ticker(name.lower())
        self.financials = self.ticker.financials
        self.balancesheet = self.ticker.balance_sheet
        self.cashflow = self.ticker.cashflow

        self.raw_data = {
            'Year' : self.financials.columns
        }
        self.percent_data = {
            'Year' : self.financials.columns
        }
        self.raw_dataframes = []
        self.percent_dataframes = []
    
    def add_data(self, data):
        self.raw_data[data] = self.get_raw_data(data)
        self.percent_data[data] = self.get_percent_data(data)
        return
    
    def generate_raw_dataframe(self, dataset, col, row):
        self.raw_dataframes.append(pd.DataFrame(dataset, columns=[col, row]))
    
    def generate_percent_dataframe(self, dataset, col, row):
        self.percent_dataframes.append(pd.DataFrame(dataset, columns=[col, row]))

    def get_raw_data(self, data):
        try:
             return [x/1000000 for x in self.financials.loc[data].tolist()]
        except:
            pass
        try:
            return [x/1000000 for x in self.balancesheet.loc[data].tolist()]
        except:
            pass
        try:
            return [x/1000000 for x in self.cashflow.loc[data].tolist()]
        except:
            pass

        print("Error 1: Company $"+self.name+ " has no data available for "+data)
        return [0]
    
    def get_percent_data(self, data):
        try:
             return self.financials.loc[data].pct_change(periods=-1).tolist()
        except:
            pass
        try:
            return self.balancesheet.loc[data].pct_change(periods=-1).tolist()
        except:
            pass
        try:
            return self.cashflow.loc[data].pct_change(periods=-1).tolist()
        except:
            pass

        print("Error 1: Company $"+self.name+ " has no data available for "+data)
        return [0]