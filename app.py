import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objects as go

# -------- FUNCTIONS -------- #

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period="6mo")
    return df

def calculate_indicators(df):
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    return df

def add_rsi(df):
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    return df

def support_resistance(df):
    support = df['Low'].rolling(window=10).min().iloc[-1]
    resistance = df['High'].rolling(window=10).max().iloc[-1]
    return round(support, 2), round(resistance, 2)

def capital_strategy(price):
    capital = 25000
    qty = int(capital / price)

    return {
        "Capital": capital,
        "Buy Price": round(price, 2),
        "Quantity": qty,
        "Target (5%)": round(price * 1.05, 2),
        "Stop Loss (3%)": round(price * 0.97, 2)
    }

def generate_signal(df):
    latest = df.iloc[-1]

    if latest['MA20'] > latest['MA50'] and latest['RSI'] < 70:
        return "STRONG BUY 🚀"
    elif latest['MA20'] < latest['MA50'] and latest['RSI'] > 30:
        return "STRONG SELL 🔻"
    else:
        return "HOLD ⚠️"

# -------- UI -------- #

st.title("📈 Financial AI Assistant")

ticker = st.text_input("Enter Stock Symbol (e.g., TCS.NS)", "TCS.NS")

# -------- MAIN -------- #

if ticker:
    try:
        df = get_stock_data(ticker)

        if df.empty:
            st.error("Invalid stock ❌")
        else:
            df = calculate_indicators(df)
            df = add_rsi(df)

            st.subheader("📊 Chart")
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )])
            st.plotly_chart(fig)

            support, resistance = support_resistance(df)

            col1, col2 = st.columns(2)
            with col1:
                st.success(f"Support: {support}")
            with col2:
                st.error(f"Resistance: {resistance}")

            signal = generate_signal(df)
            st.write("### 🧠 Signal:", signal)

            latest_price = df['Close'].iloc[-1]
            strategy = capital_strategy(latest_price)

            st.write("### 💰 Strategy")
            st.json(strategy)

            st.subheader("📉 RSI")
            st.line_chart(df['RSI'])

    except Exception as e:
        st.error(f"Error: {e}")
