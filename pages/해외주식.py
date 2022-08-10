import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px

st.set_page_config(
    page_title="반포자이까지 한걸음",
    page_icon= "chart_with_upwards_trend",
    layout="wide",
)

st.sidebar.markdown("# Overseas stocks 📊")

st.title('Overseas stocks 📈')
Stockcode = pd.read_csv('data/oversea_stockcode.csv')
Stockcode.set_index('Symbol', inplace=True)
Name = st.text_input('Code Name', 'ticker를 입력해주세요.')
Code_name_list = Stockcode.index.tolist()
Stockcode['ticker'] = Stockcode.index
if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'ticker'][0]
    df = fdr.DataReader(code_num)
    df = df.rename(columns={'Open':'시가', 'High':'고가','Low':'저가', 'Close':'종가', 'Volume':'거래량', 'Change':'전일대비'})
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 주식가격",format(df['종가'].tail(1)[0], ',')+'$', "%d$" %(df['종가'].diff().tail(1)[0]))
    col2.metric("현재 거래량", format(round(df['거래량'].tail(1)[0]), ','),"%.2f%%" %(df['거래량'].pct_change().tail(1)[0] * 100))
    col3.metric("전일 대비 가격", "%d$" %(df['종가'].diff().tail(1)[0]), "%.2f%%" %(df['전일대비'].tail(1)[0] * 100))

elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')
