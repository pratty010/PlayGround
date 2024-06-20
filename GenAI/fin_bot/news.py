from newspaper import Article, ArticleException
import yfinance as yf
from gnews import GNews
from newsapi import NewsApiClient
from textblob import TextBlob

import pandas as pd
from datetime import datetime, timedelta
from dateutil import tz

def convert_to_local_time(datetime_str, source):
    """
    Converts a given datetime string from UTC to local time.

    Parameters:
    datetime_str (str): The datetime string to be converted. The string should be in either '%a, %d %b %Y %H:%M:%S %Z' (for Google News) or '%Y-%m-%dT%H:%M:%SZ' (for News API) format.
    source (str): The source of the datetime string. It should be either 'g' for Google News or 'n' for News API.

    Returns:
    datetime: The converted datetime object in local time. If the source is invalid, the function will print an error message and exit.

    Note:
    -- This function uses the datetime and pytz libraries.
    - The function first parses the datetime string into a datetime object.
    - It then sets the timezone of the datetime object to UTC.
    - Finally, it converts the datetime object to local time and returns it.
    """

    # Parse the datetime string
    rec_datetime = None
    if source == "g":
        rec_datetime = datetime.strptime(datetime_str, '%a, %d %b %Y %H:%M:%S %Z')
    elif source == "n":
        rec_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')

    if rec_datetime:
        # Set timezone to UTC
        rec_datetime = rec_datetime.replace(tzinfo=tz.tzutc())

        # Convert to local time
        local_datetime = rec_datetime.astimezone(tz.tzlocal()).replace(tzinfo=None)

        # print(rec_datetime, type(rec_datetime))
        # print(local_datetime, type(local_datetime))
        return local_datetime
    else:
        print("Invalid Source for the screener. Available - ['g', 'n']")
        exit()

def yahoo_news_screen(ticker: str) -> list:
    """
    This function retrieves news articles related to a given ticker symbol from Yahoo Finance.

    Parameters:
    ticker (str): The ticker symbol for which news articles are to be retrieved.

    Returns:
    list: A list of dictionaries, where each dictionary represents a news article.
          Each dictionary contains the following keys:
          - "source": The source of the news article, in this case, "Yahoo News".
          - "title": The title of the news article.
          - "publisher": The publisher of the news article.
          - "link": The URL of the news article.
          - "PublishTime": The publication time of the news article.

    Note:
    -- Only for US data primarily.
    - The function uses the yfinance library to retrieve news articles related to the given ticker symbol.
    - The function returns a list of dictionaries, where each dictionary represents a news article.
    - Can work with keywords too. But mostly focused on the ticker symbols for search.
    """

    # Get the Yahoo Finance ticker object for the given ticker symbol.
    yfticker = yf.Ticker(ticker)
    yfnews = yfticker.news # Invoke the news function for the ticker

    print(yfnews[0])
    # To create a useful list of data points for each news article.
    if yfnews:
        news_data = []
        for news in yfnews:
            time = datetime.fromtimestamp(news["providerPublishTime"])
            news_data.append(
                {
                "screener": "Yahoo News",
                "title": news["title"],
                "publisher": news["publisher"],
                "link" : news["link"],
                "PublishTime" : time, 
                # "relatedTickers": news["relatedTickers"]
                }
            )
        # print(news_data)
        return news_data
    else:
        return None
    
def google_news_screen(ticker: str) -> list:
    """
    This function retrieves news articles related to a given ticker symbol from Google News.

    Parameters:
    ticker (str): The ticker symbol for which news articles are to be retrieved.

    Returns:
    list: A list of dictionaries, where each dictionary represents a news article.
          Each dictionary contains the following keys:
          - "source": The source of the news article, in this case, "Google News".
          - "title": The title of the news article.
          - "publisher": The publisher of the news article.
          - "link": The URL of the news article.
          - "PublishTime": The publication time of the news article.

    Note:
    -- This function uses the GNews library to retrieve news articles related to the given ticker symbol.
    - The function returns a list of dictionaries, where each dictionary represents a news article.
    - Can work with keywords too. But mostly focused on the ticker symbols for search.
    - Refer: https://pypi.org/project/gnews/
    """

    # Create a Google News client object with certain parameters
    google_news = GNews()

    google_news.period = '7d'  # For daterange from current
    google_news.max_results = 5 # number of responses across a keyword
    # google_news.exclude_websites = ['yahoo.com', 'cnn.com'] # Exclude news from specific website
    # google_news.start_date = (2020, 1, 1) # Search from 1st Jan 2020
    # google_news.end_date = (2020, 3, 1) # Search until 1st March 2020

    ## Optional parameters
    # google_news.country = 'US'  # News from a specific country 
    # google_news.language = 'english'  # News in a specific language.

    articles = google_news.get_news(ticker)
    print(articles)

    # To create a useful list of data points for each news article.
    if articles:
        news_data = []
        # print(articles[0])
        for article in articles:
            # Parse the string into a datetime object
            time = convert_to_local_time(article["published date"], "g")
            # print(article)

            news_data.append(
                {
                "screener": "Google News",
                "title": article["title"],
                "publisher": article["publisher"]["title"],
                "link" : article["url"],
                "PublishTime" : time,
                # "relatedTickers": [f"{ticker}"]
                }
            )

        # Print the news data
        # print(news_data[0])
        return news_data
    else:
        # Return None if no articles found
        return None

def newsapi_news_screen(ticker: str) -> list:
    """
    This function retrieves news articles related to a given ticker symbol from News API.

    Parameters:
    ticker (str): The ticker symbol for which news articles are to be retrieved.

    Returns:
    list: A list of dictionaries, where each dictionary represents a news article.
          Each dictionary contains the following keys:
          - "source": The source of the news article, in this case, "News API".
          - "title": The title of the news article.
          - "publisher": The publisher of the news article.
          - "link": The URL of the news article.
          - "PublishTime": The publication time of the news article.

    Note:
    -- This function uses the NewsApiClient library to retrieve news articles related to the given ticker symbol.
    - The function returns a list of dictionaries, where each dictionary represents a news article.
    - Can work with keywords too. But mostly focused on the ticker symbols for search.
    """

    # Initialize the NewsApiClient with the API key
    newsapi = NewsApiClient(api_key='7503eaf48b8a4c08980052830f5d19c6')

    # Define a list of news sources to be used for the search
    my_news_sources_list = ["abc-news", "bbc-news", "bloomberg", "buissness-insider", "buzzfeed", "cnn", "cbs-news", "financial-post", "independent", "msnbc", "nbc-news", "the-hindu", "the-hill", "the-times-of-india", "vice-news", "the-wall-street-journal", "wired"]
    news_sources = ",".join(my_news_sources_list)

    # Initialize an empty list to store the news data
    news_data = []

    # Fetch the top headlines related to the given ticker symbol from News API
    top_headlines = newsapi.get_top_headlines(
        q = ticker,
        sources = news_sources,
        # category= "business",
        # country="us",
        # language="en",
    )
    # print(top_headlines["articles"])

    # If there are any articles found, process them
    if top_headlines['totalResults'] > 0:
        for article in top_headlines["articles"]:
            # Parse the string into a datetime object
            time = convert_to_local_time(article["publishedAt"], "n")
            # Append the news data to the list
            news_data.append(
                {
                "screener": "News API - TH",
                "title": article["title"],
                "publisher": article["author"],
                "link" : article["url"],
                "PublishTime" : time, 
                }
            )

    # Get the current date and time
    current_datetime = datetime.now()
    # Get the date and time 1 day ago
    start_datetime = current_datetime - timedelta(weeks=1)
    # Format the date and time as 'YYYY-MM-DDTHH:MM:SS'
    cdatetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    sdatetime = start_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    # Fetch all the articles related to the given ticker symbol from News API
    all_articles = newsapi.get_everything(
        q = ticker,
        sources = news_sources,
        from_param = sdatetime,
        to = cdatetime,
        sort_by='relevancy',
        # language='en',
    )
    # print(all_articles["articles"])

    # If there are any articles found, process them
    if all_articles['totalResults'] > 0:
        for article in all_articles["articles"]:
            # Parse the string into a datetime object
            time = convert_to_local_time(article["publishedAt"], "n")
            # Append the news data to the list
            news_data.append(
                {
                "screener": "News API - Everything",
                "title": article["title"],
                "publisher": article["author"],
                "link" : article["url"],
                "PublishTime" : time, 
                }
            )

    # Return the list of news data
    return news_data

def news_aggregator(ticker):
    """
    This function aggregates news articles from different sources related to a given ticker symbol.

    Parameters:
    ticker (str): The ticker symbol for which news articles are to be retrieved.

    Returns:
    None: The function does not return any value. It saves the aggregated news data to an Excel file.

    Note:
    -- This function calls the respective news screening functions to retrieve news articles from Yahoo Finance, Google News, and News API.
    - The retrieved news articles are then combined into a single DataFrame.
    - The DataFrame is saved to an Excel file named "output.xlsx".
    """

    # collecting all the sources' data
    yahoo_news_data = yahoo_news_screen(ticker)
    google_news_data = google_news_screen(ticker)
    newsapi_news_data = newsapi_news_screen(ticker)

    final_news_data = yahoo_news_data + google_news_data +  newsapi_news_data
    # print(len(final_news_data))

    # Define the columns and index
    columns = ["screener", "title", "publisher", "link", "PublishTime"]
    # Create an DataFrame with the specified columns and the aggragated news_data
    df = pd.DataFrame(final_news_data, columns=columns)
    # print(df)

    # Set the 'ID' column as the index
    df.set_index('screener', inplace=True)
    # print(df)

    df.sort_values(by=["PublishTime"], ascending= False, inplace= True)
    # print(df)

    df.to_excel(f"./data/daily_news_{ticker}.xlsx")

def features(article):
    print(article.title)
    print(article.authors)
    print(article.publish_date)
    print(article.summary)
    # print(article.text)
    # print(article.top_image)

def article_senti(url):
    """
    This function performs sentiment analysis on an article given its URL.

    Parameters:
    url (str): The URL of the article to be analyzed.

    Returns:
    tuple: A tuple containing the polarity and subjectivity scores of the article's sentiment.
           If an error occurs during the download or parsing of the article, the function returns None.

    Note:
    -- This function uses the TextBlob library to perform sentiment analysis.
    - The polarity score is a float within the range [-1.0, 1.0], where -1.0 indicates a negative sentiment,
      0.0 indicates a neutral sentiment, and 1.0 indicates a positive sentiment.
    - The subjectivity score is a float within the range [0.0, 1.0], where 0.0 indicates a very objective statement,
      and 1.0 indicates a very subjective statement.
    """

    try:
        article = Article(url) # create a article object
        article.download() # try to download the article
        article.parse() # parse the article to get the common parameters
        article.nlp() # to the NLP and vectors
        analysis = TextBlob(article.text) # get the analysis data
    except ArticleException:
        print("Error downloading the article - {}".format(url))
        # print(e)
        return None
    
    # print(analysis.sentences)
    # print(analysis.sentiment)
    return analysis.sentiment

def senti_analysis(ticker):
    """
    Performs sentiment analysis on news articles related to a given ticker symbol.

    Parameters:
    ticker (str): The ticker symbol for which news articles are to be analyzed.

    Returns:
    None: The function does not return any value. It saves the DataFrame with sentiment scores to an Excel file.

    Note:
    -- This function reads the daily news data from an Excel file.
    - It creates new columns for sentiment scores.
    - It iterates over each URL in the DataFrame and performs sentiment analysis on the article.
    - The sentiment scores are then assigned to the corresponding rows in the DataFrame.
    - Finally, the DataFrame is saved to an Excel file with sentiment scores.
    """

    daily_news_file = f"./data/daily_news_{ticker}.xlsx"

    df = pd.read_excel(daily_news_file)
    # Set the 'screener' column as the index
    df.set_index('screener', inplace=True)

    # Create a new column for sentiment scores
    df["Sentiment - Polarity"] = 0.0
    df["Sentiment - Subjectivity"] = 0.0

    # Iterate over each URL in the DataFrame
    for index, row in df.iterrows():
        url = row["link"]
        # Perform sentiment analysis on the article
        sentiment_score = article_senti(url)

        if sentiment_score is not None:
            # Assign the sentiment score to the corresponding row in the DataFrame
            df.at[index, "Sentiment - Polarity"] = sentiment_score.polarity
            df.at[index, "Sentiment - Subjectivity"] = sentiment_score.subjectivity
        else:
            df.at[index, "Sentiment - Polarity"] = 0.0
            df.at[index, "Sentiment - Subjectivity"] = 0.0

    # print(df)
    # Save the DataFrame with sentiment scores to an Excel file
    df.to_excel(f"./data/daily_news_{ticker}_with_sentiments.xlsx")

    return df

def main():

    # check for invalid source in time convert
    # convert_to_local_time('2024-06-17 23:04:33+00:00', source="k")
   
    ticker = "NVDA"
    
    # to check for individual source
    # k = yahoo_news_screen(ticker)
    # k = google_news_screen(ticker)
    # k = newsapi_news_screen(ticker)
    # print(k)

    # run this to get all the news for the ticker or keyword
    # news_aggregator(ticker)

    # k = article_senti(url) # setiment anlysis for the article

    # sentment score calculated for each news article found
    df =  senti_analysis(ticker)

    # calacuaklte avg values for all the sentiment scores
    avg_polarity = df["Sentiment - Polarity"].mean()
    avg_subjectivity = df["Sentiment - Subjectivity"].mean()
    print(avg_polarity, avg_subjectivity)

if __name__ == '__main__':
    main()