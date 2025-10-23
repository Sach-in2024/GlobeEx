import streamlit as st
import requests
from langchain_groq import ChatGroq

# ----------------- CONFIG -----------------
st.set_page_config(page_title="AI Currency Converter 💱", layout="centered")

# ----------------- CHATGROQ SETUP -----------------
chat_client = ChatGroq(
    api_key="GROQ_API_KEY",  # Replace with your key
    model="llama-3.1-3b-instant"
)

# ----------------- STATIC CURRENCY LIST -----------------
currency_list = [
    "USD","EUR","GBP","INR","JPY","AUD","CAD","CHF","CNY","HKD","NZD","SEK","KRW","SGD","NOK",
    "MXN","BRL","ZAR","TRY","RUB","MYR","IDR","THB","PHP","DKK","PLN","HUF","CZK","ILS","CLP",
    "PKR","EGP","SAR","NGN","AED","COP","TWD","VND","ARS","BDT","KWD","QAR","RON","BGN","HRK",
    "ISK","LKR","KZT","OMR","MAD","DZD","UYU","PEN","JMD","BHD","ALL","AZN","BAM","BYN","CUP",
    "DOP","ETB","GEL","GHS","GTQ","HNL","IQD","JOD","KES","LBP","MKD","MUR","NAD","NPR","PAB",
    "PGK","RSD","SCR","SHP","TND","TZS","UGX","UZS","XAF","XCD","XOF","XPF"
]

# ----------------- STREAMLIT UI -----------------
st.markdown("<h1 style='text-align: center;'>🌍 AI Currency Converter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:gray;'>Select currencies from the lists and convert in real-time</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox("From Currency", currency_list, index=0)
with col2:
    to_currency = st.selectbox("To Currency", currency_list, index=3)

amount = st.number_input("Enter Amount", min_value=0.0, format="%.2f")
submit_btn = st.button("🔄 Convert")

# ----------------- CONVERSION FUNCTION USING ExchangeRate-API -----------------
API_KEY = "EXCHANGE_RATE_KEY"  # Your API key
def convert_currency(amount, from_curr, to_curr):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_curr}/{to_curr}"
        response = requests.get(url)
        data = response.json()
        if data['result'] == 'success':
            rate = data['conversion_rate']
            converted_amount = amount * rate
            return converted_amount, rate
        else:
            return None, None
    except:
        return None, None

# ----------------- PROCESS -----------------
if submit_btn:
    converted, rate = convert_currency(amount, from_currency, to_currency)
    if converted:
        st.success(f"💰 {amount:.2f} {from_currency} = {converted:.2f} {to_currency}")
        st.caption(f"1 {from_currency} = {rate:.4f} {to_currency}")
    else:
        st.error("❌ Conversion failed. Check your internet connection or currency selection.")

