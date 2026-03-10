import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="주식 분석 앱", layout="wide")

# 줄바꿈 처리를 위한 CSS 스타일 정의
st.markdown("""
    <style>
    .preserve-whitespace {
        white-space: pre-wrap;
        word-wrap: break-word;
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 종목 분석 데이터 조회기")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        
        # 상단 검색 바 및 버튼 레이아웃
        col1, col2 = st.columns([4, 1])
        with col1:
            search_query = st.text_input("분석할 종목명을 입력하세요", key="search_input")
        with col2:
            st.write(" ") # 수직 정렬용 공백
            search_button = st.button("🔍 검색하기", use_container_width=True)

        # 검색 실행 (엔터 또는 버튼 클릭 시)
        if search_query or search_button:
            result = df[df['종목명'].astype(str).str.contains(search_query, na=False)]

            if not result.empty:
                row = result.iloc[0]
                st.divider()
                st.subheader(f"🔍 {row['종목명']} 상세 분석")

                # 탭 구성 (요청 순서 유지)
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                    "📰 기사", "🎯 코어테마", "🌐 전체테마", "🥇 대장이력", "📝 키워드요약", "📄 기사본문", "📈 K스윙"
                ])

                # 공통 함수: 스크롤 vs 전체보기 전환 기능
                def display_content(title, content):
                    is_expand = st.checkbox(f"{title} 전체 펼쳐보기", key=f"check_{title}")
                    if is_expand:
                        # 클릭 한 번에 전체 내용 출력 (줄바꿈 보존)
                        st.markdown(f'<div class="preserve-whitespace">{content}</div>', unsafe_allow_html=True)
                    else:
                        # 기본 스크롤 박스
                        st.text_area(f"{title} (스크롤 가능)", value=str(content), height=250, disabled=True)

                with tab1: # 기사
                    display_content("기사", row['기사'])

                with tab2: # 코어테마 (줄바꿈 반영)
                    st.write("**🎯 코어테마 상세:**")
                    st.markdown(f'<div class="preserve-whitespace">{row["코어테마"]}</div>', unsafe_allow_html=True)

                with tab3: # 전체테마
                    st.markdown(f'<div class="preserve-whitespace">{row["전체테마"]}</div>', unsafe_allow_html=True)

                with tab4: # 대장이력 (줄바꿈 반영)
                    st.write("**🥇 대장이력 상세:**")
                    st.markdown(f'<div class="preserve-whitespace">{row["대장이력"]}</div>', unsafe_allow_html=True)

                with tab5: # 키워드요약
                    display_content("키워드요약", row['키워드요약'])

                with tab6: # 기사본문 (더 긴 설명)
                    display_content("기사본문", row['더 긴 설명'])

                with tab7: # K스윙
                    display_content("K스윙", row['K스윙'])
            else:
                st.warning("데이터를 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")