import streamlit as st
import yfinance as yf
import datetime
from datetime import date
from streamlit_option_menu import option_menu
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import requests
hide='''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>'''

st.markdown(hide,unsafe_allow_html=True)
st.title("Spend$mart")
select=option_menu(
    menu_title=None,
    options=['Market','Prediction','News','Contact Us'],orientation='horizontal'
        )
if select == "Prediction":
    st.title('Prediction')
    symbol = st.text_input("Enter a stock token : ",value='AAPL')

    start=st.date_input('Starting Date : ',value=datetime.datetime.today()-datetime.timedelta(days=10))
    end=st.date_input('End Date : ',value=datetime.datetime.today())
    predi=st.date_input("Prediction end date (predictions start from present date) : ",value=datetime.datetime.today()+datetime.timedelta(days=10))
    @st.cache_data
    def stock_data(symbol,start,end):
        data=yf.download(symbol,start,end)
        data.reset_index(inplace=True)
        return data
    tkdata=yf.Ticker(symbol)
    tkdf=tkdata.history(period='1d',start=start,end=end)
    stock=stock_data(symbol,start,end)
    st.header("Stock Data")
    st.write(tkdf)
    no= predi-date.today()
    period=no.days
  
    def plot_graph():
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Open'],name="Stock Open Price"))
        fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Close'],name="Stock Close Price "))
        fig.layout.update(title_text="Stock Data Graph",xaxis_rangeslider_visible=True)
        fig.update_layout(xaxis_title="Price",yaxis_title="Date")        
        st.plotly_chart(fig)
    plot_graph()

    train=stock[['Date','Close']]
    train.columns=['ds','y']
    pro=Prophet(daily_seasonality=True)
    pro.fit(train)
    future=pro.make_future_dataframe(periods=period)
    predictions=pro.predict(future)
    st.header('Predicted Prices')
    df=pd.DataFrame(predictions['ds'])
    df1=pd.DataFrame(predictions['trend'])
    trend=pd.concat([df,df1],axis=1)
    st.write(trend)
    st.text('ds : Date')
    st.text('trend : Price of the Stock')
    
    fig1=plot_plotly(pro,predictions)
    fig1.update_traces(marker=dict(color='light blue'))
    fig1.layout.update(title_text='Prediction Price Graph')
    st.plotly_chart(fig1)

    
if select=='News':
    st.title("News")
    q=st.text_input("Enter the keyword :",value='bitcoin')
    url=f'https://newsapi.org/v2/everything?q={q}&sortBy=publishedAt&apiKey=6f737b4068ca40e9b77eefc66b716478'
    r=requests.get(url)
    r=r.json()
    articles=r['articles']
    for article in articles:
        st.header(article['title'])
        st.write(f"<h5 style=''> Published at : {article['publishedAt']}</h5>",unsafe_allow_html=True)
        if article['author']:
            st.write(article['author'])
        if article['description']==None:
            st.write("Refer The Link")
            st.write(f"{article['url']}")
        else:
            st.write(article['source']['name'])
            st.write(article['description'])
            st.write(f"See More :  {article['url']}")
            try:
                st.image(article['urlToImage'])
            except AttributeError:
                st.write("IMAGE IS NOT AVAILABLE")
            else:
                pass
    
if select=="Contact Us":
    st.title("Get in Touch With Us")
    form='''<form action = 'https://formsubmit.co/4e842a83b01a714615ee75a8fd702e56' method="POST">
Name : 
<input type = "hidden" name="_captcha" value="false">
<input type = "text" name="name" placeholder="Your Name" required>
Email : <input type = "email" name="email" placeholder="Your email" required>
Message : <textarea name="message" placeholder='Your Message Here' required></textarea>
<button type="Submit">Submit</button>
</form>'''

    st.markdown(form,unsafe_allow_html=True)

    def css():
        st.markdown("""<style> 
input[type=text], select, textarea {
background-color: #36454F;
color : white;
  width: 100%; 
  padding: 12px;  
  border: 1px solid #ccc; 
  border-radius: 4px;
  box-sizing: border-box;
  margin-top: 6px;
  margin-bottom: 16px; 
  resize: vertical
}
input[type=email] {width: 100%;
color : white;
  padding: 12px; 
  background-color: #36454F;
  border: 1px solid #ccc;
  border-radius: 4px; 
  box-sizing: border-box;
  margin-top: 6px; 
  margin-bottom: 16px; }


input[type=submit] {
  background-color: #04AA6D;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

input[type=submit]:hover {
  background-color: #45a049;
}</style>""",unsafe_allow_html=True)
    css()

    
           
if select=="Market":
    st.title("Market")
    wt=st.selectbox("Select",('Stock Token','S&P 500'))
    if wt=='Stock Token':
        sym=st.text_input('Stock',"AAPL").upper()

        rqst=f"""https://query1.finance.yahoo.com/v10/finance/quoteSummary/{sym}?modules=assetProfile%2Cprice"""
        request=requests.get(f"{rqst}",headers={"USER-AGENT":"Mozilla/5.0"})
        json=request.json()
        data=json["quoteSummary"]["result"][0]

        st.header(f"About : {sym}")
        e=data['price']['longName']
        st.subheader(f"Name : {e}")
        b=data["assetProfile"]["sector"]
        st.subheader(f"Sector : {b}")
        c=data["assetProfile"]["industry"]
        st.subheader(f"Industry : {c}")
        d=data["price"]["marketCap"]['fmt']
        st.subheader(f"Market Capital : {d}")
        st.markdown((data['assetProfile']["website"]),unsafe_allow_html=True)
        with st.expander("About Company"):
            st.write(data["assetProfile"]["longBusinessSummary"])


        start=datetime.datetime.today()-datetime.timedelta(days=3650)
        end=datetime.datetime.today()
        tkdata=yf.Ticker(sym)
        tkdf=tkdata.history(period='1d',start=start,end=end)
        def stock_data(symbol,start,end):
            data=yf.download(symbol,start,end)
            data.reset_index(inplace=True)
            return data
    
        stock=stock_data(sym,start,end)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=stock['Date'],y=stock['Close']))
        fig.update_layout(title=sym,xaxis_title="Price",yaxis_title="Date")
        fig.layout.update(xaxis_rangeslider_visible=True)
        st.subheader("Price Graph")
        st.plotly_chart(fig)
        st.subheader("Price Chart")
        st.write(tkdf)
    if wt=="S&P 500":
        st.header("S&P 500")
        @st.cache_data
        def load_data():
            url='https://en.wikipedia.org/wiki/list_of_S%26P_500_companies'
            html=pd.read_html(url,header=0)
            df=html[0]
            return df
        df=load_data()
        sector=df.groupby("GICS Sector")

        sortsector = sorted(df['GICS Sector'].unique())
        selectsector=st.multiselect("Sector",sortsector,sortsector)

        df1=df[(df['GICS Sector'].isin(selectsector))]

        st.write("Number of Companies for selected Categories : "+ str(df1.shape[0]))
        st.dataframe(df1)
        data=yf.download(tickers=list(df1[:10].Symbol),period = 'ytd',interval='1d',group_by = 'ticker',auto_adjust=True,prepost=True,threads=True,proxy=None)
        def price_plot(symbol):
            df=pd.DataFrame(data[symbol].Close)
            df['Date']=df.index
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=df.Date,y=df.Close,name="Stock Close Price "))
            fig.layout.update(title_text=symbol,xaxis_rangeslider_visible=True)
            fig.update_layout(xaxis_title="Date",yaxis_title="Price")        
            st.plotly_chart(fig)
        num=st.selectbox("Number of Company Graphs : ",(1,2,3,4,5,6,7,8,9,10))
        if st.button('Graphs'):
            st.subheader(f"Graphs of Top {num} Companies")
            for i in list(df1.Symbol)[:num]:
                price_plot(i)
