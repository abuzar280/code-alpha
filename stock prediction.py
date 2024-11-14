from pyngrok import ngrok, conf

# Set the correct path for your ngrok executable
conf.get_default().ngrok_path = "C:\\Desktop\\files\\Documents\\MYDOC\\ngrok-v3-stable-windows-amd64\\ngrok.exe"

# Set your ngrok authtoken
NGROK_AUTHTOKEN = "2hzSdjFg50QLQ4Cr4lhF9KgJqPQ_5wU28ibM3rP2SBut3tkaE"  # Replace with your actual authtoken
ngrok.set_auth_token(NGROK_AUTHTOKEN)

# Check if a tunnel on port 8501 already exists
tunnels = ngrok.get_tunnels()
tunnel_on_port_8501 = next((t for t in tunnels if t.config["addr"] == "8501"), None)

if tunnel_on_port_8501:
    public_url = tunnel_on_port_8501.public_url
    print("Reusing existing ngrok tunnel on port 8501:", public_url)
else:
    # Terminate any existing tunnels that are not on port 8501
    for tunnel in tunnels:
        if tunnel.config["addr"] != "8501":
            ngrok.disconnect(tunnel.public_url)
    
    # Create a new tunnel for port 8501
    public_url = ngrok.connect(addr="8501").public_url
    print("Streamlit URL:", public_url)

import streamlit as st
import sqlite3
import requests
import pandas as pd

# Set up the Alpha Vantage API key
API_KEY = 'XC0F0MHOGYGZP5SC'  # Replace with your Alpha Vantage API key

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to get the current stock price from Alpha Vantage
def get_stock_price(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
    response = requests.get(url).json()
    try:
        price = float(list(response['Time Series (1min)'].values())[0]['1. open'])
        return price
    except KeyError:
        return None

# Initialize the database
def initialize_database():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add stock to the portfolio
def add_stock(symbol, quantity):
    price = get_stock_price(symbol)
    if price:
        conn = get_db_connection()
        conn.execute('INSERT INTO portfolio (symbol, quantity, purchase_price) VALUES (?, ?, ?)',
                     (symbol.upper(), quantity, price))
        conn.commit()
        conn.close()
        st.success(f"Added {symbol} with quantity {quantity} at purchase price ${price:.2f}")
    else:
        st.error("Failed to retrieve stock price. Please check the symbol and try again.")

# Function to delete stock from the portfolio
def delete_stock(stock_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM portfolio WHERE id = ?', (stock_id,))
    conn.commit()
    conn.close()
    st.success("Stock removed from portfolio.")

# Function to load portfolio data
def load_portfolio():
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM portfolio').fetchall()
    conn.close()
    return stocks

# Function to calculate gain/loss
def calculate_portfolio():
    portfolio = []
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM portfolio').fetchall()
    conn.close()

    for stock in stocks:
        current_price = get_stock_price(stock['symbol'])
        if current_price:
            gain_loss = (current_price - stock['purchase_price']) * stock['quantity']
            portfolio.append({
                'id': stock['id'],
                'symbol': stock['symbol'],
                'quantity': stock['quantity'],
                'purchase_price': stock['purchase_price'],
                'current_price': current_price,
                'gain_loss': gain_loss
            })
    return pd.DataFrame(portfolio)

# Streamlit interface
st.title("Stock Portfolio Tracker")

# Initialize database
initialize_database()

# Section to add a new stock
st.header("Add a Stock")
symbol = st.text_input("Stock Symbol (e.g., AAPL)")
quantity = st.number_input("Quantity", min_value=1, step=1)
if st.button("Add Stock"):
    add_stock(symbol, quantity)

# Display portfolio
st.header("Your Portfolio")
stocks = load_portfolio()
if stocks:
    df = calculate_portfolio()
    if not df.empty:
        st.dataframe(df[['symbol', 'quantity', 'purchase_price', 'current_price', 'gain_loss']])
else:
    st.write("No stocks in your portfolio.")

# Section to delete a stock
st.header("Remove a Stock")
stock_id_to_delete = st.number_input("Stock ID to Remove", min_value=1, step=1)
if st.button("Remove Stock"):
    delete_stock(stock_id_to_delete)
