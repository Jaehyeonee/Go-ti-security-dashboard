import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from components.header import render_header
from components.agent_history import render_agent_history
from data.provider import get_provider

def render_dashboard():
    provider = get_provider()
    
    # Top Header Injection
    render_header()
    st.markdown('<div class="section-title" style="margin-top: 25px;">매크로 탐지 현황</div>', unsafe_allow_html=True)
    
    # 1. Top Metrics Cards — Provider에서 데이터 가져오기
    stats = provider.get_dashboard_stats()
    
    cards_html = f"""
    <div class="metric-card-container">
        <div class="m-stat-card">
            <div class="m-stat-title">금일 접속 건수</div>
            <div><span class="m-stat-value">{stats['total_access']:,}</span><span class="m-stat-unit">건</span></div>
            <div class="m-stat-badge {stats['total_access_badge']}">{stats['total_access_delta']}</div>
        </div>
        <div class="m-stat-card">
            <div class="m-stat-title">접속자 건수</div>
            <div><span class="m-stat-value">{stats['unique_users']:,}</span><span class="m-stat-unit">건</span></div>
            <div class="m-stat-badge {stats['unique_users_badge']}">{stats['unique_users_delta']}</div>
        </div>
        <div class="m-stat-card">
            <div class="m-stat-title">매크로 차단 건수</div>
            <div><span class="m-stat-value">{stats['blocked_count']:,}</span><span class="m-stat-unit">건</span></div>
            <div class="m-stat-badge {stats['blocked_badge']}">{stats['blocked_delta']}</div>
        </div>
        <div class="m-stat-card">
            <div class="m-stat-title">차단율</div>
            <div><span class="m-stat-value">{stats['block_rate']}</span><span class="m-stat-unit">%</span></div>
            <div class="m-stat-badge {stats['block_rate_badge']}">{stats['block_rate_delta']}</div>
        </div>
    </div>
    """
    st.markdown(cards_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Middle Row: Map & Agent History
    col_charts, col_map = st.columns([1, 1.5], gap="large")
    
    with col_map:
        st.markdown('<div class="section-title" style="margin-top: 10%;">매크로 발생 주요 국가</div>', unsafe_allow_html=True)
        
        # Provider에서 지도 데이터 가져오기
        loc_data = provider.get_geo_detection_data()
        
        if not loc_data.empty:
            my_map = folium.Map(
                location=[loc_data['Lat'].mean(), loc_data['Lon'].mean()], 
                zoom_start=2,
                tiles='CartoDB Positron'
            )
            
            for index, row in loc_data.iterrows():
                folium.CircleMarker(
                    location=[row['Lat'], row['Lon']],
                    radius=row['Detections'] / 30,
                    color='#ef4444',             
                    fill=True,
                    fill_color='#ef4444',
                    fill_opacity=0.5,
                    weight=1
                ).add_to(my_map)

                folium.Marker(
                    location=[row['Lat'], row['Lon']],
                    icon=folium.DivIcon(
                        html=f"<div style='font-size: 11px; font-weight: 700; color: #1e293b; background: rgba(255,255,255,0.6); padding: 2px 4px; border-radius: 4px; border: 1px solid #cbd5e1; white-space: nowrap; transform: translate(-50%, -150%);'>{row['Country']} {row['Detections']}</div>"
                    ),
                ).add_to(my_map)
                
            st.components.v1.html(my_map._repr_html_(), height=480)
        else:
            st.info("지도 데이터를 불러올 수 없습니다.")

    with col_charts:
        st.markdown('<div class="chart-bg-target"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">매크로 조치 현황</div>', unsafe_allow_html=True)
        from components.charts import render_status_donut_chart
        df_history = provider.get_enriched_history()
        render_status_donut_chart(df_history, height=220)
        
        st.markdown('<div class="section-title" style="margin-top: 25px;">탐지 유형 통계</div>', unsafe_allow_html=True)
        
        # Provider에서 바 차트 데이터 가져오기
        bar_data = provider.get_detection_type_stats()
        
        if not bar_data.empty:
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
        else:
            st.info("탐지 유형 데이터를 불러올 수 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Middle Row: Agent History
    render_agent_history()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. Bottom Row: Recent Detections List
    bottom_col, = st.columns(1)
    with bottom_col:
        st.markdown('<div class="section-title">Recent Detections List</div>', unsafe_allow_html=True)
        df_display = provider.get_enriched_history()
        
        if not df_display.empty:
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
