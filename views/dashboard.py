import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from components.header import render_header
from components.agent_history import render_agent_history
from utils.db import load_history_from_db

def render_dashboard():
    # Top Header Injection
    render_header()
    st.markdown('<div class="section-title" style="margin-top: 25px;">매크로 탐지 현황</div>', unsafe_allow_html=True)
    
    # 1. Top Metrics Cards (Updated Design matching User Image)
    cards_html = """
    <div class="metric-card-container">
        <div class="m-stat-card">
            <div class="m-stat-title">금일 접속 건수</div>
            <div><span class="m-stat-value">14,859</span><span class="m-stat-unit">건</span></div>
            <div class="m-stat-badge badge-up">↑ +120</div>
        </div>
        <div class="m-stat-card">
            <div class="m-stat-title">접속자 건수</div>
            <div><span class="m-stat-value">6,513</span><span class="m-stat-unit">건</span></div>
            <div class="m-stat-badge badge-down">↓ -40</div>
        </div>
        <div class="m-stat-card">
            <div class="m-stat-title">매크로 차단 건수</div>
            <div><span class="m-stat-value">8,346</span><span class="m-stat-unit">건</span></div>
            <div class="m-stat-badge badge-up">↑ +500</div>
        </div>
        <div class="m-stat-card">
            <div class="m-stat-title">차단율</div>
            <div><span class="m-stat-value">56.2</span><span class="m-stat-unit">%</span></div>
            <div class="m-stat-badge badge-up">↑ 1.2%</div>
        </div>
    </div>
    """
    st.markdown(cards_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Middle Row: Map & Agent History (Ongoing Projects) inside bordered white containers
    col_charts, col_map = st.columns([1, 1.5], gap="large")
    
    with col_map:
        st.markdown('<div class="section-title" style="margin-top: 10%;">매크로 발생 주요 국가</div>', unsafe_allow_html=True)
        # Generate mock coordinate data for the map
        loc_data = pd.DataFrame({
            'Country': ['Canada', 'Russia', 'Greenland', 'USA', 'China', 'Brazil', 'Australia', 'India', 'Japan', 'Korea'],
            'Lat': [56.13, 61.52, 71.7, 37.09, 35.86, -14.23, -25.27, 20.59, 35.6895, 37.5665],
            'Lon': [-106.34, 105.31, -42.6, -95.71, 104.19, -51.92, 133.77, 78.96, 139.6917, 126.9780],
            'Detections': [175, 162, 191, 220, 185, 145, 130, 110, 300, 700]
        })
        # Folium 기반 지도 객체 생성
        my_map = folium.Map(
            location=[loc_data['Lat'].mean(), loc_data['Lon'].mean()], 
            zoom_start=2,
            tiles='CartoDB Positron' # 깔끔한 도화지 테마
        )
        
        # 지도에 원형 마커와 텍스트 값 추가
        for index, row in loc_data.iterrows():
            # 탐지 횟수 비례 원형 마커
            folium.CircleMarker(
                location=[row['Lat'], row['Lon']],
                radius=row['Detections'] / 30, # 크기 비율 조정
                color='#ef4444',             
                fill=True,
                fill_color='#ef4444',
                fill_opacity=0.5,
                weight=1
            ).add_to(my_map)

            # 국가명 및 값 텍스트 표시
            folium.Marker(
                location=[row['Lat'], row['Lon']],
                icon=folium.DivIcon(
                    html=f"<div style='font-size: 11px; font-weight: 700; color: #1e293b; background: rgba(255,255,255,0.6); padding: 2px 4px; border-radius: 4px; border: 1px solid #cbd5e1; white-space: nowrap; transform: translate(-50%, -150%);'>{row['Country']} {row['Detections']}</div>"
                ),
            ).add_to(my_map)
            
        # HTML 렌더링으로 Streamlit에 주입 (크기 맞춤)
        st.components.v1.html(my_map._repr_html_(), height=480)

    with col_charts:
        st.markdown('<div class="chart-bg-target"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">매크로 조치 현황</div>', unsafe_allow_html=True)
        from components.charts import render_status_donut_chart
        from utils.db import get_enriched_history
        render_status_donut_chart(get_enriched_history(), height=220)
        
        st.markdown('<div class="section-title" style="margin-top: 25px;">탐지 유형 통계</div>', unsafe_allow_html=True)
        # 탐지 유형별 바 차트 (Bar Chart)
        bar_data = pd.DataFrame({
            "Type": ["Mouse Macro", "API Abuse", "Fast Click", "Proxy IP"],
            "Count": [240, 180, 140, 90]
        })
        fig_bar = px.bar(
            bar_data, x="Count", y="Type", orientation='h',
            color="Type",
            color_discrete_sequence=["#8b5cf6", "#14b8a6", "#ec4899", "#f59e0b"]
        )
        fig_bar.update_layout(
            margin=dict(l=0, r=10, t=10, b=0), 
            height=200, 
            showlegend=False,
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(title="")
        )
        st.plotly_chart(fig_bar, width="stretch")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Middle Row: Agent History
    render_agent_history()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. Bottom Row: Recent Orders (Recent Macro History) nested in bordered container
    bottom_col, = st.columns(1)
    with bottom_col:
        st.markdown('<div class="section-title">Recent Detections List</div>', unsafe_allow_html=True)
        from utils.db import get_enriched_history
        df_display = get_enriched_history()
        
        if not df_display.empty:
            # 최종 보여줄 컬럼 정렬 (대상 경기 포함)
            df_display = df_display[["Event ID", "접속시간", "대상 경기", "접속IP", "Target URL", "탐지유형", "Status", "Risk Score"]]
            
            st.dataframe(
                df_display, 
                width='stretch', 
                hide_index=True,
                column_config={
                    "Status": st.column_config.TextColumn("Status", help="Action taken by the detection system"),
                    "Risk Score": st.column_config.ProgressColumn(
                        "Risk Score", help="Probability of macro behavior (0-100)", format="%d", min_value=0, max_value=100
                    )
                }
            )
        else:
            st.info("No recent interventions recorded.")
