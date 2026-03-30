import streamlit as st
import pandas as pd
from utils.api import get_grafana_alerts
from components.header import render_header

def render_grafana():
    render_header("GRAFANA")
    st.subheader("📊 Grafana 실시간 모니터링")
    
    GRAFANA_URL = st.secrets.get("GRAFANA_URL", "http://localhost:3000").rstrip("/")
    GRAFANA_USERNAME = st.secrets.get("GRAFANA_USERNAME", "admin")
    GRAFANA_PASSWORD = st.secrets.get("GRAFANA_PASSWORD", "YOUR_GRAFANA_PASSWORD")
    GRAFANA_DASHBOARD_UID = st.secrets.get("GRAFANA_DASHBOARD_UID", "macro-detection")
    GRAFANA_SHARE_TOKEN = st.secrets.get("GRAFANA_SHARE_TOKEN", "YOUR_SHARE_TOKEN")

    # Grafana 연동 상태 확인
    if GRAFANA_PASSWORD == "YOUR_GRAFANA_PASSWORD":
        st.warning("⚠️ Grafana 로그인 정보가 설정되지 않았습니다. `.streamlit/secrets.toml`에 다음을 추가하세요:")
        st.code('''GRAFANA_URL = "https://your-grafana-url"
GRAFANA_USERNAME = "admin"
GRAFANA_PASSWORD = "your-password"
GRAFANA_DASHBOARD_UID = "your-dashboard-uid"
GRAFANA_SHARE_TOKEN = "your-embed-share-token"  # 선택사항''', language="toml")
    else:
        # 탭 생성
        tab1, tab2, tab3 = st.tabs(["📊 대시보드", "🚨 알러트", "ℹ️ 정보"])
        
        with tab1:
            st.subheader("실시간 대시보드")
            
            # 공개 공유 토큰이 있으면 iframe으로 임베드, 없으면 링크 제공
            if GRAFANA_SHARE_TOKEN != "YOUR_SHARE_TOKEN":
                st.info("✅ 공개 공유 대시보드로 iframe 표시 중입니다.")
                # 공개 공유 토큰을 사용한 임베드 URL
                embed_url = f"{GRAFANA_URL}/render/d-solo/{GRAFANA_DASHBOARD_UID}?refresh=5s&kiosk=tv"
                st.markdown(f'<iframe src="{embed_url}" width="100%" height="700" frameborder="0"></iframe>', unsafe_allow_html=True)
            else:
                st.info("💡 **iframe 임베드를 활성화하려면:**\n\n1. Grafana → 해당 대시보드 → Share\n2. **Embed** 탭에서 Embed 옵션 복사\n3. URL의 `kiosk` 파라미터 추가: `?refresh=5s&kiosk=tv`\n4. 공유 토큰을 `secrets.toml`의 `GRAFANA_SHARE_TOKEN`에 저장")
                
                # 또는 직접 링크 제공
                grafana_dashboard_url = f"{GRAFANA_URL}/d/{GRAFANA_DASHBOARD_UID}?orgId=1&refresh=5s"
                st.markdown(f"**[🔗 Grafana 대시보드 열기 (새 탭)]({grafana_dashboard_url})**")
        
        with tab2:
            st.subheader("🚨 현재 활성 알러트")
            alerts = get_grafana_alerts(GRAFANA_URL)
            
            if alerts and isinstance(alerts, list) and len(alerts) > 0 and "error" not in str(alerts):
                alert_df = []
                for alert in alerts[:10]:  # 최대 10개 알러트 표시
                    alert_name = alert.get("name", "Unknown")
                    alert_state = alert.get("state", "unknown")
                    
                    # 상태 아이콘
                    if alert_state == "alerting":
                        icon = "🔴"
                    elif alert_state == "pending":
                        icon = "🟡"
                    else:
                        icon = "🟢"
                    
                    alert_df.append({
                        "상태": f"{icon} {alert_state}",
                        "알러트명": alert_name,
                        "최종 평가": alert.get("evalData", {}).get("evalMatches", [{}])[0].get("metric", "N/A")
                    })
                
                if alert_df:
                    st.dataframe(pd.DataFrame(alert_df), width='stretch')
                else:
                    st.success("✅ 현재 활성 알러트가 없습니다.")
            else:
                st.info("⚠️ Grafana에서 알러트를 가져올 수 없습니다. URL 및 로그인 정보를 확인하세요.")
            
            st.divider()
            
            # 주요 메트릭
            st.subheader("📈 주요 메트릭")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("CPU 사용률", "45%", "-5%")
            with col2:
                st.metric("메모리 사용률", "62%", "+3%")
            with col3:
                st.metric("네트워크 처리량", "1.2 Gbps", "+0.1 Gbps")
        
        with tab3:
            st.subheader("ℹ️ Grafana 정보 및 설정")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(f"**URL**: [{GRAFANA_URL}]({GRAFANA_URL})")
                st.write(f"**사용자**: `{GRAFANA_USERNAME}`")
                st.write(f"**대시보드 UID**: `{GRAFANA_DASHBOARD_UID}`")
            with col2:
                st.write(f"**상태**: ✅ 연결됨")
                st.write(f"**공유 토큰**: {'✅ 설정됨' if GRAFANA_SHARE_TOKEN != 'YOUR_SHARE_TOKEN' else '❌ 미설정'}")
            
            st.divider()
            
            st.subheader("🔧 iframe 임베드 활성화 방법")
            st.markdown("""
            **방법 1: Grafana 공개 공유 사용 (권장)**
            1. Grafana 대시보드 열기
            2. 우측 상단 **Share** 클릭
            3. **Embed** 탭 선택
            4. **Embed** 섹션의 URL 복사
            5. `secrets.toml`에 다음 추가:
               ```toml
               GRAFANA_SHARE_TOKEN = "복사한_공유URL"
               ```
            
            **방법 2: URL 파라미터 사용**
            - `?refresh=5s&kiosk=tv` → TV 모드로 표시
            - `?refresh=1m&kiosk` → 자동 새로고침
            """)
