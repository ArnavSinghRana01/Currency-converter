import streamlit as st
from decouple import config
import requests
from datetime import datetime

# Load API key from .env file
fixer_api_key = config('FIXER_API_KEY')

# Set page configuration, including title and icon
st.set_page_config(
    page_title="Currency Converter",
    page_icon="currency-exchange"
)

# Hide the hamburger menu
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        .css-1v3fvcr {background-color: #f0f0f0;} /* Set background color for main content */
    </style>
""", unsafe_allow_html=True)

# Display the main title with improved styling
st.markdown(
    "<h1 style='text-align: center; color: #1E90FF;'>Currency Converter</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# Fetch the list of currencies from the Fixer API
currency_url = f'http://data.fixer.io/api/symbols?access_key={fixer_api_key}'
currency_response = requests.get(currency_url)

# Check if the API request was successful
if currency_response.status_code == 200:
    currency_data = currency_response.json()

    # Extract currency symbols from the API response
    currency_symbols = currency_data['symbols']
    all_currencies = list(currency_symbols.keys())

    # Create a three-column layout with improved styling
    col1, col2, col3 = st.columns(3)

    # Sidebar for input options with improved styling
    with col1:
        amount = st.number_input("Enter Amount", min_value=0.01, step=0.01, value=1.0, format="%.2f", key="amount_input")

    with col2:
        currency1 = st.selectbox('Select base currency for conversion', all_currencies)

    with col3:
        currency2 = st.selectbox('Select target currency to convert to', all_currencies)

    # Main content area with improved styling
    url = f'http://data.fixer.io/api/latest?access_key={fixer_api_key}'

    # Fetch exchange rates
    response = requests.get(url)

    # Check if the API request for exchange rates was successful
    if response.status_code == 200:
        data = response.json()

        # Check if 'rates' key is present in the response
        if 'rates' in data:
            exchange_rates = data['rates']

            # Perform currency conversion
            if currency2 in exchange_rates:
                converted_amount = amount * exchange_rates[currency2]
                st.success(f"Converted Amount ({currency2}): {converted_amount:.2f}")
                st.info(f"Date of Exchange Rates: {datetime.utcfromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')} (UTC)")

            else:
                st.error(f"Error: Exchange rate for {currency2} not available.")
        else:
            st.error("Error: 'rates' key not found in the API response.")
    else:
        st.error(f"Error fetching exchange rates. Status code: {response.status_code}. Please check your API key or try again later.")

else:
    st.error(f"Error fetching currency symbols. Status code: {currency_response.status_code}. Please check your API key or try again later.")
