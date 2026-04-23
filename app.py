import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta
import plotly.graph_objects as go
ticker = st.text_input("Enter Stock Symbol (e.g., TCS.NS)", "TCS.NS")

if ticker:
    try:
        df = get_stock_data(ticker)

        if df.empty:
            st.error("Invalid stock symbol ❌")
        else:
            df = calculate_indicators(df)
            df = add_rsi(df)

            # Chart
            st.subheader("📊 Candlestick Chart")
            import plotly.graph_objects as go
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )])
            st.plotly_chart(fig)

            # Support Resistance
            support, resistance = support_resistance(df)

            col1, col2 = st.columns(2)
            with col1:
                st.success(f"Support: {support}")
            with col2:
                st.error(f"Resistance: {resistance}")

            # Signal
            signal = generate_signal(df)
            st.write("### 🧠 AI Signal:", signal)

            # Strategy
            latest_price = df['Close'].iloc[-1]
            strategy = capital_strategy(latest_price)

            st.write("### 💰 ₹25K Strategy")
            st.json(strategy)

            # RSI
            st.subheader("📉 RSI")
            st.line_chart(df['RSI'])

    except Exception as e:
        st.error(f"Error: {e}") 
