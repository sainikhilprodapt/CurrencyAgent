import streamlit as st
from agent import create_currency_agent, get_currency_info

# Page configuration
st.set_page_config(
    page_title="Currency Converter & News",
    page_icon="💱",
    layout="wide"
)

# Initialize session state for caching agent responses
if 'conversion_result' not in st.session_state:
    st.session_state.conversion_result = None

# Initialize agent if not already in session state
if 'agent_executor' not in st.session_state:
    st.session_state.agent_executor = create_currency_agent()

# App title and description
st.title("💱 Currency Converter & News")
st.markdown("Get the latest exchange rates and currency news in one place!")

# Create two columns for currency selection
col1, col2 = st.columns(2)

# Currency options
currency_options = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "INR": "Indian Rupee",
    "SGD": "Singapore Dollar",
    "NZD": "New Zealand Dollar",
    "HKD": "Hong Kong Dollar",
    "KRW": "South Korean Won",
    "MXN": "Mexican Peso",
    "BRL": "Brazilian Real"
}

# Create selectboxes for currency selection
with col1:
    from_currency = st.selectbox(
        "From Currency",
        options=list(currency_options.keys()),
        format_func=lambda x: f"{x} - {currency_options[x]}",
        index=0  # Default to USD
    )

with col2:
    to_currency = st.selectbox(
        "To Currency",
        options=list(currency_options.keys()),
        format_func=lambda x: f"{x} - {currency_options[x]}",
        index=8  # Default to INR
    )

# Add a button to swap currencies
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("↔️ Swap Currencies"):
        # Store current selections
        temp_from = from_currency
        temp_to = to_currency
        
        # Get the indices
        from_index = list(currency_options.keys()).index(temp_from)
        to_index = list(currency_options.keys()).index(temp_to)
        
        # Update session state to force re-render with swapped selections
        st.session_state['from_currency_index'] = to_index
        st.session_state['to_currency_index'] = from_index
        st.rerun()

# Convert button
if st.button("🔍 Get Rate & News", type="primary"):
    with st.spinner("Fetching latest rates and news..."):
        try:
            # Get currency information using the agent
            result = get_currency_info(
                st.session_state.agent_executor, 
                from_currency, 
                to_currency
            )
            st.session_state.conversion_result = result
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display result if available
if st.session_state.conversion_result:
    st.markdown("## Results")
    
    # Create a styled container for the results
    with st.container():
        st.markdown(st.session_state.conversion_result, unsafe_allow_html=True)
