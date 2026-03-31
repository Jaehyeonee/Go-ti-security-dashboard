import streamlit as st
import time
import json
from components.header import render_header
from components.charts import render_status_donut_chart
from data.provider import get_provider


@st.dialog("분석 리포트 상세", width="large")
def show_opensearch_report(event_id, row_data):
    provider = get_provider()
    
    st.subheader(f"🔍 {event_id} 매크로 탐지 원인 분석")
    st.caption("OpenSearch 클러스터에 저장된 상세 백엔드 이벤트 로그입니다.")
    st.divider()
    
    with st.spinner("OpenSearch에서 로우 데이터를 불러오는 중..."):
        report = provider.get_detection_report(event_id)
        
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
    Provider를 통해 수동 심사 액션(Block/Pass)을 처리합니다.
    Mock 모드에서는 세션 상태만 업데이트, Production에서는 실제 API 호출.
    """
    provider = get_provider()
    success = provider.update_event_status(event_id, action)
    
    if success:
        print(f"[SUCCESS] Event {event_id} status updated to {action}.")
    else:
        print(f"[FAIL] Event {event_id} status update failed.")

def handle_review_action(event_id, action):
    """Button click callback handler."""
    execute_review_api_call(event_id, action)
    action_kor = "차단" if action == "Blocked" else "패스"
    st.toast(f"✅ **{event_id}** 건에 대한 수동 **{action_kor}** 처리가 완료되었습니다.", icon="🚨" if action == "Blocked" else "✅")

def render_review():
    provider = get_provider()
    
    render_header("MANUAL REVIEW")
    st.header("고위험 계정 수동 검토")
    st.write("실시간 AI 탐지로 적발된 이력 중 추가 확인이 필요한 건(Pending/Warning)에 대해 수동 검토를 진행합니다.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Provider에서 글로벌 히스토리 데이터 가져오기
    df = provider.get_enriched_history()
    
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
        selected_dates = st.multiselect("📅 날짜", available_dates, default=available_dates)
    with filter_col2:
        selected_games = st.multiselect("⚾ 대상 경기", available_games, default=available_games)
    with filter_col3:
        selected_status = st.multiselect("🚥 심사 상태", ["Pending", "Warning", "Blocked", "Passed"], default=["Pending", "Warning"])

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. 데이터프레임 필터링 적용
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
            
            # Action Buttons Row
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
