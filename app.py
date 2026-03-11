import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Stock Analysis", layout="wide")

# CSS: 줄바꿈 유지 및 탭 디자인 설정
st.markdown("""
<style>
    .content-box {
        white-space: pre-wrap; /* 엑셀의 줄바꿈 유지 */
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
            # 모든 데이터를 문자열로 로드하여 에러 방지
            return pd.read_excel(FILE_NAME).astype(str)
        
        df = load_data()
        search_col = '종목명' if '종목명' in df.columns else df.columns[0]
        
        query = st.text_input(f"{search_col}을 입력하세요", placeholder="예: 삼성전자")

        if query and query != "nan":
            # 검색 로직 (대소문자 구분 없이 포함된 단어 찾기)
            res = df[df[search_col].str.contains(query, na=False, case=False)]
            if not res.empty:
                row = res.iloc[0]
                st.divider()
                st.subheader(f"🔍 {row[search_col]} 상세 분석")

                # 요청하신 순서대로 탭 구성
                tabs = st.tabs(["📰 기사", "🎯 테마", "🥇 대장이력", "💡 키워드요약", "🌐 전체테마", "📝 기사본문", "📈 K스윙"])

                with tabs[0]: # 기사
                    st.markdown(f'<div class="content-box">{row.get("기사", "내용 없음")}</div>', unsafe_allow_html=True)

                with tabs[1]: # 테마 (코어테마 중심)
                    st.info(f"**코어테마:** {row.get('코어테마', '없음')}")

                with tabs[2]: # 대장이력
                    st.markdown(f'<div class="content-box">{row.get("대장이력", "정보 없음")}</div>', unsafe_allow_html=True)

                with tabs[3]: # 키워드요약
                    st.success(row.get("키워드요약", "내용 없음"))

                with tabs[4]: # 전체테마
                    st.markdown(f'<div class="content-box">{row.get("전체테마", "내용 없음")}</div>', unsafe_allow_html=True)

                with tabs[5]: # 기사본문 (더 긴 설명)
                    st.markdown(f'<div class="content-box">{row.get("더 긴 설명", "내용 없음")}</div>', unsafe_allow_html=True)
                    
                with tabs[6]: # K스윙
                    st.markdown(f'<div class="content-box">{row.get("K스윙 정리", "정보 없음")}</div>', unsafe_allow_html=True)
            else:
                st.warning("검색 결과가 없습니다.")
                
        st.sidebar.success("✅ 데이터 연결됨")
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.error(f"'{FILE_NAME}' 파일을 찾을 수 없습니다. GitHub에 'data.xlsx' 파일을 올려주세요.")
