import streamlit as st

def load_session(session_id):
    """지정된 세션 아이디를 활성화하고, AI 에이전트 페이지로 뷰를 강제 전환합니다."""
    st.session_state.active_session_id = session_id
    st.session_state.current_menu = "AI 방어 어시스턴스 에이전트"
    st.session_state.menu_radio = "AI 방어 어시스턴스 에이전트"

def render_agent_history():
    """스크롤 가능한 Agent 대화 히스토리 카드 목록을 렌더링합니다."""
    st.markdown('<div class="section-title">Agent Chat History</div>', unsafe_allow_html=True)
    
    # 딕셔너리 값들을 리스트로 변환 (역순으로 띄우기 위함)
    sessions = list(st.session_state.agent_sessions.values())
    
    # 스크롤 가능한 컨테이너 생성 (지정된 높이를 넘어가면 세로 스크롤 생성됨)
    with st.container(height=420):
        # 최신 세션이 위로 올라오도록 역순 반복
        for sess in reversed(sessions):
            # Streamlit Markdown 지원 버튼을 활용해 카드 형태의 큰 버튼 생성
            btn_label = f" **{sess['date']}**&nbsp;&nbsp;|&nbsp;&nbsp;💬 {sess['topic']}"
            
            # width='stretch' 로 100% 폭을 채우는 블록 버튼 생성
            # on_click 콜백으로 클릭 즉시 세션 아이디 교체 후 자동 리런 유도
            st.button(
                btn_label, 
                key=f"hist_btn_{sess['id']}", 
                on_click=load_session, 
                args=(sess['id'],), 
                width="stretch"
            )
