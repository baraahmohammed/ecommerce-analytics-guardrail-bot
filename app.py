import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="E-commerce Analytics Bot", page_icon="🤖", layout="centered")

# --- 1. Data Ingestion Layer ---
@st.cache_data # Cache data to optimize performance and prevent reloading on every rerun
def load_data():
    try:
        # Load the targeted e-commerce dataset
        return pd.read_csv("DatasetSheet1.csv")
    except FileNotFoundError:
        return None

df = load_data()

# --- 2. Process Layer (Analytical Logic Core) ---
def get_total_sales():
    """Calculates and formats the cumulative store revenue."""
    total = df['TotalPrice'].sum()
    return f"The total store revenue to date is ${total:,.2f}."

def get_order_status_report():
    """Generates a summary report of all current order statuses."""
    status_counts = df['OrderStatus'].value_counts()
    report = "Current Order Status Summary:\n"
    for status, count in status_counts.items():
        report += f" • {status}: {count} orders\n"
    return report.strip()

def get_top_marketing_channel():
    """Identifies the referral source driving the highest gross revenue."""
    top_channel = df.groupby('ReferralSource')['TotalPrice'].sum().idxmax()
    return f"The highest revenue-generating channel is: {top_channel}."

def show_help_menu():
    """Returns available deterministic commands for the rule-based engine."""
    return "How can I assist you today? You can ask me about: 'sales', 'status', 'marketing', or type a specific product name like 'Monitor'."

# --- 3. Knowledge Base Mapping ---
# Using a Hash Map (Dictionary) to achieve O(1) algorithmic complexity,
# avoiding unstable linear complexity patterns (If-Elif Ladders).
analytics_rules = {
    "sales": get_total_sales,
    "status": get_order_status_report,
    "marketing": get_top_marketing_channel,
    "help": show_help_menu
}

# --- 4. Presentation Layer (Streamlit UI Design) ---
st.title("🤖 E-commerce Analytics Guardrail Bot")
st.caption("A Production-Grade Deterministic Bot Powered by DecodeLabs Logic kit")

if df is None:
    st.error("Error: 'DatasetSheet1.csv' not found. Please check the path inside 'Project no1/' folder.")
else:
    # Initialize session state for persistent chat history mapping
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to the E-commerce Analytics Guardrail Bot! Type 'help' to see available analytical commands."}
        ]

    # Render structural logs of historical chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle explicit user queries from the modern chat interface
    if user_query := st.chat_input("Ask about sales, status, marketing or a product..."):
        
        # Display user runtime prompt
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Data Sanitization & Normalization (Case insensitivity & whitespace stripping)
        clean_input = user_query.lower().strip()

        # Decision-Making Processing Layer
        if clean_input == 'exit':
            bot_response = "To exit or reset the session, simply refresh the web page. Goodbye!"
        else:
            # Deterministic dictionary lookup phase
            action = analytics_rules.get(clean_input)
            
            if action:
                bot_response = action()
            else:
                # Flexible continuous mapping verification for explicit product items
                available_products = df['Product'].str.lower().unique()
                if clean_input in available_products:
                    product_df = df[df['Product'].str.lower() == clean_input]
                    product_revenue = product_df['TotalPrice'].sum()
                    product_units = product_df['Quantity'].sum()
                    bot_response = f"[{user_query.capitalize()}] has generated **${product_revenue:,.2f}** across **{product_units}** units sold."
                else:
                    # Deterministic Fallback mechanism for unexpected queries
                    bot_response = "Command not recognized. Type 'help' to see what I can calculate from the dataset."

        # Display and record structural bot output
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})