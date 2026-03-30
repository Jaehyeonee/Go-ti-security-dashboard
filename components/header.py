import streamlit as st

def render_header(page_title="DASHBOARD"):
    current_user = st.session_state.username or "Admin User"
    
    top_header_html = f"""
    <div class="custom-top-header">
        <div class="top-left" style="margin-left: 50px;">
            <span><span class="active">HOME</span> / {page_title}</span>
        </div>
        <div class="top-right">
            <div class="search-bar">🔍 Search here...</div>
            <div class="icons-group">
                <span>▦</span>
                <span>✉️</span>
                <span>🌙</span>
                <span>🔔</span>
            </div>
            <div class="user-profile">
                <div class="user-avatar">👨🏻‍💻</div>
                <div class="user-info">
                    <span class="user-name">{current_user}</span>
                    <span class="user-role">Admin</span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(top_header_html, unsafe_allow_html=True)
