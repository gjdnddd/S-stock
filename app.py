import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Stock Analysis", layout="wide")

# CSS: 탭 가로 스크롤 시각화 및 강제 활성화
st.markdown("""
<style>
    /* 1. 탭 리스트 가로 스크롤 강제 및 디자인 */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        display: flex !important;
        overflow-x: auto !important; /* 가로 스크롤 허용 */
        white-space: nowrap !important;
        padding-bottom: 10px !important; /* 스크롤바 공간 확보 */
    }

    /* 2. 스크롤바를 항상 보이게 설정 (크롬, 사파리 등) */
    div[data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar {
        height: 8px !important; /* 스크롤바 두께 */
        display: block !important;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
        border-radius: 10px;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
        background: #888 !important; /* 스크롤바 색상 (진하게) */
        border-radius: 10px;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar-thumb:hover {
        background: #555 !important;
    }

    /* 3. 본문 스타일 */
    .content-box {
        white-space: pre-wrap; 
        word-break: break-all;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        line-height: 1.6;
        border: 1px solid #eee;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px; 
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 종목 분석 데이터 조회기")

FILE_NAME = "data.xlsx"

if os.path.exists(FILE_NAME):
    try:
        @st.cache_data
        def load_data():
            return pd.read_excel(FILE_NAME).astype(str)
        
        df = load_data()
        search_col = '종목명' if '종목명' in df.columns else df.columns[0]
        
        query = st.text_input(f"{search_col}을 입력하세요", placeholder="예: 한미반도체")

        if query and query != "nan":
            res = df[df[search_col].str.contains(query, na=False, case=False)]
            if not res.empty:
                row = res.iloc[0]
                st.divider()
                st.subheader(f"🔍 {row[search_col]} 상세 분석")

                # 탭 구성
                tabs = st.tabs(["📰 기사", "🎯 테마", "🥇 대장이력", "💡 키워드요약", "🌐 전체테마", "📝 기사본문", "📈 K스윙"])

                with tabs[0]:
                    st.markdown(f'<div class="content-box">{row.get("기사", "내용 없음")}</div>', unsafe_allow_html=True)
                with tabs[1]:
                    st.markdown(f'<div class="content-box">{row.get("코어테마", "내용 없음")}</div>', unsafe_allow_html=True)
                with tabs[2]:
                    st.markdown(f'<div class="content-box">{row.get("대장이력", "정보 없음")}</div>', unsafe_allow_html=True)
                with tabs[3]:
                    st.success(row.get("키워드요약", "내용 없음"))
                with tabs[4]:
                    st.markdown(f'<div class="content-box">{row.get("전체테마", "내용 없음")}</div>', unsafe_allow_html=True)
                with tabs[5]:
                    st.markdown(f'<div class="content-box">{row.get("더 긴 설명", "내용 없음")}</div>', unsafe_allow_html=True)
                with tabs[6]:
                    st.markdown(f'<div class="content-box">{row.get("K스윙 정리", "정보 없음")}</div>', unsafe_allow_html=True)
            else:
                st.warning("검색 결과가 없습니다.")
        st.sidebar.success("✅ 데이터 연결됨")
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.error(f"'{FILE_NAME}' 파일을 찾을 수 없습니다.")
