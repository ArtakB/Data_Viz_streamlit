import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# Load your data with new caching
@st.cache_data
def load_data():
    data = pd.read_csv('Data-Model-Pizza-Sales.csv')
    # Convert 'order_date' to datetime at the point of loading to ensure consistency.
    if 'order_date' in data.columns:
        data['order_date'] = pd.to_datetime(data['order_date'])
    return data

data = load_data()

# Define the pages
def home_page():
    st.title('🍕 Pizza Sales Dashboard')

    # Introduction text with larger font size and spacing for better readability
    st.markdown("""
        <div style="text-align: center;">
            <h2>Welcome to the Pizza Sales Insights Dashboard!</h2>
            <p style="font-size: 18px;">Explore interactive visualizations and gain detailed insights into pizza sales trends and patterns. Dive into the data to uncover key factors driving pizza sales across different categories and sizes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Layout using columns to separate text and image for a balanced look
    col1, col2 = st.columns([2, 3])  # Adjusting column width ratios for better visual balance

    with col1:
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin: 5px;">
            <h3>🔍 Discover</h3>
            <p>Utilize the interactive tools provided to filter and visualize sales data based on categories, sizes, and date ranges.</p>
            <h3>📊 Analyze</h3>
            <p>Access various analysis sections to understand sales dynamics, peak times, and customer preferences.</p>
            <h3>📈 Optimize</h3>
            <p>Identify bestsellers and areas for improvement to optimize sales strategies and maximize revenue.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Ensure the image is centered and appropriately sized within the column
        st.image(Image.open('pizza_image.jpg'), caption='Explore Pizza Data', use_column_width='auto')

    # Adding a spacer for aesthetic spacing
    st.markdown('<hr style="margin-top: 50px; margin-bottom: 50px;">', unsafe_allow_html=True)

    # A more interactive or engaging footer
    st.markdown("""
        <div style="text-align: center; color: grey;">
            <p>Designed and built by Artak Bakhshyan.</p>
        </div>
        """, unsafe_allow_html=True)


def data_visualization():
    st.title('📊 Data Visualization')
    st.markdown("""
    <div style='text-align: justify; padding: 20px; margin-top: 20px; border-radius: 10px; background-color: #f8f9fa; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <p style='font-size: 18px; color: #333;'>
            Explore key metrics and trends in pizza sales through simplified visualizations. Dive deeper into the categories and sizes to gain insights into sales performance. This dashboard allows you to interact with the data, uncovering underlying patterns that drive business decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stylish and simple selection for pizza categories
    st.markdown("""
    <style>
        .stSelectbox {
            font-size: 16px;
            border: 1px solid #009688;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

    pizza_filter = st.selectbox('Select Pizza Category:', options=np.unique(data['pizza_category']))

    # Filtered data based on the selected pizza category
    filtered_data = data[data['pizza_category'] == pizza_filter]

    # Bar chart for total sales by pizza within the selected category
    total_sales_by_pizza = filtered_data.groupby('pizza_name').agg({'total_price': 'sum'}).reset_index()
    fig_bar = px.bar(total_sales_by_pizza, x='pizza_name', y='total_price', title=f'Total Sales by Pizza in "{pizza_filter}" Category')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie chart for the proportion of sales by pizza size
    sales_by_size = filtered_data.groupby('pizza_size').agg({'total_price': 'sum'}).reset_index()
    fig_pie = px.pie(sales_by_size, values='total_price', names='pizza_size', title=f'Sales Distribution by Size in "{pizza_filter}" Category')
    st.plotly_chart(fig_pie, use_container_width=True)

    # Line chart for sales trend over time
    if 'order_date' in data.columns:
        filtered_data['order_date'] = pd.to_datetime(filtered_data['order_date'])
        sales_over_time = filtered_data.groupby('order_date').agg({'total_price': 'sum'}).reset_index()
        fig_line = px.line(sales_over_time, x='order_date', y='total_price', title=f'Sales Trend Over Time in "{pizza_filter}" Category')
        st.plotly_chart(fig_line, use_container_width=True)

    # Optionally show the data table with style enhancements
    if st.checkbox('Show Data Table', value=False):
        st.dataframe(filtered_data.style.applymap(lambda x: 'background-color: #e3f2fd'))

    # Download button with custom styling
    st.markdown("""
    <style>
        .stDownloadButton>button {
            border: none;
            border-radius: 5px;
            font-size: 16px;
            background-color: #009688;
            color: white;
            padding: 10px 24px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    st.download_button('Download Filtered Data as CSV', data=filtered_data.to_csv(index=False), file_name=f'{pizza_filter}_data.csv', mime='text/csv')

def data_analysis():
    st.title('🔍 Data Analysis')
    st.markdown("""
    <div style='text-align: justify; padding: 20px; margin-top: 20px; border-radius: 10px; background-color: #f8f9fa; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
        <p style='font-size: 18px; color: #333;'>
            Gain deeper insights into the pizza sales data. Analyze total sales, average prices, top-selling pizzas, and sales trends over time. Use the comparative analysis to understand how different pizzas perform against each other.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter for detailed analysis
    category = st.selectbox('Select Category:', options=np.unique(data['pizza_category']))
    filtered_data = data[data['pizza_category'] == category]

    # Metric cards for key statistics
    total_sales = filtered_data['total_price'].sum()
    average_price = filtered_data['unit_price'].mean()
    top_selling_pizza = filtered_data.groupby('pizza_name')['total_price'].sum().idxmax()
    top_pizza_sales = filtered_data.groupby('pizza_name')['total_price'].sum().max()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    with col2:
        st.metric(label="Average Price", value=f"${average_price:.2f}")
    with col3:
        st.metric(label="Top Selling Pizza", value=top_selling_pizza)
    with col4:
        st.metric(label="Top Pizza Sales", value=f"${top_pizza_sales:,.2f}")

    # Time series analysis for sales over time
    if 'order_date' in data.columns:
        st.markdown("### Sales Over Time")
        filtered_data['order_date'] = pd.to_datetime(filtered_data['order_date'])
        time_data = filtered_data.groupby('order_date')['total_price'].sum().reset_index()
        fig_time_series = px.line(time_data, x='order_date', y='total_price', title='Daily Sales Over Time')
        st.plotly_chart(fig_time_series, use_container_width=True)

    # Comparative analysis for selected pizzas
    st.markdown("### Comparative Analysis")
    compare = st.multiselect('Select pizzas to compare:', options=data['pizza_name'].unique())
    if compare:
        comparison_data = data[data['pizza_name'].isin(compare)]
        fig_compare = px.bar(comparison_data, x='pizza_name', y='total_price', color='pizza_name',
                             labels={'total_price': 'Total Sales'}, title='Comparative Sales by Pizza')
        st.plotly_chart(fig_compare, use_container_width=True)

    # Download button for the filtered data
    st.markdown("### Download Data")
    st.markdown("""
    <style>
        .stDownloadButton>button {
            border: none;
            border-radius: 5px;
            font-size: 16px;
            background-color: #009688;
            color: white;
            padding: 10px 24px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    st.download_button(label="Download Data as CSV", data=filtered_data.to_csv(index=False), file_name='filtered_data.csv', mime='text/csv')

# Setup sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio("Choose a page:", ['Home', 'Data Visualization', 'Data Analysis'])

if page == 'Home':
    home_page()
elif page == 'Data Visualization':
    data_visualization()
elif page == 'Data Analysis':
    data_analysis()
