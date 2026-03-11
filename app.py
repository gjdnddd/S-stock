import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Stock Analysis", layout="wide")

# CSS: 줄바꿈 유지 및 박스 스타일 설정
st.markdown("""
<style>
    .content-box {
        white-space: pre-wrap; /* 엑셀의 줄바꿈(Enter)을 그대로 표시 */
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin-bottom: 20px;
        font-size: 16px;
        line-height: 1.6;
    }
    h3 { margin-top: 30px; color: #1f77b4; }
</style>
""", unsafe_allow_html=True)

st.title("📊 종목 분석 데이터 조회기")

FILE_NAME = "data.xlsx"

if os.path.exists(FILE_NAME):
    try:
        @st.cache_data
        def load_data():
            return pd.read_excel(FILE_NAME)
        
        df = load_data()
        search_col = '종목명' if '종목명' in df.columns else df.columns[0]
        
        query = st.text_input(f"{search_col}을 입력하세요 (예: 삼성전자)")

        if query:
            res = df[df[search_col].astype(str).str.contains(query, na=False, case=False)]
            if not res.empty:
                row = res.iloc[0]
                st.divider()
                st.header(f"🔍 {row[search_col]} 분석 결과")

                # 1. 기사 섹션 (아래로 쭉 나옴)
                st.subheader("📰 관련 기사")
                st.markdown(f'<div class="content-box">{row.get("기사", "내용 없음")}</div>', unsafe_allow_html=True)

                # 2. 테마 섹션
                st.subheader("🎯 테마 정보")
                st.info(f"**코어테마:** {row.get('코어테마', '없음')}")
                st.markdown(f'**전체테마:**\n{row.get("전체테마", "없음")}')

                # 3. 대장이력 및 K스윙 (분리 및 줄바꿈 유지)
                st.subheader("🥇 대장이력")
                st.markdown(f'<div class="content-box" style="border-left-color: #ffc107;">{row.get("대장이력", "정보 없음")}</div>', unsafe_allow_html=True)
                
                st.subheader("📈 K스윙 정리")
                st.markdown(f'<div class="content-box" style="border-left-color: #28a745;">{row.get("K스윙 정리", "정보 없음")}</div>', unsafe_allow_html=True)

                # 4. 키워드 요약 및 기사 본문 (따로 분리)
                st.subheader("💡 키워드 요약")
                st.success(row.get("키워드요약", "내용 없음"))

                st.subheader("📝 기사 본문")
                st.markdown(f'<div class="content-box" style="border-left-color: #6c757d;">{row.get("더 긴 설명", "본문 내용 없음")}</div>', unsafe_allow_html=True)
                
            else:
                st.warning("검색 결과가 없습니다.")
                
        st.sidebar.success("✅ 데이터 연결됨")
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.error(f"'{FILE_NAME}' 파일을 찾을 수 없습니다. GitHub에 업로드해 주세요.")
