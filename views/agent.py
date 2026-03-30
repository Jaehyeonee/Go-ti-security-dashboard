import streamlit as st
from utils.db import load_history_from_db
from utils.api import get_solar_client
from components.header import render_header

def render_agent():
    render_header("AI AGENT")
    st.subheader("🫆 매크로 방어 정책 에이전트")
    
    # 최근 매크로 차단 이력 데이터 준비 (DB에서 로드)
    df_history = load_history_from_db()
    history_text = df_history.to_string(index=False)
    
    system_prompt = f"Go-Ti 매크로 관제 에이전트입니다. 다음은 최근 매크로 차단 이력 데이터입니다:\n{history_text}\n\n이 데이터를 참고하여 사용자의 질문에 답변하세요."
    
    # 활성화된 세션 컨텍스트 가져오기
    if "agent_sessions" not in st.session_state or "active_session_id" not in st.session_state:
        from utils.session import init_agent_sessions
        init_agent_sessions()
        
    active_id = st.session_state.active_session_id
    current_session = st.session_state.agent_sessions[active_id]
    
    # 상단 메뉴바에 신규 세션 생성 버튼 추가
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("➕ 새 대화 시작", type="primary", width="content"):
            from utils.session import create_new_session
            create_new_session()
            st.rerun()
            
    st.markdown(f"**현재 세션:** `{current_session['topic']}` (_{current_session['date']}_)")
    st.divider()
    
    if len(current_session["messages"]) == 0:
        current_session["messages"].append({"role": "assistant", "content": "무엇을 도와드릴까요?"})

    for msg in current_session["messages"]:
        if msg["role"] != "system":  # 시스템 메시지는 표시하지 않음
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("메시지를 입력하세요."):
        # Update topic to first prompt if it's a new conversation
        if current_session["topic"] == "새로운 대화":
            current_session["topic"] = prompt[:15] + "..." if len(prompt) > 15 else prompt
            
        current_session["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            UPSTAGE_API_KEY = st.secrets.get("UPSTAGE_API_KEY", "YOUR_UPSTAGE_API_KEY")
            if UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY":
                response = "API 키가 등록되지 않았습니다. `.streamlit/secrets.toml`을 확인해주세요."
                st.markdown(response)
                current_session["messages"].append({"role": "assistant", "content": response})
            else:
                solar_client = get_solar_client()
                message_placeholder = st.empty()
                full_response = ""
                
                # API로 보낼 메시지 구성 (최신 컨텍스트 + 시스템 프롬프트 주입)
                api_messages = [{"role": "system", "content": system_prompt}] + current_session["messages"]
                
                api_response = solar_client.chat.completions.create(
                    model="solar-pro",
                    messages=api_messages,
                    stream=True
                )
                for chunk in api_response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                current_session["messages"].append({"role": "assistant", "content": full_response})
