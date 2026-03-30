import streamlit as st
from streamlit_cognito_auth import CognitoAuthenticator

def init_auth():
    """인증 상태를 확인하고 로그인 UI 혹은 세션 처리를 수행합니다."""
    POOL_ID = st.secrets.get("COGNITO_USER_POOL_ID", "YOUR_POOL_ID")
    APP_CLIENT_ID = st.secrets.get("COGNITO_APP_CLIENT_ID", "YOUR_CLIENT_ID")
    APP_CLIENT_SECRET = st.secrets.get("COGNITO_APP_CLIENT_SECRET", "YOUR_CLIENT_SECRET")

    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "authenticator" not in st.session_state:
        st.session_state.authenticator = None
    if "username" not in st.session_state:
        st.session_state.username = None

    if hasattr(st, "user"):
        try:
            user_info = st.user.to_dict() if hasattr(st.user, "to_dict") else dict(st.user)
        except Exception:
            user_info = {}

        if user_info:
            st.session_state.is_logged_in = True
            st.session_state.username = user_info.get("given_name") or user_info.get("email") or "Authenticated User"

    if POOL_ID == "YOUR_POOL_ID":
        st.session_state.is_logged_in = True
        st.sidebar.warning("⚠️ 테스트 모드 (Cognito 연동 전)")
    else:
        if not st.session_state.is_logged_in:
            if st.session_state.authenticator is None:
                st.session_state.authenticator = CognitoAuthenticator(
                    pool_id=POOL_ID,
                    app_client_id=APP_CLIENT_ID,
                    app_client_secret=APP_CLIENT_SECRET,
                )

            st.session_state.is_logged_in = st.session_state.authenticator.login()

            if st.session_state.is_logged_in:
                try:
                    ua = st.session_state
                    username = ua.get("username") if ua else None
                    if not username:
                        username = ua.get("auth_email") if ua else None
                except (AttributeError, TypeError):
                    username = None

                st.session_state.username = username or "Authenticated User"

    if not st.session_state.is_logged_in:
        st.info("Go-Ti 보안팀 Admin 시스템입니다. 등록된 관리자 계정으로 로그인해주세요.")
        
    return st.session_state.is_logged_in

def logout():
    """로그아웃 함수"""
    POOL_ID = st.secrets.get("COGNITO_USER_POOL_ID", "YOUR_POOL_ID")
    if POOL_ID != "YOUR_POOL_ID":
        if st.session_state.authenticator:
            st.session_state.authenticator.logout()
            
    st.session_state.is_logged_in = False
    st.session_state.authenticator = None
    st.session_state.username = None
