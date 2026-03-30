import sqlite3
import pandas as pd
import streamlit as st

def init_db():
    conn = sqlite3.connect('macro_history.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY,
                        접속시간 TEXT,
                        접속IP TEXT,
                        탐지유형 TEXT
                    )''')
    # 샘플 데이터 삽입 (실제로는 API나 다른 소스에서)
    sample_data = [
        ("10:23:32", "203.242.89.166", "동적 행위분석"),
        ("10:23:31", "218.234.23.186", "정적 통계분석"),
        ("10:23:30", "112.111.22.33", "LLM 심층분석")
    ]
    conn.executemany("INSERT OR IGNORE INTO history (접속시간, 접속IP, 탐지유형) VALUES (?, ?, ?)", sample_data)
    conn.commit()
    conn.close()

def load_history_from_db():
    conn = sqlite3.connect('macro_history.db')  # DB 파일
    df = pd.read_sql_query("SELECT * FROM history", conn)
    conn.close()
    return df

def get_enriched_history():
    """
    DB에서 가져온 이력 데이터를 대시보드 구조에 맞게 확장하여 반환합니다.
    수동 심사 등을 통해 변경된 상태(Action Override)를 보존하기 위해 세션 스테이트를 캐시로 사용합니다.
    """
    if "enriched_history" not in st.session_state:
        df_history = load_history_from_db()
        if df_history.empty:
            return df_history
            
        # 50개 데이터로 빵빵하게 복제 (Mocking)
        df_expanded = pd.concat([df_history] * 17, ignore_index=True).head(50)
        
        df_display = df_expanded.copy()
        df_display["Event ID"] = ["#VZ" + str(1000 + i) for i in range(len(df_display))]
        target_urls = ["/login", "/checkout", "/event", "/signup", "/home"]
        df_display["Target URL"] = [target_urls[i % len(target_urls)] for i in range(len(df_display))]
        
        # MOCK Data: 최초 상태
        statuses = ["Blocked", "Pending", "Warning", "Passed"]
        df_display["Status"] = [statuses[i % len(statuses)] for i in range(len(df_display))]
        
        risk_scores = [94, 72, 88, 61, 45, 99]
        df_display["Risk Score"] = [risk_scores[i % len(risk_scores)] for i in range(len(df_display))]
        
        # 날짜 랜덤 부여 (오늘 / 어제)
        from datetime import datetime, timedelta
        import random
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        dates_pool = [today, today, today, yesterday, yesterday] # 60% 오늘, 40% 어제
        df_display["접속일자"] = [random.choice(dates_pool) for _ in range(len(df_display))]
        
        # 경기 ID 및 타이틀 맵핑
        baseball_games = {
            1: "2026 KBO 개막전 LG vs 삼성",
            2: "2026 KBO 정규시즌 KIA vs 한화",
            3: "2026 KBO 한국시리즈 7차전",
            4: "2026 KBO 올스타전 나눔 vs 드림"
        }
        game_ids_mock = [1, 1, 3, 2, 4, 1, 2]
        df_display["Game_ID"] = [game_ids_mock[i % len(game_ids_mock)] for i in range(len(df_display))]
        df_display["대상 경기"] = df_display["Game_ID"].map(lambda x: baseball_games.get(x, "알 수 없는 경기"))
        
        # 컬럼 순서 조정
        df_display = df_display[["Event ID", "접속일자", "접속시간", "대상 경기", "접속IP", "Target URL", "탐지유형", "Status", "Risk Score"]]
        
        st.session_state.enriched_history = df_display
        
    return st.session_state.enriched_history

def update_override_status(event_id, new_status):
    """
    세션에 저장된 최근 탐지 리스트의 특정 Event ID 상태를 업데이트합니다.
    """
    if "enriched_history" in st.session_state:
        df = st.session_state.enriched_history
        # 조건에 맞는 해당 row의 Status 컬럼 값을 업데이트
        df.loc[df["Event ID"] == event_id, "Status"] = new_status
        st.session_state.enriched_history = df
