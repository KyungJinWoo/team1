import streamlit as st

# 제목 설정
st.title("비디오 사물 검출 앱")

# 파일 업로드
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

# 파일이 업로드되었는지 확인
if uploaded_file is not None:
    # 비디오 플레이어
    st.video(uploaded_file)
else:
    st.write("재생하고 싶은 비디오 파일을 업로드하세요.")
