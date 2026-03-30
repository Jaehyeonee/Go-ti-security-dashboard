import streamlit as st

# MUST be first streamit command
st.set_page_config(page_title="Go-Ti Security Admin", layout="wide")

from utils.db import init_db
from utils.auth import init_auth
from utils.session import init_agent_sessions

from components.css_overrides import inject_custom_css
from components.sidebar import render_sidebar
from views.dashboard import render_dashboard
from views.agent import render_agent
from views.review import render_review
from views.grafana import render_grafana

# 앱 최상단에 CSS 레이아웃 주입
inject_custom_css()

# 앱 시작 시 DB 상태 초기화
init_db()

# 에이전트 다중 세션 스토어 초기화
init_agent_sessions()

# 기본 현재 네비게이션 메뉴 상태 선언
if "current_menu" not in st.session_state:
    st.session_state.current_menu = "실시간 매크로 모니터링"

# 로그인 / 인증 확인 (테스트 모드 처리 포함)
is_logged_in = init_auth()

if not is_logged_in:
    # 로그인 실패 시 혹은 화면 진입 통제
    st.stop()

# 인증된 유저라면 사이드바 렌더링 호출
render_sidebar()

# 화면 라우팅 (current_menu 스테이트 기준)
menu_selection = st.session_state.current_menu

if menu_selection == "실시간 매크로 모니터링":
    render_dashboard()
elif menu_selection == "AI 방어 어시스턴스 에이전트":
    render_agent()
elif menu_selection == "의심 유저 수동 심사":
    render_review()
elif menu_selection == "Grafana":
    render_grafana()
