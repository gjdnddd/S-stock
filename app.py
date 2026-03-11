import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Stock Analysis", layout="wide")

# CSS: 탭 가로 스크롤 강제 활성화 및 가독성 설정
st.markdown("""
<style>
    /* 1. 탭 라인 가로 스크롤 및 잘림 방지 */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        display: flex !important;
        flex-direction: row !important;
        overflow-x: auto !important; /* 가로 스크롤 활성화 */
        overflow-y: hidden !important;
        white-space: nowrap !important;
        scrollbar-width: thin; /* 파이어폭스용 스크롤바 */
        padding-bottom: 5px;
    }
    
    /* 크롬/사파리용 스크롤바 디자인 (살짝 보이게 설정) */
    div[data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar {
        height: 4px;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
        background-color: #ccc;
        border-radius: 10px;
    }

    /* 2. 본문 내용 줄바꿈 및 박스 설정 */
    .content-box {
        white-space: pre-wrap; 
        word-break: break-all;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        line-height: 1.6;
        border: 1px solid #eee;
    }
    
    /* 3. 탭 텍스트 강조 */
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

                # 7개의 탭 구성
                tabs = st.tabs(["📰 기사", "🎯 테마", "🥇 대장이력", "💡 키워드요약", "🌐 전체테마", "📝 기사본문", "📈 K스윙"])

                with tabs[0]: # 기사
                    st.markdown(f'<div class="content-box">{row.get("기사", "내용 없음")}</div>', unsafe_allow_html=True)

                with tabs[1]: # 테마 (제목 삭제, 첫 줄부터 노출)
                    theme_content = row.get('코어테마', '내용 없음')
                    st.markdown(f'<div class="content-box">{theme_content}</div>', unsafe_allow_html=True)

                with tabs[2]: # 대장이력
                    st.markdown(f'<div class="content-box">{row.get("대장이력", "정보 없음")}</div>', unsafe_allow_html=True)

                with tabs[3]: # 키워드요약
                    st.success(row.get("키워드요약", "내용 없음"))

                with tabs[4]: # 전체테마
                    st.markdown(f'<div class="content-box">{row.get("전체테마", "내용 없음")}</div>', unsafe_allow_html=True)

                with tabs[5]: # 기사본문
                    st.markdown(f'<div class="content-box">{row.get("더 긴 설명", "내용 없음")}</div>', unsafe_allow_html=True)
                    
                with tabs[6]: # K스윙
                    st.markdown(f'<div class="content-box">{row.get("K스윙 정리", "정보 없음")}</div>', unsafe_allow_html=True)
            else:
                st.warning("검색 결과가 없습니다.")
                
        st.sidebar.success("✅ 데이터 연결됨")
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.error(f"'{FILE_NAME}' 파일을 찾을 수 없습니다.")
