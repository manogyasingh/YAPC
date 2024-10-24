# Converted from 1.ipynb

# ![](https://algo-assets.amplifyme.com/quant/citadelchallenge1.png)

# # Quant Simulation Challenge 1 - Non-skewed Price Making
#
# Your first challenge is to work independently to follow the instructor to complete the challenges below. This will help give you the foundations for the future challenges.
#
# The goal of this challenge is to automate the market-making process, using object-orientated programming to automatically create a bid-offer spread around the reference price. You're expected to provide a 2% non-skewed bid and offer for each trade.
#
# Good luck!
#
# To start let's import the packages to be used within this notebook.

# The code in this cell is used to import the packages to be used throughout this notebook.
# The following are private packages available only during this simulation:
from AmplifyQuantTrading import Data
from AmplifyQuantTrading import Exchange
from AmplifyQuantTrading import MarketMaker
from AmplifyQuantTrading import HedgeFund as hf
# The following are publicly available packages:
from matplotlib import pyplot as plt
from pandas import *


# HIDDEN PARAMS BOX

# The code below will assign the prices data series and price_requests data series to the two variables to make them available throughout the project.

prices = Data.get_price_series('PricestoFeedserver2011')
price_requests = Data.get_price_requests('PriceRequeststoFeedserver2011')

# ### a) Iterate through the first ten price requests and append to the test_requests list.
#
# The price requests are being reduced to just 10 items to allow for easier creation of an algorithm on a smaller dataset.

test_requests = []

for index in range(0, 10): # Select the first ten prices in the data.
    test_requests.append(price_requests[index])

# Now that you have appended the items to **test_requests** you can find them in the output below.
#
# The output should follow the format **[ [ ticker, date, volume ], [ ticker, date, volume ], ... ]**

print(test_requests)

# ##### The cell below is used to grade the work after the event. You do not need to do anything here.

# GRADING CELL

# ### b) Identify the reference prices for the first ten requests
#
# Now iterate through the *test_requests* and match them with the relevant *date* and *ticker* in the *prices* variable. Store these reference prices and price_requests in a list called *request_with_prices*.
#
# #### request_with_prices should be in the format [ ([price requests], refPrice), ([price requests], refPrice), ...  ]

request_with_prices = []

for price in prices:  # Iterate through all the prices to match them against the price requests.
    for request in test_requests:  # Iterate through the requests from the Hedge Funds.
        if price[0] == request[0] and price[1] == request[1]:
            request_with_prices.append((request, price[2]))

# Run the cell below to check the output for test_requests.
#
# ##### The output from test_requests should be in the format: [ ( [price requests], refPrice ), ( [price requests], refPrice ), ... ]

print(request_with_prices)

#
# ##### The cell below is used to grade the work after the event. You do not need to do anything here.

# GRADING CELL

# ### c) Create a non-skewed bid and offer for the request_with_prices
#
# Now that you have paired the Request with a Reference Price you can create your bid and offer. We will be using Object Oriented Programming here to pass our trade to the Hedge Fund later on.
#
# ### **QuotedTrade object**
# This object will be used to quote trades and send them to the hedge funds. The object contains the following attributes:
# * ticker: String
# * trade_volume: Integer
# * ref_price: Float
# * bid_price: Float
# * offer_price: Float
# * date: Integer

class QuotedTrade:
    def __init__(self, ticker, trade_volume, ref_price, bid_price, offer_price,
                 date):
        self.ticker = ticker
        self.trade_volume = trade_volume
        self.ref_price = ref_price
        self.bid_price = bid_price
        self.offer_price = offer_price
        self.date = date

    def __str__(self):
        return f'Trade Request for {self.ticker}, {self.trade_volume} shares @ {self.ref_price} on {self.date}. Bid Price: {self.bid_price} and Offer Price: {self.offer_price}'

    def __repr__(self):
        return f'QuotedTrade(ticker={self.ticker}, trade_volume={self.trade_volume}, ref_price={self.ref_price}, bid_price={self.bid_price}, offer_price={self.offer_price}, date={self.date})'

# Now that you have initialised the QuotedTrade object you can use this as a template for trades.
#
# To do this create your bid and offer in the task below by assigning a 2% spread on each side based on the reference price.

quoted_trades = []

for matched in request_with_prices:
    ref_price = matched[1]
    request = matched[0]
    bid_price = ref_price * (1 - 0.02)  # Create the bid spread
    offer_price = ref_price * (1 + 0.02)  # Create the offer spread

    # Now create the QuotedTrade object and append it to the quoted_trades list.
    quoted_trade = QuotedTrade(
        ticker=request[0],
        trade_volume=request[2],
        ref_price=ref_price,
        bid_price=bid_price,
        offer_price=offer_price,
        date=request[1]
    )
    quoted_trades.append(quoted_trade)


# Run the cell below to check the output for quotedTrades. 
#
# ##### In the output below you should see many QuotedTrade objects with their details.

print(quoted_trades)

# ##### The cell below is used to grade the work after the event. You do not need to do anything here.

# GRADING CELL

# ### d) Interact with the Hedge Fund to Show quoted_trades and recieve a response.
#
# Using the *quoted_trades* list interact with the HF object to receive a "Buy, Sell, Refuse" response from the HF and store these *HfResponse* objects in an list called *hf_responses*.
#
# ##### Sends the quoted_trade object to the hedge fund to make a decision for a trade.
# ```python
# hf.show(QuotedTrade)
# ```
# ***Parameters:***
# * QuotedTrade: Custom Object
#
# ***Returns:***
# * HfResponse( ticker: String, trade_volume: Integer, trade_price: Float, hf_action: String, ref_price: Float, bid_price: Float, offer_price: Float, date: Integer )

hf_responses = []

for trade in quoted_trades:
    response = hf.show(trade)  # Assign the response to the return from the hf.show()
    hf_responses.append(response)

# Run the cell below to check the output for the responses from the Hedge Fund. 
#
# ##### In the output below you should see many HfResponse objects with their details.

print(hf_responses)

# ##### The cell below is used to grade the work after the event. You do not need to do anything here.

# GRADING CELL

# ### e) Store the quotedTrades and completedTrades in the Market Maker (MM Object)
#
# ## Initialise the Market Maker Object
#
# To be able to use the Market Maker in this simulation we run the code in the cell below to create the object. The Market Maker object contains the following properities.
#
# #### Market Maker object contains:
# * current_positions: Dictionary of current_position objects - {ticker: String, current_position: Object}
#   * current_position: Custom Object
#     * ticker: String
#     * position_volume: Integer
#     * open_price: Float
#     * date: Integer
# * quoted_trades: List of quoted_trade objects - [quoted_trade, quoted_trade, …]
#   * quoted_trade: Custom Object
# * completed_trades: List of completed_trade objects - [completed_trade, completed_trade, ...]
#   * completed_trade: Custom Object
# * ETF_positions: List of completed_trade objects - [completed_trade, completed_trade, ...]
#   * completed_trade: Custom Object
#

stocks = ['ESTOXX', 'SPX', 'UKX', 'NKY', 'MSCI-ETF']
mm = MarketMaker.mm(stocks)

#  As a Market Maker, it is imperative to keep a log of the trades quoted and clients' responses. As a result, interact with the MM object to store the quoted_trades lists into the logs.
#
# #### Add a trade to Market Makers history
# ```python
# mm.add_quoted_trade(QuotedTrade)
# ```
# ***Parameters:***
# * QuotedTrade: Custom Object
#
# ***Returns:***
# * String: Indicating a successfully added trade or failed added trade.

for quote in quoted_trades:
    mm.add_quoted_trade(quote)


# Run the cell below to check the output for market maker quoted_trades. 
#
# ##### In the output below you should see many QuotedTrade objects with their details.

print(mm.quoted_trades)

# ### Create another object to be used during this event following a similar structure to the QuotedTrade class.
#
# **Create a CompletedTrade object**
#
# This object will be used to log successful trades to the market maker object. The object should contain the following attributes:
# * ticker: String
# * trade_volume: Integer
# * trade_price: Float
# * mm_action: String
# * ref_price: Float
# * bid_price: Float
# * offer_price: Float
# * date: Integer

class CompletedTrade:
    def __init__(self, ticker, trade_volume, trade_price, mm_action, ref_price, bid_price, offer_price, date):
        self.ticker = ticker
        self.trade_volume = trade_volume
        self.trade_price = trade_price
        self.mm_action = mm_action
        self.ref_price = ref_price
        self.bid_price = bid_price
        self.offer_price = offer_price
        self.date = date

    def __str__(self):
        return f'CompletedTrade(ticker={self.ticker}, volume={self.trade_volume}, price={self.trade_price}, action={self.mm_action}, date={self.date})'

    def __repr__(self):
        return f'CompletedTrade(ticker={self.ticker}, trade_volume={self.trade_volume}, trade_price={self.trade_price}, mm_action={self.mm_action}, ref_price={self.ref_price}, bid_price={self.bid_price}, offer_price={self.offer_price}, date={self.date})'


# ### Interact with the MM object to store the CompletedTrade objects into the logs.
#
# #### Update the Market Makers current positions.
# ```python
# mm.add_trade(CompletedTrade)
# ```
# ***Parameters:***
# * CompletedTrade: Custom Object
#
# ***Returns:***
# * String: Indicating a successfully added trade or failed added trade.
#
# #### Throughout this simulation the hfAction has the possibility to be the following: "buy", "sell" and "refuse"

for response in hf_responses:  # Loops through the completedTrades for each response

    # Collection of conditionals for "buy", "sell" and "refuse"
    if response.hf_action == "buy":  # Identifies the HF action to be converted into the MM action
        mm_action = "sell"
        trade_price = response.bid_price
        completed_trade = CompletedTrade(
            ticker=response.ticker,
            trade_volume=response.trade_volume,
            trade_price=trade_price,
            mm_action=mm_action,
            ref_price=response.ref_price,
            bid_price=response.bid_price,
            offer_price=response.offer_price,
            date=response.date
        )
        mm.add_trade(completed_trade)

    elif response.hf_action == "sell":
        mm_action = "buy"
        trade_price = response.offer_price
        completed_trade = CompletedTrade(
            ticker=response.ticker,
            trade_volume=response.trade_volume,
            trade_price=trade_price,
            mm_action=mm_action,
            ref_price=response.ref_price,
            bid_price=response.bid_price,
            offer_price=response.offer_price,
            date=response.date
        )
        mm.add_trade(completed_trade)

    elif response.hf_action == "refuse":
        pass  # No action needed


# Run the cell below to check the output for market maker quoted_trades. 
#
# ##### In the output below you should see many CompletedTrade objects with their details.

print(mm.completed_trades)

# ##### The cell below is used to grade the work after the event. You do not need to do anything here.

# GRADING CELL

# ### f) Create a graphical output for all the SPX quoted trades.
#
# The graph should be created using the matplotlib library. It should show all the quoted trades completed for the ticker SPX and visualise the *Bid, Offer and Reference Price* against *Date*.
#
# #### Initialise the plot with the <python>fig, axes = plt.subplots() </python> function. 
# #### Populate the lists given, and plot them using <python>axes.plot()</python>.

# Initalises the lists to store all the data
bid_data = []
offer_data = []
quote_dates = []

for trade in mm.completed_trades:  # Iterate through the completed trades to find the SPX trades and store the data.
    if trade.ticker == 'SPX':
        bid_data.append(trade.bid_price)
        offer_data.append(trade.offer_price)
        quote_dates.append(trade.date)


# ##### In the print statements below you should be able to see equal length lists for each list.

print("bid_data:", bid_data)
print("offer_data:", offer_data)
print("quote_dates:", quote_dates)

# The quote_dates, bid_data and offer_data are now assigned to the corresponding list. 
#
# #### Next find the reference prices for SPX as we have gaps in our dates.

ref_data = []
ref_dates = []

last_date = max(quote_dates)

for price in prices:  # Iterate through the quotes to find each SPX ticker and matching price data.
    if price[0] == 'SPX' and price[1] <= last_date:
        ref_dates.append(price[1])
        ref_data.append(price[2])

# ##### In the print statements below you should be able to see equal length lists for each list. The ref_dates should go untill the last quote_dates

print("ref_data:", ref_data)
print("ref_dates:", ref_dates)

# #####  Finally plot each of the axes.

axes = plt.subplot()  # Creates the Axis.

axes.plot(quote_dates, bid_data, label='Bid Price')  # Plot the bid prices.
axes.plot(quote_dates, offer_data, label='Offer Price')  # Plot the offer prices.
axes.plot(ref_dates, ref_data, label='Reference Price')  # Plot the reference prices.

axes.set_xlabel('Date')
axes.set_ylabel('Price')
axes.set_title('SPX Quoted Trades')
axes.legend()
plt.show()


# ##### The cell below is used to grade the work after the event. You do not need to do anything here.

# GRADING CELL

# ![](https://algo-assets.amplifyme.com/quant/citadelchallenge2.png)

# # Quant Simulation Challenge 2 - Skewed Price Making
#
# In this challenge you must work independently to complete several functions which will now skew your prices based on the position of risk at any given moment of time. This will help show you how to optimize the code.
#
# The goal of this challenge is to automate the market-making process, using object-orientated programming to automatically create a bid-offer spread around the reference price. 
#
# You're expected to provide a 2% non-skewed bid and offer for each trade with no risk.
#
# You're expected to provide a 1% non-skewed bid or offer and a 7% skewed bid or offer depending on your risk.
#
# Good luck!

mm = MarketMaker.mm(stocks)

#
# ### a) Using the code learned in challenge 1 apply an algorithm to all price requests and skew based on risk.
#
#
# The functions below have been created in 2 steps to allow you to manage the trade process faster.
#
#
# #### Remember to log any *QuotedTrades* and *CompletedTrades* to your MM object or risk penalties for poor risk management.

# #### Function 1 - `def calculate_spread(price):` 
# This first function has been mostly done for you, just calculate the bid and offer price. For this function, the *balance* is accessed to determine the firm's risk at any given moment. This information is then used to decide if you're Axed Long, Axed Short or Neutral in your position. This is then reflected in your **bid** and **offer** prices.

def calculate_spread(quote):
    request = quote[0]
    ticker = request[0]
    date = request[1]
    trade_volume = request[2]
    ref_price = quote[1]
    volume = mm.current_positions[ticker].position_volume

    if volume > 0:
        # Axed Long: Less attractive bid, more attractive offer
        bid_price = ref_price * (1 - 0.01)
        offer_price = ref_price * (1 - 0.07)
    elif volume < 0:
        # Axed Short: More attractive bid, less attractive offer
        bid_price = ref_price * (1 + 0.07)
        offer_price = ref_price * (1 + 0.01)
    else:
        # Neutral: Standard 2% spread
        bid_price = ref_price * (1 - 0.02)
        offer_price = ref_price * (1 + 0.02)

    # Create a QuotedTrade object and log it
    quoted_trade = QuotedTrade(
        ticker=ticker,
        trade_volume=trade_volume,
        ref_price=ref_price,
        bid_price=bid_price,
        offer_price=offer_price,
        date=date
    )
    mm.add_quoted_trade(quoted_trade)
    return quoted_trade


# #### Function 2 - `def handle_response(trade):` 
# The **QuotedTrade** object is shown using the HF's function, to get the HF's response. You need to handle this response, in order to create your **CompletedTrade** object correctly. Also, log your CompletedTrade object using: `mm.add_trade(CompletedTrade)` .


def handle_response(trade):
    if trade.hf_action == "buy":
        mm_action = "sell"
        trade_price = trade.bid_price
    elif trade.hf_action == "sell":
        mm_action = "buy"
        trade_price = trade.offer_price
    else:
        # If the hedge fund refuses, no trade is executed
        return None

    # Create a CompletedTrade object and log it
    completed_trade = CompletedTrade(
        ticker=trade.ticker,
        trade_volume=trade.trade_volume,
        trade_price=trade_price,
        mm_action=mm_action,
        ref_price=trade.ref_price,
        bid_price=trade.bid_price,
        offer_price=trade.offer_price,
        date=trade.date
    )
    mm.add_trade(completed_trade)
    return completed_trade

# ### Run the cell below to call your functions

for request in price_requests:
    for price in prices:
        if price[0] == request[0] and price[1] == request[1]:
            quote = calculate_spread( (request, price[2]) )
            response = hf.show(quote)
            trade = handle_response(response)

# GRADING CELL

# ### b) Create graphical outputs for all the tickers you quoted_trades
#
# #### Similar to the graph created in Challenge 1 however it should be done for all the different tickers dealt for the HF client.

# Get list of unique tickers from completed trades
tickers = set([trade.ticker for trade in mm.completed_trades])

for ticker in tickers:
    bid_data = []
    offer_data = []
    quote_dates = []
    ref_data = []
    ref_dates = []
    
    # Collect bid, offer, and dates from completed trades
    for trade in mm.completed_trades:
        if trade.ticker == ticker:
            bid_data.append(trade.bid_price)
            offer_data.append(trade.offer_price)
            quote_dates.append(trade.date)
    
    # Collect reference prices up to the last quote date
    last_date = max(quote_dates) if quote_dates else None
    for price in prices:
        if price[0] == ticker and (last_date is None or price[1] <= last_date):
            ref_dates.append(price[1])
            ref_data.append(price[2])
    
    # Plotting
    plt.figure(figsize=(10,6))
    axes = plt.subplot()
    axes.plot(quote_dates, bid_data, label='Bid Price')
    axes.plot(quote_dates, offer_data, label='Offer Price')
    axes.plot(ref_dates, ref_data, label='Reference Price')
    axes.set_xlabel('Date')
    axes.set_ylabel('Price')
    axes.set_title(f'{ticker} Quoted Trades')
    axes.legend()
    plt.show()


# ![](https://algo-assets.amplifyme.com/quant/citadelchallenge3.png)

# # Quant Simulation Challenge 3 - Hedging with an ETF
#
#
# In this challenge you must work independently to complete an implementation which is able to enter positions using the ETF to hedge the risk at any given moment of time. The implementation should be based on the code from the previous challenges but you have freedom to improve and go further.
#
# The goal of this challenge is to automate the market-making process, using object-orientated programming to automatically create a bid-offer spread around the reference price and place hedging trades. 
#
# You're expected to provide a 2% non-skewed bid and offer for each trade with no risk.
#
# You're expected to provide a 1% non-skewed bid or offer and a 7% skewed bid or offer depending on your risk.
#
# You're expected to enter a hedge of nominal value but are free to explore alternative ways if you wish.
#
# For all price requests we calculcate a skew based on risk. Using the MM function, we access the current_positions to determine the firm's risk at any given moment. We then use this information to decide if we're Axed Long, Axed Short or Neutral in our position.
#
# This will then be reflected in our Bid and Offer prices. We then add a hedge that is determined by the correlation of the risk taken on against the MSCI-ETF to then execute the correct hedge for each stock in the exchange using the ExchangeTrade object.
#
# Once we have determined the ratio of MSCI ETF to equity position held by the market maker, we create an ExchangeTrade object to interact with the exchange and execute the ETF trade based on the equity position held.
#
#
# Good luck!
#
#
# # How we calculate the MSCI ETF
#
# <hr>
#
# It may be useful for you to know how the MSCI ETF is calculated. The MSCI ETF is an exchange traded product that is made up of 4 component equity assets: ESTOXX, NKY, SPX and UKX.
#
# The MSCI ETF is an equally dollar weighted index rebased at t0 with no further rebalancing. 
#
# The daily value of the ETF is always calculated by taking the average of the 4 rebased components. 
#
# For example, on t0, - each of the 4 stock prices are rebased to \\$100 and therefore the ETF's value on t0 = $100.
#
# ![](https://algo-assets.amplifyme.com/quant/MSCI-t0.png)
#
# At t1 the value of each rebased stock changes from its starting value of 100 by the percentage value that the actual stock price changed between time t0 and time t1.
#
# FAs a simple example, if ESTOXX's share price rose by 1% between time to and time t1, then the value of the rebased ESTOXX component moves from \\$100 to \\$101.
#
# If NKY's share price dropped by 0.5% between time to and time t1 then the value of the rebased NKY component moves from \\$100 to \\$99.5 and so on.
#
# The MSCI ETF at t1 is simply the average of the 4 rebased component prices at t1. Below is an image explaining how the value of the MSCI ETF at t1 is calculated:
#
# ![](https://algo-assets.amplifyme.com/quant/MSCI-t1.png)
#
# <hr> 

#
# ### Relevant Market Maker Functions
# - mm.current_positions
# - mm.add_quoted_trade
# - mm.add_trade
#
# NOTE Any QuotedTrades and CompletedTrades are to be explicitly logged to the MM object to avoid penalties for poor risk management.
#
#
# ### Hedge Fund Object
# The Hedge Fund Object is used to Show quoted_trades and receive a response.
#
# Using the quoted_trades list interact with the HF object to receive a "Buy, Sell, Refuse" response from the HF and store these HfResponse objects in an list called hf_responses.
#
# ###### Sends the quoted_trade object to the hedge fund to make a decision for a trade.
# hf.show(QuotedTrade)
#
# ##### Parameters:
# - QuotedTrade: Custom Object
#
# ##### Returns:
# - HfResponse( ticker: String, trade_volume: Integer, trade_price: Float, hf_action: String, ref_price: Float, bid_price: Float, offer_price: Float, date: Integer )
#
# ### HfResponse object
# - ticker: String
# - trade_volume: Integer
# - trade_price: Float
# - hf_action: String
# - ref_price: Float
# - bid_price: Float
# - offer_price: Float
# - date: Integer
#
#
# ### Relevant functions used for this implementation
# ##### Execute a MSCI trade
# Exchange.execute(ExchangeTrade)
#
# ##### Parameters:
# - ExchangeTrade: Custom Object
#
# ##### Returns:
# - ExecutedTrade( ticker: String, trade_volume: Integer, ref_price: Float, trade_price: Float, action: String, date: Integer )
#
#
# ##### Update the Market Makers current ETF position.
# mm.update_ETF_position(ExecutedTrade)
#
# ##### Parameters:
# - ExecutedTrade: Custom Object from exchange return
#
# ##### Returns:
# - String: Indicating a successfully added trade or failed added trade.
#
#
# Log the response for Exchange.execute(ExchangeTrade) with the mm.update_ETF_position(ExecutedTrade)

# ### a) Using your code from challenge 2, add a MSCI ETF hedge using the nominal values.
#
# When a completed trade has been received from the HF object, you're now to hedge the firm's risk using the MSCI ETF. 
#
# Determine the volume and current reference price to find the nominal value for the position of risk the firm now holds; this value should then be used to hedge using the MSCI ETF.
#
# Once you have determined how much of the MSCI ETF should be purchased, you need to create an ExchangeTrade object to interact with the exchange and complete the trade. 
#
# You should then log this trade in the *updateETFPosition* function on the MM object.

# ### ExchangeTrade object
# To get started you need to create an ExchangeTrade object This will be used to create a trade that will be executed using the exchange. As this is similar to the two you have done before we have drafted the code to run for you below which contains the following attributes:
#
# - ticker: String
# - trade_volume: Integer
# - ref_price: Float
# - action: String
# - date: Integer

class ExchangeTrade:
    def __init__(self, ticker, trade_volume, ref_price, action, date):
        self.ticker = ticker
        self.trade_volume = trade_volume
        self.ref_price = ref_price
        self.action = action
        self.date = date

# Hint - For previous challenges, the prices series was stored in a list. However, from this Challenge onwards, prices series will be stored in a Pandas Dataframe.

mm = MarketMaker.mm(stocks)
prices = Data.get_price_series('PricestoFeedserverHedge2011', True)
price_requests = Data.get_price_requests('PriceRequeststoFeedserverExtended2011')

# Main loop to process price requests and hedge positions
for request in price_requests:
    ticker = request[0]
    date = request[1]
    trade_volume = request[2]

    # Ensure date is an integer and matches the index in prices
    date = int(date)

    # Check if the date exists in the prices DataFrame
    if date not in prices.index:
        continue  # Skip if date not in prices

    # Check if ticker exists in the prices DataFrame columns
    if ticker not in prices.columns:
        continue  # Skip if ticker not in prices

    # Get the reference price from the prices DataFrame
    ref_price = prices.at[date, ticker]

    # Create a quote and process it
    quote = (request, ref_price)
    quoted_trade = calculate_spread(quote)
    response = hf.show(quoted_trade)
    completed_trade = handle_response(response)

    # If a trade was executed, hedge the position using the MSCI ETF
    if completed_trade:
        # Calculate the nominal value of the position
        position_volume = mm.current_positions[completed_trade.ticker].position_volume
        nominal_value = position_volume * ref_price

        # Get the MSCI ETF reference price on the same date
        if 'MSCI-ETF' not in prices.columns:
            continue  # Skip if MSCI-ETF not in prices

        etf_ref_price = prices.at[date, 'MSCI-ETF']

        # Calculate the ETF trade volume needed to hedge
        etf_trade_volume = -nominal_value / etf_ref_price
        etf_trade_volume = int(round(etf_trade_volume))

        # Determine the action based on the trade volume
        if etf_trade_volume > 0:
            action = 'buy'
        elif etf_trade_volume < 0:
            action = 'sell'
            etf_trade_volume = abs(etf_trade_volume)
        else:
            continue  # No hedge needed if trade volume is zero

        # Create an ExchangeTrade object and execute it
        exchange_trade = ExchangeTrade(
            ticker='MSCI-ETF',
            trade_volume=etf_trade_volume,
            ref_price=etf_ref_price,
            action=action,
            date=date
        )
        executed_trade = Exchange.execute(exchange_trade)

        # Log the executed trade to update the ETF position
        mm.update_ETF_position(executed_trade)


# #### Below you will find some space to enter any comments and thoughts you may have about the challenge so far.

# i'll say it was a very fun intro to programming in quant finance. i look forward to doing more of it

# GRADING CELL

# ### b) Create graphical output of the combined nominal risk value over time
#
# This will be the nominal value for all risk at any given time from the position you have open. This data will be stored in the balance.

import pandas as pd
import matplotlib.pyplot as plt

# Initialize a list to store the nominal risk value over time
risk_data = {'date': [], 'nominal_value': []}

# Get a sorted list of all unique dates from completed trades and ETF positions
dates = set()

# Collect dates from completed trades
for trade in mm.completed_trades:
    dates.add(trade.date)

# Collect dates from ETF positions
for trade in mm.ETF_positions:
    dates.add(trade.date)

# Sort the dates
dates = sorted(dates)

# Initialize dictionaries to track positions over time
equity_positions = {}  # {ticker: position_volume}
etf_position_volume = 0  # Total ETF position volume

# Initialize variables to store the cumulative positions
cumulative_positions = []

# Iterate over each date to calculate the nominal value
for date in dates:
    # Update equity positions based on trades on the current date
    for trade in mm.completed_trades:
        if trade.date == date:
            ticker = trade.ticker
            volume = trade.trade_volume
            if trade.mm_action == 'buy':
                equity_positions[ticker] = equity_positions.get(ticker, 0) + volume
            elif trade.mm_action == 'sell':
                equity_positions[ticker] = equity_positions.get(ticker, 0) - volume

    # Update ETF position based on trades on the current date
    for etf_trade in mm.ETF_positions:
        if etf_trade.date == date:
            if etf_trade.action == 'buy':
                etf_position_volume += etf_trade.trade_volume
            elif etf_trade.action == 'sell':
                etf_position_volume -= etf_trade.trade_volume

    # Calculate total nominal value for the current date
    total_nominal_value = 0

    # Calculate nominal value for equity positions
    for ticker, position_volume in equity_positions.items():
        # Get the reference price for the ticker on the current date
        if date in prices.index and ticker in prices.columns:
            price = prices.at[date, ticker]
            total_nominal_value += position_volume * price

    # Calculate nominal value for ETF position
    # Get the ETF price at the current date
    if date in prices.index and 'MSCI-ETF' in prices.columns:
        etf_price = prices.at[date, 'MSCI-ETF']
        total_nominal_value += etf_position_volume * etf_price

    # Append the date and total nominal value to the risk data
    risk_data['date'].append(date)
    risk_data['nominal_value'].append(total_nominal_value)

# Convert the risk data to a DataFrame
risk_df = pd.DataFrame(risk_data)

# Plot the nominal risk value over time
plt.figure(figsize=(12, 6))
plt.plot(risk_df['date'], risk_df['nominal_value'], label='Nominal Risk Value')
plt.xlabel('Date')
plt.ylabel('Nominal Risk Value')
plt.title('Combined Nominal Risk Value Over Time')
plt.legend()
plt.grid(True)
plt.show()




