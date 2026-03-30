import streamlit as st
from utils.auth import logout

def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style='display:flex; align-items:center; gap:12px; margin-bottom: 30px; margin-top: 10px;'>
                <div style='background-color:#00c292; width:35px; height:35px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:20px;'>🛡️</div>
                <h2 style='margin:0; font-size:20px; color:#2c3e50; letter-spacing:0.5px; font-weight:800;'>GoTi Macro Monitor</h2>
            </div>
            <div style='font-size: 11px; font-weight:bold; color: #aaa; margin-bottom: 10px; padding-left: 5px; letter-spacing: 1px;'>MAIN MENU</div>
        """, unsafe_allow_html=True)
            
        menus = ["실시간 매크로 모니터링", "AI 방어 어시스턴스 에이전트", "의심 유저 수동 심사", "Grafana"]
        
        def on_menu_change():
            st.session_state.current_menu = st.session_state.menu_radio
            
        if "menu_radio" not in st.session_state:
            st.session_state.menu_radio = st.session_state.get("current_menu", "실시간 매크로 모니터링")
            
        st.radio("MENU", menus, key="menu_radio", on_change=on_menu_change)
        
        st.markdown("<br><br><hr style='border:none; border-top:1px solid #eee; margin:20px 0;'>", unsafe_allow_html=True)
        st.button("로그아웃", on_click=logout, width='stretch')
