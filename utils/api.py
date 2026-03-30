import streamlit as st
import requests
import base64
from openai import OpenAI

def get_solar_client():
    UPSTAGE_API_KEY = st.secrets.get("UPSTAGE_API_KEY", "YOUR_UPSTAGE_API_KEY")
    return OpenAI(api_key=UPSTAGE_API_KEY, base_url="https://api.upstage.ai/v1/solar")

def get_grafana_headers():
    """Grafana Basic Auth 헤더 생성"""
    username = st.secrets.get("GRAFANA_USERNAME", "admin")
    password = st.secrets.get("GRAFANA_PASSWORD", "YOUR_GRAFANA_PASSWORD")
    
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    return {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

def get_grafana_metrics(grafana_url, dashboard_uid):
    """Grafana에서 대시보드 정보 및 메트릭 가져오기"""
    try:
        headers = get_grafana_headers()
        response = requests.get(f"{grafana_url}/api/dashboards/uid/{dashboard_uid}", headers=headers, timeout=5, verify=True)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Grafana API 오류: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_grafana_alerts(grafana_url):
    """Grafana에서 현재 알러트 상태 가져오기"""
    try:
        headers = get_grafana_headers()
        response = requests.get(f"{grafana_url}/api/alerts", headers=headers, timeout=5, verify=True)
        
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        return [{"error": str(e)}]
