import streamlit as st
import streamlit.components.v1 as components

def inject_custom_css():
    st.markdown(
        """
        <style>
        .stApp { background-color: #f4f7f6 !important; color: #1f2937 !important; }
        .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label, .stMarkdown { color: #1f2937 !important; }
        .stApp [data-testid="stForm"] label, .stApp [data-testid="stForm"] div { color: #1f2937 !important; }

        .block-container { padding-top: 3rem !important; padding-bottom: 2rem !important; max-width: 95% !important; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: none !important;
            box-shadow: 2px 0 15px rgba(0,0,0,0.03) !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] {
            padding: 12px 16px !important;
            border-radius: 8px !important;
            margin-bottom: 5px !important;
            background-color: transparent;
            transition: all 0.2s ease;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:hover { background-color: #f0f2f5; }
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] {
            background-color: #00c292 !important; /* Active Green */
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] p {
            color: white !important; font-weight: 600 !important; font-size: 14px !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] div[data-baseweb="radio"] div:first-child { display: none !important; }
        [data-testid="stSidebar"] .stRadio > label { display: none !important; }

        /* Custom Top Header */
        .custom-top-header {
            display: flex; justify-content: space-between; align-items: center;
            background-color: transparent; padding: 0 0 20px 0; margin-bottom: 20px;
        }
        .top-left { display: flex; align-items: center; gap: 20px; font-weight: bold; color: #888; font-size: 14px; letter-spacing: 1px; }
        .top-left span.active { color: #00c292; }
        .top-right { display: flex; align-items: center; gap: 20px; }
        .search-bar { background: white; padding: 10px 20px; border-radius: 20px; border: none; font-size: 13px; color: #aaa; width: 250px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
        .icons-group { display: flex; gap: 15px; font-size: 18px; color: #666; cursor: pointer; }
        .user-profile { display: flex; align-items: center; gap: 10px; }
        .user-avatar { width: 40px; height: 40px; border-radius: 50%; background-color: #e2e8f0; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .user-info { display: flex; flex-direction: column; }
        .user-name { font-size: 14px; font-weight: bold; color: #333; }
        .user-role { font-size: 12px; color: #888; }
        
        /* White Box Component Styling (targeting column containers) */
        div[data-testid="column"] > div {
            background-color: #ffffff !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
        }

        # Native Streamlit border container override (for charts box)
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #ffffff !important;
            border-radius: 12px !important;
            border: none !important;
        }

        /* Top Metrics Custom Dashboard CSS */
        .metric-card-container { display: flex; justify-content: space-between; gap: 20px; margin-bottom: 25px; }
        .m-stat-card {
            flex: 1; padding: 24px; border-radius: 12px; background-color: #181b21; /* Dark aesthetic from image */
            box-shadow: 0 4px 15px rgba(0,0,0,0.06); display: flex; flex-direction: column; gap: 8px; text-align: left;
        }
        .stApp .m-stat-title { font-size: 14px; font-weight: 600; color: #9ca3af !important; letter-spacing: -0.3px; }
        .stApp .m-stat-value { font-size: 32px; font-weight: 700; color: #ffffff !important; letter-spacing: -0.5px; }
        .stApp .m-stat-unit { font-size: 20px; font-weight: 500; margin-left: 2px; color: #ffffff !important; }
        .m-stat-badge {
            display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 20px;
            font-size: 13px; font-weight: 600; width: fit-content; margin-top: 4px;
        }
        .badge-up { background-color: rgba(16, 185, 129, 0.15); color: #34d399; }
        .badge-down { background-color: rgba(239, 68, 68, 0.15); color: #f87171; }

        /* Ongoing Projects UI */
        .op-card { background: #fdfdfd; border: 1px solid #efefef; border-radius: 10px; padding: 15px; margin-bottom: 15px; display: flex; flex-direction: column; border-left: 5px solid #2196F3; box-shadow: 0 2px 5px rgba(0,0,0,0.01); }
        .op-card.sys { border-left-color: #ccc; background: #fafafa; }
        .op-card.assist { border-left-color: #4CAF50; background: #f8fbf8; }
        .op-card .op-role { font-size: 12px; font-weight: bold; color: #555; margin-bottom: 5px; text-transform: uppercase; }
        .op-card .op-msg { font-size: 14px; color: #444; line-height: 1.5; }
        
        .section-title { font-size: 18px; font-weight: 700; margin-bottom: 20px; color: #2c3e50; }
        </style>
        """,
        unsafe_allow_html=True,
    )
