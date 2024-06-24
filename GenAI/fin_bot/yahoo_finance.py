from datetime import datetime
import ta
import yfinance as yf

import tradingview_ta as tdta
from tradingview_ta import TA_Handler, Interval, Exchange

import pandas as pd
import matplotlib.pyplot as plt
import json

pd.options.mode.copy_on_write = True

def get_info(ticker: yf.Ticker) -> dict:
    """
    This function retrieves and returns detailed information about a stock ticker.

    Parameters:
    ticker (yf.Ticker): The yfinance Ticker object for the stock.

    Returns:
    dict: A dictionary containing detailed information about the stock.

    Note:
    The returned dictionary contains various attributes such as the stock's name,
    symbol, currency, country, etc.
    """

    # get ticker info
    info = ticker.info

    # basics = [info.shortName, info.zip,  info.longBusinessSummary, info.exchange, info.marketCap]
    # industry = [info.industry , info.industryKey, info.sector, info.sectorKey]
    # price_action = [info.previousClose, info.open, info.dayLow, info.dayHigh, info.volume]


    # show ISIN code
    # ISIN = International Securities Identification Number
    isin = ticker.isin
    # print(isin)

    print(type(info))
    return info

def get_history(ticker: yf.Ticker, tp: str) -> {pd.DataFrame, dict}:
    """
    This function retrieves historical stock prices and metadata for a given ticker and time period.

    Parameters:
    ticker (yf.Ticker): The yfinance Ticker object for the stock.
    tp (str): The time period for which to retrieve historical data.

    Returns:
    Tuple[pd.DataFrame, dict]: A tuple containing the historical stock prices (as a pandas DataFrame) and the metadata (as a dictionary).
    """

    history = ticker.history(period=tp)
    history_metadata = ticker.history_metadata

    return history, history_metadata

def get_actions(ticker: yf.Ticker) -> pd.DataFrame:
    """
    Retrieves and returns a DataFrame containing future and historic earnings dates for the given stock.
    The function fetches at most the next 4 quarters and last 8 quarters by default.
    If more data is needed, the limit parameter can be increased.

    Parameters:
    ticker (yf.Ticker): The yfinance Ticker object for the stock.

    Returns:
    pd.DataFrame: A DataFrame containing the earnings dates.
    """
    # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default.
    # Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
    earning_dates = ticker.get_earnings_dates(limit = 14)
    ac = ticker.actions # all actions available 
    div = ticker.dividends # Return dividend section of actions
    splits = ticker.splits # Return splits section of actions
    # cap_gains = ticker.capital_gains # only for mutual funds & etfs

    return ac

def income_sheet_fa(ticker, time_period) -> pd.DataFrame:
    """
    Generate a financial analysis report for the income statement.

    Parameters:
    ticker (yf.Ticker): The yfinance ticker object for the stock.
    time_period (str): The time period for the financial analysis. It can be 'annually' or 'quaterly'.

    Returns:
    None

    Notes:
    - The function fetches the income statement data from the yfinance ticker object, prepares it for analysis, calculates additional features, and saves the final statement in an Excel file.
    - It also plots some useful information in a matplotlib figure.

    Definations:
    - Total Revenue = Operating Revenue(earnings from offering services or goods) + Non-Operating Revenue(earning from non-core businesses activities)
    - Costs of Goods Sold and Services Rendered (COGS) = Cost of goods and services in an income statement denote the expenses incurred to sell the final goods.
    - Gross Profit = Total Revenue - Costs of Goods Sold and Services Rendered (COGS)
    - Operating expenses (OPEX) = These denote costs linked to the goods and services offered by a business, such as rent, office, supplies etc
    - Earnings Before Interest, Taxes, Depreciation and Amortization (EBITDA) = EBITDA is the net income of a business after deducting interest, taxes, depreciation and amortization = Gross Profit - OPEX
    - Depreciation & Amortization (D&A) = These are special types of expenses that are spread over a long period. They include the decline in the value of equipment used in producing goods and services.
    - Earnings Before Tax (EBIT) = Operating Income/Profit = EBIDTA - D&A
    - Earnings Before Taxes(EBT) = EBIT - Intrest Expense
    - Net Income/PAT = EBT - Taxes
    """

    # get ticker from the yfinance ticker object
    stock = ticker.ticker

    # to check if the right time period is passed
    if time_period == "annually":
        income_stmt_raw_T = ticker.income_stmt
    elif time_period == "quaterly":
        income_stmt_raw_T = ticker.quarterly_income_stmt
    else:
        print("Please enter a valid time period")
        exit()

    # Drop the empty values and transpose the matrix
    income_stmt_raw_T.dropna()
    income_stmt = income_stmt_raw_T.T
    

    # store the raw statement in the database for later query
    income_stmt_raw_T.to_excel(f"fin_bot/data/financials/income_statements/income_stmt_{time_period}_{stock}_raw_T.xlsx")
    # print(income_stmt)
    income_stmt.to_excel(f"fin_bot/data/financials/income_statements/income_stmt_{time_period}_{stock}_raw.xlsx")

    # extract the useful features from the statement
    columns = [
        "Total Revenue",
        "Cost Of Revenue",
        "Gross Profit",
        "Operating Expense",
        "EBITDA",
        "Operating Income",
        "Pretax Income",
        "Tax Provision",
        "Net Income", 
        "Diluted Average Shares", 
        "Basic Average Shares"
        ]

    # pre-process the values to million dollar level
    income_stmt_final = income_stmt[columns]
    for col in income_stmt_final.columns.values:
        income_stmt_final.loc[:, col] = income_stmt_final.loc[:, col] / 1000000

    # adding the EPS features
    income_stmt_final["Diluted EPS"] = income_stmt_final["Net Income"] / income_stmt_final["Diluted Average Shares"]
    income_stmt_final["Basic EPS"] = income_stmt_final["Net Income"] / income_stmt_final["Basic Average Shares"]

    # Adding some consolidated features
    income_stmt_final["TE"] = income_stmt_final["Total Revenue"] - income_stmt_final["Pretax Income"]
    income_stmt_final["OI"] = income_stmt_final["Pretax Income"] - income_stmt_final["Operating Income"]

    income_stmt_final.insert(6, "Other Income", income_stmt_final["OI"])
    income_stmt_final.insert(7, "Total Expenditure", income_stmt_final["TE"])

    income_stmt_final.drop(columns=['TE'], inplace=True)
    income_stmt_final.drop(columns=['OI'], inplace=True)

    # more readable labels
    income_stmt_final.rename(
        columns = {
            'Cost Of Revenue': 'Cost Of Goods Sold/COGS',
            "Operating Expense": "Operating Expense/OPEX",
            'Gross Profit': 'Gross Profit/Margin',
            "Operating Income" : "Operating Income/EBIT",
            "Net Income": "Net Income/PAT",
        }, 
        inplace=True
        )

    # save the final statement
    income_stmt_final.to_excel(f"fin_bot/data/financials/income_statements/income_stmt_{time_period}_{stock}.xlsx")

    # plot some useful informmation.
    plt.figure(figsize=(22, 18))

    ax1 = plt.subplot(211)
    ax1.plot(income_stmt_final.index, income_stmt_final['Total Revenue'], label='Total Revenue', color='green')
    ax1.plot(income_stmt_final.index, income_stmt_final['Total Expenditure'], label='Total Expenditure', color='red')
    ax1.plot(income_stmt_final.index, income_stmt_final['Net Income/PAT'], label='Net Income/PAT', color='black')
    ax1.set_title('Top and Bottom Line')
    ax1.grid(True)
    ax1.set_xlabel('Report Date')
    ax1.set_ylabel('Price in million dollars')
    ax1.legend()

    ax2 = plt.subplot(212, sharex=ax1)
    columns_to_plot = ['Diluted EPS', 'Basic EPS']
    income_stmt_final[columns_to_plot].plot(kind='bar', stacked=False)

    ax2.set_title('EPS Growth')
    ax2.set_xlabel('Report Date')
    ax2.set_ylabel('Price in million dollars')
    # ax2.legend()

    plt.show()

    return income_stmt_final

def balance_sheet_fa(ticker, time_period) -> pd.DataFrame:
    """
    This function generates a financial analysis report based on the balance sheet of a given stock.

    Parameters:
    ticker (yf.Ticker): The yfinance ticker object for the stock.
    time_period (str): The time period for the financial analysis. It can be either 'annually' or 'quaterly'.

    Returns:
    None
    
    Notes:
    - The Balance Sheet is carried forward on basis of the defined time period.
    - An asset/liability is considered current if it can reasonably be converted into cash within one year. 
    - Assets
        -- Current
            --- Cash Cash Equivalents And Short Term Investments
            --- Inventory
            --- Accounts Receivable
        -- Non-Current 
            --- Accumulated Depreciation
            --- Net PPE
            --- Investments And Advances
    - Liabilities
        -- Current
            --- Accounts Payable
            --- Current Debt
            --- Current Deferred Liabilities
        -- Non-Current 
            --- Long Term Debt
            --- Other Non-Current Liabilities
    - Equity
        -- Stockholders Equity
        -- Retained Earnings
        -- Other Equity Adjustments
    """

    # Extract the stock symbol from the ticker object
    stock = ticker.ticker

    # Check the time period and fetch the corresponding balance sheet data
    if time_period == "annually":
        balance_sheet_raw_T = ticker.balance_sheet
    elif time_period == "quaterly":
        balance_sheet_raw_T = ticker.quarterly_balance_sheet
    else:
        print("Please enter a valid time period")
        exit()

    # Clean the data by removing any NaN values
    balance_sheet_raw_T.dropna()
    balance_sheet = balance_sheet_raw_T.T

    # Save the raw balance sheet data to an Excel file
    balance_sheet_raw_T.to_excel(f"fin_bot/data/financials/balance_sheet/balance_sheet_{time_period}_{stock}_raw_T.xlsx")
    # print(balance_sheet)
    balance_sheet.to_excel(f"fin_bot/data/financials/balance_sheet/balance_sheet_{time_period}_{stock}_raw.xlsx")

    # Define the columns to include in the final balance sheet report
    columns = [
        "Total Assets",
        "Current Assets",
        "Cash And Cash Equivalents",
        "Cash Cash Equivalents And Short Term Investments",
        "Inventory",
        "Accounts Receivable",
        "Other Current Assets",
        "Total Non Current Assets",
        "Gross PPE",
        "Accumulated Depreciation",
        "Net PPE",
        "Investments And Advances",
        "Other Non Current Assets",
        "Total Liabilities Net Minority Interest",
        "Current Liabilities",
        "Accounts Payable",
        "Current Debt",
        "Current Deferred Liabilities",
        "Total Non Current Liabilities Net Minority Interest",
        "Long Term Debt",
        "Other Non Current Liabilities",
        "Stockholders Equity",
        "Common Stock",
        "Retained Earnings",
        "Other Equity Adjustments",
        ]

    # Create a new DataFrame with the selected columns
    balance_sheet_final = balance_sheet[columns]

    # Convert the values in the DataFrame to millions for easier readability
    for col in balance_sheet_final.columns.values:
        balance_sheet_final.loc[:, col] = balance_sheet_final.loc[:, col] / 1000000

    # Rename specific columns for better readability
    balance_sheet_final.rename(
        columns = {
            'Other Short Term Investments' : 'Short Term Investments/Market Securities',
            'Total Liabilities Net Minority Interest' : 'Total Liabilities',
            'Total Non Current Liabilities Net Minority Interest' : 'Total Non-Current Liabilities',
            'Other Non Current Liabilities' : 'Other Non-Current Liabilities'
            }, 
        inplace=True
        )

    # Save the final balance sheet report to an Excel file
    balance_sheet_final.to_excel(f"fin_bot/data/financials/balance_sheet/balance_sheet_{time_period}_{stock}.xlsx")

    # Create a plot to visualize the debt vs equity
    plt.figure(figsize=(22, 18))

    ax1 = plt.subplot(211)
    ax1.plot(balance_sheet_final.index, balance_sheet_final['Stockholders Equity'], label='Stockholders Equity', color='green')
    ax1.plot(balance_sheet_final.index, balance_sheet_final['Long Term Debt'], label='Long Term Debt', color='red')
    ax1.set_title('Debt vs Equity')
    ax1.grid(True)
    ax1.set_xlabel('Report Date')
    ax1.set_ylabel('Price in million dollars')
    ax1.legend()

    # Create a plot to visualize the assets vs liabilities
    ax2 = plt.subplot(212, sharex=ax1)
    columns_to_plot = ['Current Assets', 'Current Liabilities']
    balance_sheet_final[columns_to_plot].plot(kind='bar', stacked=False)

    ax2.set_title('Assets vs Liabilities')
    ax2.set_xlabel('Report Date')
    ax2.set_ylabel('Price in million dollars')

    # Display the plot
    plt.show()

    return balance_sheet_final

def cashflow_stmt_fa(ticker, time_period) -> pd.DataFrame:
    """
    This function generates a financial analysis report based on the balance sheet of a given stock.

    Parameters:
    ticker (yf.Ticker): The yfinance ticker object for the stock.
    time_period (str): The time period for the financial analysis. It can be either 'annually' or 'quaterly'.

    Returns:
    None
    
    Notes:
    - The Balance Sheet is carried forward on basis of the defined time period.

    """

    # Extract the stock symbol from the ticker object
    stock = ticker.ticker

    # Check the time period and fetch the corresponding balance sheet data
    if time_period == "annually":
        cashflow_raw_T = ticker.cashflow
    elif time_period == "quaterly":
        cashflow_raw_T = ticker.quarterly_cashflow
    else:
        print("Please enter a valid time period")
        exit()

    # Clean the data by removing any NaN values
    cashflow_raw_T.dropna()
    cashflow = cashflow_raw_T.T

    # Save the raw balance sheet data to an Excel file
    cashflow_raw_T.to_excel(f"fin_bot/data/financials/cashflow/cashflow_{time_period}_{stock}_raw_T.xlsx")
    cashflow.to_excel(f"fin_bot/data/financials/cashflow/cashflow_{time_period}_{stock}_raw.xlsx")

    # Define the columns to include in the final balance sheet report
    columns = [
        "Free Cash Flow",
        "Operating Cash Flow",
        "Net Income From Continuing Operations",
        "Depreciation And Amortization", 
        "Change In Working Capital",
        "Change In Receivables",
        "Change In Inventory",
        "Change In Payables And Accrued Expense",
        # "Change In Other Current Assets",
        # "Change In Other Current Liabilities",
        "Investing Cash Flow",
        "Purchase Of Investment",
        "Net PPE Purchase And Sale",
        "Sale Of Investment",
        # "Net Other Investing Changes",
        "Financing Cash Flow",
        "Net Common Stock Issuance",
        "Common Stock Dividend Paid",
        "Cash Dividends Paid",
        "Long Term Debt Payments",
        "Long Term Debt Issuance",
        "Net Other Financing Charges",
        ]

    # Create a new DataFrame with the selected columns
    cashflow_final = cashflow[columns]

    # adding the Other Income feature
    cashflow_final["Other Income"] = cashflow["Stock Based Compensation"] + cashflow["Other Non Cash Items"]



    # Convert the values in the DataFrame to millions for easier readability
    for col in cashflow_final.columns.values:
        cashflow_final.loc[:, col] = cashflow_final.loc[:, col] / 1000000

    # Rename specific columns for better readability
    cashflow_final.rename(
        columns = {
            'Net Income From Continuing Operations' : 'Net Income',
            # Add this
            }, 
        inplace=True
        )

    # Save the final balance sheet report to an Excel file
    cashflow_final.to_excel(f"fin_bot/data/financials/cashflow/cashflow_{time_period}_{stock}.xlsx")

    return cashflow_final

def get_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    This function calculates and adds various technical indicators to the given stock price data.
    The indicators include Simple Moving Average (SMA), Exponential Moving Average (EMA), 
    Moving Average Convergence Divergence (MACD), Relative Strength Index (RSI), and Bollinger Bands.

    Parameters:
    data (pd.DataFrame): The DataFrame containing the stock price data. The DataFrame should have a 'Close' column.

    Returns:
    None. The function modifies the input DataFrame in-place by adding the calculated indicators as new columns.
    """

    # Adding Simple Moving Average (SMA) and Exponential Moving Average (EMA)
    data['SMA'] = ta.trend.sma_indicator(data['Close'], window=14)
    data['EMA'] = ta.trend.ema_indicator(data['Close'], window=14)

    # Adding Moving Average Convergence Divergence (MACD)
    data['MACD'] = ta.trend.macd_diff(data['Close'])

    # Adding Relative Strength Index (RSI)
    data["RSI"] = ta.momentum.rsi(data['Close'])
    data["StochRSI"] = ta.momentum.stochrsi(data['Close'])
    data["StochRSI_d"] = ta.momentum.stochrsi(data['Close'])
    data["StochRSI_k"] = ta.momentum.stochrsi(data['Close'])

    # Adding Bollinger Bands
    data['BB_high'] = ta.volatility.bollinger_hband(data['Close'])
    data['BB_mid'] = ta.volatility.bollinger_mavg(data['Close'])
    data['BB_low'] = ta.volatility.bollinger_lband(data['Close'])

    # Display the data with indicators.
    # print(data)
    data.to_excel(f"fin_bot/data/stocks/indicators.xlsx")

    # plotting the Moving averages against dates
    plt.figure(figsize=(20, 16))
    plt.plot(data.index, data['Adj Close'], label='Price', color='black')
    plt.plot(data.index, data['SMA'], label='SMA', color='blue')
    plt.plot(data.index, data['EMA'], label='EMA', color='red')
    plt.grid(True)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('EMA vs. SMA')
    plt.xticks(data.index, rotation=90)
    plt.legend()
    plt.show()

    # plotting the RSI against price movement
    plt.figure(figsize=(20, 16))

    ax1 = plt.subplot(211)
    ax1.plot(data.index, data['Adj Close'], label='Price', color='black')
    ax1.set_title('Adjusted Close Price')
    ax1.grid(True)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('StockPrice')
    # ax1.set_xticks(data.index, rotation=90)
    ax1.legend()

    ax2 = plt.subplot(212, sharex=ax1)
    ax2.plot(data.index, data['RSI'], label='Price', color='black')
    ax2.axhline(0, linestyle="--", alpha=0.5)
    ax2.axhline(10, linestyle="--", alpha=0.5)
    ax2.axhline(20, linestyle="--", alpha=0.5)
    ax2.axhline(30, linestyle="--", alpha=0.5)
    ax2.axhline(40, linestyle="--", alpha=0.5)
    ax2.axhline(50, linestyle="--", alpha=0.5)
    ax2.axhline(60, linestyle="--", alpha=0.5)
    ax2.axhline(70, linestyle="--", alpha=0.5)
    ax2.axhline(80, linestyle="--", alpha=0.5)
    ax2.axhline(90, linestyle="--", alpha=0.5)
    ax2.axhline(100, linestyle="--", alpha=0.5)

    ax2.set_title('RSI')
    ax1.grid(False)
    ax2.set_xlabel('Date')
    # ax2.xticks(data.index, rotation=90)
    ax2.legend()

    plt.show()

    return data

def get_recommendations(ticker: yf.Ticker) -> pd.DataFrame:
    """
    This function retrieves the recommendations made by analysts for the given stock.

    Parameters:
    ticker (yf.Ticker): The yfinance Ticker object for the stock.

    Returns:
    tuple: A tuple containing two pandas DataFrames. The first DataFrame contains the recommendations made by analysts, and the second DataFrame contains a summary of these recommendations.
    """
    rec = ticker.get_recommendations()
    rec_summ = ticker.recommendations_summary
    updwn = ticker.upgrades_downgrades

    return rec

def tradingview_tech_analysis(stock:str, exchange:str, country:str) -> tuple:
    """
    This function retrieves technical analysis data from TradingView for a given stock.

    Parameters:
    stock (str): The symbol of the stock.
    exchange (str): The exchange where the stock is traded.
    country (str): The country where the stock is traded.

    Returns:
    tuple: A tuple containing two pandas DataFrames. The first DataFrame contains the technical indicators, and the second DataFrame contains a summary of the technical analysis.
    """

    # Initialize the TA_Handler with the necessary parameters
    handler = TA_Handler(
        symbol=stock,
        exchange="",
        screener="",
        interval="30m",
        timeout=None
    )

    # Set the exchange as a crypto or stock
    handler.set_exchange_as_crypto_or_stock(exchange)

    # Set the screener as a stock
    handler.set_screener_as_stock(country)

    # Get the technical indicators
    indicators = handler.get_indicators()

    # Get the summary of the technical analysis
    analysis = handler.get_analysis()
    
    # Return the indicators and analysis summary
    return indicators, analysis.summary

def main():

    stock = "AAPL"
    ticker = yf.Ticker(stock)
    # stocks = "AAPL MSFT TSLA" 
    # tickers = yf.Tickers(stocks) # get data for all the seperated tickers

    
    info = get_info(ticker)
    # info = get_info(tickers.tickers["TSLA"])
    # print(json.dumps(info, indent=4))

    hist = get_history(ticker, "5d")
    # print(hist[0].columns.values)
    # print(hist[0].head)
    # print(json.dumps(hist[1], indent=4))

    # actions = get_actions(ticker)
    # print(actions.head)

    # stmt = income_sheet_fa(ticker, "annually")
    stmt = balance_sheet_fa(ticker, "annually")
    # stmt = cashflow_stmt_fa(ticker, "annually")
    print(stmt)

    data = yf.download(stock, start='2023-12-01', end=None)
    # print(data)
    indicators = get_indicators(data)
    # print(indicators)
    
    # rec = get_recommendations(ticker)
    # rec = tradingview_tech_analysis(stock, exchange, country)
    # print(rec)
  

if __name__ ==  "__main__":
    main()