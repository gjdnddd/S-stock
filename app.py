import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Stock Analysis", layout="wide")

# CSS: 가독성 향상
st.markdown("""<style>.result-box { white-space: pre-wrap; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; }</style>""", unsafe_allow_html=True)

st.title("📊 종목 분석 데이터 조회기")

# 파일 경로 설정 (깃허브에 올린 파일 이름과 동일해야 함)
FILE_NAME = "data.xlsx"

# 파일 존재 여부 확인 후 데이터 로드
if os.path.exists(FILE_NAME):
    try:
        # 데이터 불러오기 (캐싱 처리하여 속도 향상)
        @st.cache_data
        def load_data():
            return pd.read_excel(FILE_NAME)
        
        df = load_data()
        
        # 검색 기준 컬럼 찾기
        search_col = '종목명' if '종목명' in df.columns else df.columns[0]
        
        query = st.text_input(f"{search_col}을 입력하세요 (예: 지슨)")

        if query:
            res = df[df[search_col].astype(str).str.contains(query, na=False, case=False)]
            if not res.empty:
                row = res.iloc[0]
                st.subheader(f"🔍 {row[search_col]} 상세 결과")
                
                tabs = st.tabs(["📰 기사", "🎯 테마", "🥇 대장/K스윙", "📝 요약/본문"])
                
                with tabs[0]: st.text_area("관련 기사", value=str(row.get('기사', '내용 없음')), height=300)
                with tabs[1]: 
                    st.info(f"**코어테마:** {row.get('코어테마', '없음')}")
                    st.write(f"**전체테마:** {row.get('전체테마', '없음')}")
                with tabs[2]:
                    st.warning(f"**대장이력:** {row.get('대장이력', '없음')}")
                    st.success(f"**K스윙 정리:** {row.get('K스윙 정리', '없음')}")
                with tabs[3]:
                    st.write("**키워드 요약**")
                    st.markdown(f'<div class="result-box">{row.get("키워드요약", "없음")}</div>', unsafe_allow_html=True)
                    st.write("**기사 본문**")
                    st.markdown(f'<div class="result-box">{row.get("더 긴 설명", "내용 없음")}</div>', unsafe_allow_html=True)
            else:
                st.warning("검색 결과가 없습니다.")
                
        # 업데이트 방법 안내 (사이드바)
        st.sidebar.success("✅ 데이터 로드 완료")
        st.sidebar.info("💡 업데이트 방법: GitHub에서 'data.xlsx' 파일을 새 파일로 덮어쓰기(Overwrite) 하시면 됩니다.")

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.error(f"'{FILE_NAME}' 파일을 찾을 수 없습니다. GitHub에 파일을 업로드해 주세요.")
