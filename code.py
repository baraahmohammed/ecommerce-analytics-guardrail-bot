import pandas as pd
try:
    df = pd.read_csv("DatasetSheet1.csv")
except FileNotFoundError:
    print("Error: Data file not found.")
    exit()

def get_total_sales():
    total = df['TotalPrice'].sum()
    return f"The total store revenue to date is ${total:,.2f}."

def get_order_status_report():
    status_counts = df['OrderStatus'].value_counts()
    report = "Current Order Status Summary:\n"
    for status, count in status_counts.items():
        report += f" - {status}: {count} orders\n"
    return report.strip()

def get_top_marketing_channel():
    top_channel = df.groupby('ReferralSource')['TotalPrice'].sum().idxmax()
    return f"The highest revenue-generating channel is: {top_channel}."

def show_help_menu():
    return "How can I assist you today? You can ask about: 'sales', 'status', 'marketing', or type a specific product name like 'Monitor'."


analytics_rules = {
    "sales": get_total_sales,
    "status": get_order_status_report,
    "marketing": get_top_marketing_channel,
    "help": show_help_menu
}

print("=== E-commerce Analytics Guardrail Bot Initialized ===")
print("Type 'help' to see available commands or 'exit' to quit.")

while True:
    raw_input = input("\nYou: ")
    clean_input = raw_input.lower().strip() 
    
    if clean_input == 'exit':
        print("Bot: Shutting down analytics session. Goodbye!")
        break
        
    action = analytics_rules.get(clean_input)
    
    if action:
        print(f"Bot: {action()}")
    else:
        available_products = df['Product'].str.lower().unique()
        
        if clean_input in available_products:
            product_df = df[df['Product'].str.lower() == clean_input]
            product_revenue = product_df['TotalPrice'].sum()
            product_units = product_df['Quantity'].sum()
            print(f"Bot: [{raw_input.capitalize()}] has generated ${product_revenue:,.2f} across {product_units} units sold.")
        else:
            print("Bot: Command not recognized. Type 'help' to see what I can calculate from the dataset.")