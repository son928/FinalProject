import pandas as pd
import streamlit as st
import FinanceDataReader as fdr
import plotly.graph_objects as go
import plotly.express as px

st.title('국내 주식 현황입니다.')
Stockcode = pd.read_csv('data/Stockcode.csv')
Stockcode.set_index('Name', inplace=True)
Name = st.text_input('Code Name')
Code_name_list = Stockcode.index.tolist()

if Name in Code_name_list:
    code_num = Stockcode.at[Name, 'Symbol']
    df = fdr.DataReader(code_num)
    df = df.rename(columns={'Open':'시가', 'High':'고가','Low':'저가', 'Close':'종가', 'Volume':'거래량', 'Change':'전일대비'})
    col1, col2, col3 = st.columns(3)
    col1.metric("현재 주식가격",format(df['종가'].tail(1)[0], ',')+'원', "%d원" %(df['종가'].diff().tail(1)[0]))
    col2.metric("현재 거래량", format(df['거래량'].tail(1)[0], ','),"%.2f%%" %(df['거래량'].pct_change().tail(1)[0] * 100))
    col3.metric("전일 대비 가격", round(df['전일대비'].tail(1)[0], 4), "%.2f%%" %(df['전일대비'].tail(1)[0] * 100))
    
    fig = px.line(df, y='종가', title='{} 종가 Time Series'.format(Name))

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['시가'],
                high=df['고가'],
                low=df['저가'],
                close=df['종가'],
                increasing_line_color = 'tomato',
                decreasing_line_color = 'royalblue',
                showlegend = False)])

    fig2.update_layout(title='{} Candlestick chart'.format(Name))
    st.plotly_chart(fig2, use_container_width=True)

elif Name not in Code_name_list:
    st.text('검색하신 주식 종목이 없습니다. 정확하게 입력해주세요.')
