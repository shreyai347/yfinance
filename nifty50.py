import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Stock Dashboard")
st.title("📊 Stock Dashboard using yFinance + Streamlit")

# List of NIFTY 50 companies and their ticker symbols
nifty_50_stocks = {
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "Bharat Electronics": "BEL.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Cipla": "CIPLA.NS",
    "Coal India": "COALINDIA.NS",
    "Dr. Reddy's Laboratories": "DRREDDY.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Ethernal": "ZOMATO.NS",
    "Grasim Industries": "GRASIM.NS",
    "HCL Technologies": "HCLTECH.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "HDFC Life Insurance": "HDFCLIFE.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Hindalco Industries": "HINDALCO.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Infosys": "INFY.NS",
    "ITC": "ITC.NS",
    "Jio Financial Services": "JIOFIN.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Larsen & Toubro": "LT.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Nestle India": "NESTLEIND.NS",
    "NTPC": "NTPC.NS",
    "Oil and Natural Gas Corporation": "ONGC.NS",
    "Power Grid Corporation": "POWERGRID.NS",
    "Reliance Industries": "RELIANCE.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "State Bank of India": "SBIN.NS",
    "Sun Pharmaceutical": "SUNPHARMA.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Tata Consumer Products": "TATACONSUM.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Tech Mahindra": "TECHM.NS",
    "Titan Company": "TITAN.NS",
    "Trent": "TRENT.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Wipro": "WIPRO.NS"
}

# Stock input with suggestions
st.header("Search Stock")
selected_stock = st.selectbox(
    "Select a NIFTY 50 stock:",
    options=[""] + list(nifty_50_stocks.keys())
)

ticker_input = nifty_50_stocks.get(selected_stock)

if ticker_input:
    stock = yf.Ticker(ticker_input)

    # Basic Info
    st.header("📘 Company Info")
    info = stock.info
    if "shortName" in info:
        st.subheader(f"{info['shortName']} ({info['symbol']})")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}  \n"
                    f"**Industry:** {info.get('industry', 'N/A')}  \n"
                    f"**Exchange:** {info.get('exchange', 'N/A')}  \n"
                    f"**Market Cap:** {info.get('marketCap', 'N/A')}  \n"
                    f"**Beta:** {info.get('beta', 'N/A')}  \n"
                    f"**P/E Ratio (Trailing):** {info.get('trailingPE', 'N/A')}  \n"
                    f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}  \n"
                    f"[Website]({info.get('website', '#')})")
    else:
        st.error("Invalid ticker or data unavailable.")

    # Price Overview
    st.subheader("💵 Price Overview")
    price_col1, price_col2, price_col3, price_col4 = st.columns(4)
    with price_col1:
        st.metric(label="Previous Close", value=info.get("previousClose", "N/A"))
    with price_col2:
        st.metric(label="Open", value=info.get("open", "N/A"))
    with price_col3:
        st.metric(label="Day High", value=info.get("dayHigh", "N/A"))
    with price_col4:
        st.metric(label="Day Low", value=info.get("dayLow", "N/A"))

    # Day Range and 52-Week Range
    st.subheader("📏 Ranges")
    range_col1, range_col2 = st.columns(2)
    with range_col1:
        day_low = info.get("dayLow", None)
        day_high = info.get("dayHigh", None)
        if day_low and day_high:
            st.write(f"**Day Range:** {day_low} – {day_high}")
        else:
            st.write("**Day Range:** N/A")
    with range_col2:
        low_52 = info.get("fiftyTwoWeekLow", None)
        high_52 = info.get("fiftyTwoWeekHigh", None)
        if low_52 and high_52:
            st.write(f"**52-Week Range:** {low_52} – {high_52}")
        else:
            st.write("**52-Week Range:** N/A")

    # Performance Overview
    st.subheader("📈 Performance Overview")
    performance_col1, performance_col2 = st.columns(2)
    current_price = stock.history(period="1d")['Close'][-1] if not stock.history(period="1d").empty else None

    with performance_col1:
        if current_price and info.get("previousClose"):
            prev_close = info["previousClose"]
            change = current_price - prev_close
            percent = (change / prev_close) * 100
            st.metric("Today’s Change", f"{change:.2f}", f"{percent:.2f}%", delta_color="normal" if change < 0 else "inverse")

    with performance_col2:
        if current_price and info.get("fiftyTwoWeekLow"):
            low_52 = info["fiftyTwoWeekLow"]
            change_52 = current_price - low_52
            percent_52 = (change_52 / low_52) * 100
            st.metric("52W Performance", f"{change_52:.2f}", f"{percent_52:.2f}%", delta_color="normal" if change_52 < 0 else "inverse")

    # Historical Chart
    st.header("📈 Historical Price Chart")
    hist = stock.history(period="1mo", interval="1d")
    if not hist.empty:
        st.line_chart(hist['Close'])
    else:
        st.warning("No historical data available.")

    # News
    st.header("📰 Latest News")
    news_items = stock.news
    if news_items:
        for article in news_items[:5]:
            st.markdown(f"**{article.get('title', 'No Title')}** - *{article.get('publisher', 'No Publisher')}*  \n")

    else:
        st.info("No recent news available.")

    # Financial Statements
    st.header("📊 Financial Statements")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Income Statement")
        st.dataframe(stock.financials)
    with col2:
        st.subheader("Balance Sheet")
        st.dataframe(stock.balance_sheet)
    with col3:
        st.subheader("Cash Flow")
        st.dataframe(stock.cashflow)

    # Dividends & Splits
    st.header("💰 Dividends & 🔀 Stock Splits")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dividends")
        st.dataframe(stock.dividends.tail(10))
    with col2:
        st.subheader("Stock Splits")
        st.dataframe(stock.splits.tail(10))

    # Analyst Recommendations
    st.header("📋 Analyst Recommendations")
    st.dataframe(stock.recommendations.tail(10))

    # Earnings
    st.header("📆 Earnings Data")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Yearly Earnings")
        st.dataframe(stock.earnings)
    with col2:
        st.subheader("Quarterly Earnings")
        st.dataframe(stock.quarterly_earnings)

# Button to generate CSV for NIFTY 50 stocks
if st.button("Generate NIFTY 50 CSV"):
    data = []
    for name, symbol in nifty_50_stocks.items():
        stock = yf.Ticker(symbol)
        info = stock.info
        row = {
            "Name": name,
            "Symbol": symbol,
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Previous Close": info.get("previousClose", "N/A"),
            "Open": info.get("open", "N/A"),
            "Day High": info.get("dayHigh", "N/A"),
            "Day Low": info.get("dayLow", "N/A"),
            "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        }
        data.append(row)

    # Create a DataFrame and save it as a CSV file
    df = pd.DataFrame(data)
    csv_file = "nifty_50_stocks.csv"
    df.to_csv(csv_file, index=False)
    st.success(f"CSV file '{csv_file}' has been generated!")
    st.dataframe(df)

# Button to generate and display sorted NIFTY 50 table
if st.button("Generate and Sort NIFTY 50 Table by Sector"):
    data = []
    for name, symbol in nifty_50_stocks.items():
        stock = yf.Ticker(symbol)
        info = stock.info
        row = {
            "Name": name,
            "Symbol": symbol,
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Previous Close": info.get("previousClose", "N/A"),
            "Open": info.get("open", "N/A"),
            "Day High": info.get("dayHigh", "N/A"),
            "Day Low": info.get("dayLow", "N/A"),
            "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        }
        data.append(row)

    # Create a DataFrame, sort by Sector, and display it
    df = pd.DataFrame(data)
    sorted_df = df.sort_values(by="Sector")
    st.header("📋 NIFTY 50 Table Sorted by Sector")
    st.dataframe(sorted_df)

    # Optionally save the sorted table as a CSV file
    csv_file = "nifty_50_sorted_by_sector.csv"
    sorted_df.to_csv(csv_file, index=False)
    st.success(f"Sorted CSV file '{csv_file}' has been generated!")
