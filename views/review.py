import streamlit as st
import time
import json
from components.header import render_header
from components.charts import render_status_donut_chart
from utils.db import get_enriched_history, update_override_status

def fetch_opensearch_report_mock(event_id):
    """5 mock OpenSearch reports logic simulating elastic backend."""
    print(f"[OPENSEARCH API CALL] GET /api/v1/opensearch/reports/{event_id}")
    time.sleep(0.5)
    
    mock_db = {
        "#VZ1000": {
            "index": "macro-events-2026.03",
            "_id": "doc_vz1000",
            "threat_score": 94,
            "matched_rules": ["Mouse Linearity Threshold Exceeded", "Click Frequency High"],
            "raw_logs": {"click_rate": "15 cps", "mouse_variance": 0.001, "ip_reputation": "suspicious"}
        },
        "#VZ1001": {
            "index": "macro-events-2026.03",
            "_id": "doc_vz1001",
            "threat_score": 72,
            "matched_rules": ["API Abuse Detected", "Invalid User Agent"],
            "raw_logs": {"api_calls_per_sec": 50, "user_agent": "python-requests/2.31", "ip_reputation": "clean"}
        },
        "#VZ1002": {
            "index": "macro-events-2026.03",
            "_id": "doc_vz1002",
            "threat_score": 88,
            "matched_rules": ["Session Token Reused", "Simultaneous Login"],
            "raw_logs": {"active_sessions": 5, "geo_location": "Russia", "ip_reputation": "bad"}
        },
        "#VZ1003": {
            "index": "macro-events-2026.03",
            "_id": "doc_vz1003",
            "threat_score": 61,
            "matched_rules": ["Fast Checkout", "Bypass Captcha Time"],
            "raw_logs": {"checkout_duration_ms": 120, "captcha_solve_time": 0.1, "ip_reputation": "clean"}
        },
        "#VZ1004": {
            "index": "macro-events-2026.03",
            "_id": "doc_vz1004",
            "threat_score": 45,
            "matched_rules": ["Proxy IP Detected"],
            "raw_logs": {"proxy_type": "Data Center", "anonymity_level": "High", "ip_reputation": "warning"}
        }
    }
    
    default_mock = {
        "index": "macro-events-unknown",
        "_id": f"doc_{event_id.lower()}",
        "threat_score": "N/A",
        "matched_rules": ["General Suspicious Behavior"],
        "raw_logs": {"detail": "No deep logs available for this generated ID."}
    }
    
    return mock_db.get(event_id, default_mock)

@st.dialog("분석 리포트 상세", width="large")
def show_opensearch_report(event_id, row_data):
    st.subheader(f"🔍 {event_id} 매크로 탐지 원인 분석")
    st.caption("OpenSearch 클러스터에 저장된 상세 백엔드 이벤트 로그입니다.")
    st.divider()
    
    with st.spinner("OpenSearch에서 로우 데이터를 불러오는 중..."):
        report = fetch_opensearch_report_mock(event_id)
        
    st.markdown(f"**탐지된 보안 룰 (Matched Rules):**")
    for rule in report['matched_rules']:
        st.error(f"🚨 {rule}")
        
    st.markdown("<br>**OpenSearch JSON 원본 (Raw Logs):**", unsafe_allow_html=True)
    st.json(report)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("닫기", width="stretch"):
        st.rerun()


def execute_review_api_call(event_id, action):
    """
    Mock API Call to handle manual review action (Block/Pass).
    Exhibits brief simulated latency and console logs before saving.
    """
    # Simulate Network Request to backend (e.g., /api/v1/interventions/action)
    print(f"[API CALL] POST /api/v1/interventions/{event_id}/action -> Payload: {{'action': '{action}'}}")
    time.sleep(0.5) 
    
    # Save the changed state in the local Session DB so the dashboard correctly updates
    update_override_status(event_id, action)
    print(f"[API SUCCESS] Event {event_id} status updated to {action}.")

def handle_review_action(event_id, action):
    """Button click callback handler."""
    execute_review_api_call(event_id, action)
    action_kor = "차단" if action == "Blocked" else "패스"
    st.toast(f"✅ **{event_id}** 건에 대한 수동 **{action_kor}** 처리가 완료되었습니다.", icon="🚨" if action == "Blocked" else "✅")

def render_review():
    render_header("MANUAL REVIEW")
    st.header("고위험 계정 수동 검토")
    st.write("실시간 AI 탐지로 적발된 이력 중 추가 확인이 필요한 건(Pending/Warning)에 대해 수동 검토를 진행합니다.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Fetch global history data
    df = get_enriched_history()
    
    if df.empty:
        st.success("데이터가 로드되지 않았습니다.")
        return

    # 1. 상단에 대시보드와 동일한 매크로 조치 현황 차트 렌더링
    st.markdown('<div class="section-title">매크로 조치 현황 (Global View)</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="chart-bg-target"></div>', unsafe_allow_html=True)
        render_status_donut_chart(df, height=180)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. 필터링 컨트롤 UI 추가
    st.markdown('<div class="section-title">검토 목록 필터링</div>', unsafe_allow_html=True)
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    # 중복 제거된 옵션 추출
    available_dates = sorted(df["접속일자"].unique().tolist(), reverse=True)
    available_games = sorted(df["대상 경기"].unique().tolist())
    
    with filter_col1:
        # 날짜 필터 (다중 선택 가능하게 설정)
        selected_dates = st.multiselect("📅 날짜", available_dates, default=available_dates)
    with filter_col2:
        # 대상 경기 필터
        selected_games = st.multiselect("⚾ 대상 경기", available_games, default=available_games)
    with filter_col3:
        # 심사 대상 상태 필터 (기본적으로 Pending과 Warning만)
        selected_status = st.multiselect("🚥 심사 상태", ["Pending", "Warning", "Blocked", "Passed"], default=["Pending", "Warning"])

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. 데이터프레임 필터링 적용
    # 선택된 값이 없으면 아무것도 보여주지 않는 것이 일반적이므로 isin에 빈 리스트가 들어가면 empty가 됨
    filtered_df = df[
        (df["접속일자"].isin(selected_dates)) & 
        (df["대상 경기"].isin(selected_games)) & 
        (df["Status"].isin(selected_status))
    ]
    
    if filtered_df.empty:
        st.success("🎉 현재 설정된 필터 조건에 해당하는 데이터가 없습니다. (또는 모든 검토가 완료되었습니다!)")
        return
        
    # Render interactive cards for each filtered item
    for _, row in filtered_df.iterrows():
        event_id = row['Event ID']
        with st.container(border=True):
            st.markdown(f"#### {event_id}")
            
            # Use columns to lay out the data concisely
            data_col1, data_col2, data_col3 = st.columns([1, 1, 1])
            
            with data_col1:
                st.caption("위험 지표")
                st.markdown(f"**상태:** `{row['Status']}`  \n**Risk:** `{row['Risk Score']} 점`")
            with data_col2:
                st.caption("메타 데이터")
                st.markdown(f"**탐지 유형:** {row['탐지유형']}  \n**대상:** {row['대상 경기']}")
            with data_col3:
                st.caption("발생 시점")
                st.markdown(f"{row['접속시간']}  \n{row['접속IP']}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action Buttons Row (3 Columns Horizontal)
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("🔍 매크로 탐지 원인 분석 리포트", key=f"report_{event_id}", width="stretch"):
                    show_opensearch_report(event_id, row)
            with btn_col2:
                st.button(
                    "🚫 수동 차단", 
                    key=f"block_{event_id}", 
                    type="primary",
                    on_click=handle_review_action, 
                    args=(event_id, "Blocked"),
                    width="stretch"
                )
            with btn_col3:
                st.button(
                    "✅ 통과 (Pass)", 
                    key=f"pass_{event_id}", 
                    on_click=handle_review_action, 
                    args=(event_id, "Passed"),
                    width="stretch"
                )
