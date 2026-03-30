import streamlit as st
import plotly.express as px
import pandas as pd

def render_status_donut_chart(df, height=220):
    """
    주어진 데이터프레임의 'Status' 컬럼을 집계하여,
    일관성 있는 [차단/경고/대기] 원형 파이 차트(Donut)를 그려주는 재사용 컴포넌트입니다.
    """
    if "Status" not in df.columns:
        st.error("데이터에 'Status' 컬럼이 없습니다.")
        return
        
    # 상태별 개수 집계
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    # 색상 강제 매핑 딕셔너리
    color_map = {
        "Blocked": "#ef4444", 
        "Warning": "#f59e0b", 
        "Pending": "#3b82f6",
        "Passed": "#10b981" # 혹시 Passed 값이 있다면 초록색 리턴
    }
    
    fig_pie = px.pie(
        status_counts, 
        names="Status", 
        values="Count", 
        hole=0.4,
        color="Status", 
        color_discrete_map=color_map
    )
    
    # 여백 최적화 
    fig_pie.update_layout(
        margin=dict(l=0, r=0, t=10, b=0), 
        height=height
    )
    
    # 렌더링
    st.plotly_chart(fig_pie, width="stretch")
