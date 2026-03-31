"""
앱 환경 모드(Mock / Production) 중앙 설정 모듈.
app_config.toml 파일에서 모드를 읽어옵니다.
"""
import tomllib
import os
import streamlit as st

# ─────────────────────────────────────────────
# 모드 상수
# ─────────────────────────────────────────────
MODE_MOCK = "mock"
MODE_PRODUCTION = "production"

VALID_MODES = {MODE_MOCK, MODE_PRODUCTION}

# ─────────────────────────────────────────────
# app_config.toml 로딩
# ─────────────────────────────────────────────
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app_config.toml")

def _load_app_config() -> dict:
    """app_config.toml을 읽어 딕셔너리로 반환합니다."""
    try:
        with open(_CONFIG_PATH, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {}


def get_app_mode() -> str:
    """현재 앱 모드를 반환합니다. 기본값은 'mock'."""
    config = _load_app_config()
    mode = config.get("app", {}).get("mode", MODE_MOCK).lower().strip()
    if mode not in VALID_MODES:
        return MODE_MOCK
    return mode


def is_mock_mode() -> bool:
    return get_app_mode() == MODE_MOCK


def is_production_mode() -> bool:
    return get_app_mode() == MODE_PRODUCTION


# ─────────────────────────────────────────────
# Production 전용 설정 헬퍼 (secrets.toml에서 읽음)
# ─────────────────────────────────────────────
def get_api_base_url() -> str:
    """백엔드 API 베이스 URL을 반환합니다."""
    return st.secrets.get("API_BASE_URL", "https://api.go-ti.shop").rstrip("/")


def get_opensearch_config() -> dict:
    """OpenSearch 연결 정보를 딕셔너리로 반환합니다."""
    return {
        "host": st.secrets.get("OPENSEARCH_HOST", "https://search-goti.ap-northeast-2.es.amazonaws.com"),
        "index": st.secrets.get("OPENSEARCH_INDEX", "macro-events-*"),
        "username": st.secrets.get("OPENSEARCH_USERNAME", ""),
        "password": st.secrets.get("OPENSEARCH_PASSWORD", ""),
    }
