import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

main_data = pd.read_csv('dashboard/main_data.csv')

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.sidebar.title("Dashboard Filters")

start_date = st.sidebar.date_input("Start Date", pd.to_datetime(main_data['order_purchase_timestamp']).dt.date.min())
end_date = st.sidebar.date_input("End Date", pd.to_datetime(main_data['order_purchase_timestamp']).dt.date.max())

search_customer = st.sidebar.text_input("Search Customer", "")

show_top_cities = st.sidebar.checkbox("Show Top Cities", value=True)

selected_category = st.sidebar.selectbox("Select Product Category", main_data['product_category_name_english'].unique())

filtered_data = main_data[
    (pd.to_datetime(main_data['order_purchase_timestamp']).dt.date >= start_date) &
    (pd.to_datetime(main_data['order_purchase_timestamp']).dt.date <= end_date) &
    (main_data['customer_unique_id'].str.contains(search_customer, case=False)) &
    (main_data['product_category_name_english'] == selected_category)
]

st.title("E-Commerce Dashboard")

st.subheader("Filtered Data")
st.dataframe(filtered_data)

if show_top_cities:
    st.subheader("Top 10 Cities with the Highest Number of Orders")
    orders_by_city = main_data.groupby('customer_city')['order_id'].count().sort_values(ascending=False)
    
    st.bar_chart(orders_by_city.head(10))


st.subheader("Sales Growth in Each Product Category")
sales_by_category = main_data.groupby('product_category_name_english')['order_id'].count().sort_values(ascending=False)
st.bar_chart(sales_by_category)

st.subheader("Shipping Duration Distribution")
main_data['order_delivered_customer_date'] = pd.to_datetime(main_data['order_delivered_customer_date'])
main_data['order_purchase_timestamp'] = pd.to_datetime(main_data['order_purchase_timestamp'])

shipping_duration_days = (main_data['order_delivered_customer_date'] - main_data['order_purchase_timestamp']).dt.days
plt.figure(figsize=(10, 6))
sns.histplot(shipping_duration_days, bins=30, kde=True, color='skyblue')
st.pyplot(plt.gcf())

st.sidebar.text("Data Source: E-Commerce Public Dataset")
