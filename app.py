import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='StartUp Analysis', page_icon='favicon.ico')

df = pd.read_csv('startup cleaned.csv')

df['date'] = pd.to_datetime(df['date'], errors= 'coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# over all investor details
def load_overall_analysis():
    st.title('Show Overall Analysis:')

    total_amount = round(df['amount'].sum())
    # max amount in startup
    max_amount = round((df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]))
    #avg amount on startup
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    #total startups
    total_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total Invested Amount', str(total_amount) + ' Cr')
    with col2:
        st.metric('Max Funding ', str(max_amount) + ' Cr')
    with col3:
        st.metric('Avg Funding On Startup',str(avg_funding) + ' Cr')
    with col4:
        st.metric('Total Startups',str(total_startups))
        

    # month on monnth investments
    st.header('Month On Month Investments')
    selected_option = st.selectbox('Select One', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)

# investor detail on each startup
def load_investor_details(investor):
    st.title(investor)
    load_5df = df[df['investors'].str.contains('investor')].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(load_5df)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
    #big investments
        big_investment = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending= False).head()
        st.subheader('Biggest Investments')

        fig, ax = plt.subplots()
        ax.bar(big_investment.index, big_investment.values)
        st.pyplot(fig)

    with col2:
        sectors_investment = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Secters Invested In')

        fig1, ax1 = plt.subplots()
        ax1.pie(sectors_investment, labels = sectors_investment.index, autopct = '%0.01f')
        st.pyplot(fig1)
    with col3:

        
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('YoY Investment')

        fig2, ax2 = plt.subplots()
        ax2.plot(year_series.index, year_series.values)
        st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')
options = st.sidebar.selectbox('Select One', ['Overall Analysis','Startup', 'Investers'])

if options == 'Overall Analysis':
    load_overall_analysis()

elif options == 'Startup':
    st.sidebar.selectbox('Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

else:
    user_selceted = st.sidebar.selectbox('Startup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Detail')
    if btn2:
        load_investor_details(user_selceted)
        
    
