import streamlit as st
import datetime

def init_agent_sessions():
    """앱 초기화 시 임의의 에이전트 대화 세션 데이터를 주입합니다."""
    if "agent_sessions" not in st.session_state:
        st.session_state.agent_sessions = {
            "sess_1": {
                "id": "sess_1",
                "date": "2026-03-30",
                "topic": "112.111.22.33 IP 정밀 분석",
                "messages": [
                    {"role": "user", "content": "112.111.22.33 IP에 대한 정밀 분석을 실행해줘."},
                    {"role": "assistant", "content": "[Analysis Complete] 해당 IP는 10분간 500회의 비정상적인 직선 마우스 이동이 감지되었습니다. 의심도 95%로 차단 처리되었습니다."}
                ]
            },
            "sess_2": {
                "id": "sess_2",
                "date": "2026-03-29",
                "topic": "최근 스포츠 예매 프록시 패턴 분석",
                "messages": [
                    {"role": "user", "content": "최근 스포츠 예매 티켓 매크로들이 사용하는 proxy ip들의 공통적인 특징을 파악해서 새로운 룰셋을 만들어줘."},
                    {"role": "assistant", "content": "룰셋 생성을 완료했습니다."}
                ]
            },
            "sess_3": {
                "id": "sess_3",
                "date": "2026-03-28",
                "topic": "차단 이력 리포트 생성",
                "messages": [
                    {"role": "user", "content": "차단 이력을 리포트로 생성해줘."},
                    {"role": "assistant", "content": "요청하신 리포트가 생성되었습니다. PDF 형식으로 다운로드할 수 있습니다."}
                ]
            }
        }
    
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = "sess_1"

def create_new_session():
    """새로운 빈 대화 세션을 생성하고 활성화합니다."""
    import uuid
    new_id = f"sess_{uuid.uuid4().hex[:8]}"
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    st.session_state.agent_sessions[new_id] = {
        "id": new_id,
        "date": today_str,
        "topic": "새로운 대화",
        "messages": []
    }
    st.session_state.active_session_id = new_id
