import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 임베딩 모델 로드
encoder = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 식당 관련 질문과 답변 데이터
questions = [
    "포트폴리오 주제가 뭔가요?",
    "모델은 어떤 것을 썼나요?",
    "팀원 구성이 어떻게 되나요?",
    "평소 회의는 언제 하나요?",
    "역할 분담은 어떻게 했죠?",
    "프로젝트를 진행하면서 어려움은 없었나요?",
    "기대효과가 뭐죠?"
]

answers = [
    "실시간으로 피트니스 자세를 교정해주는 모델입니다.",
    "Yolo입니다..",
    "조장 서동현 팀원 이원석 경진우 노승욱입니다.",
    "수업 끝나고 21시까지 진행했습니다.",
    "바벨, 맨몸, 기구로 나누어 모델을 만들었습니다.",
    "데이터가 너무 커서 힘들었습니다.",
    "헬스를 잘 모르는 사람도 올바른 자세로 운동 할 수 있습니다."
]

# 질문 임베딩과 답변 데이터프레임 생성
question_embeddings = encoder.encode(questions)
df = pd.DataFrame({'question': questions, '챗봇': answers, 'embedding': list(question_embeddings)})

# 대화 이력을 저장하기 위한 Streamlit 상태 설정
if 'history' not in st.session_state:
    st.session_state.history = []

# 챗봇 함수 정의
def get_response(user_input):
    # 사용자 입력 임베딩
    embedding = encoder.encode(user_input)
    
    # 유사도 계산하여 가장 유사한 응답 찾기
    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer = df.loc[df['distance'].idxmax()]

    # 대화 이력에 추가
    st.session_state.history.append({"user": user_input, "bot": answer['챗봇']})

# Streamlit 인터페이스
st.title("최종 포트폴리오 챗봇")
st.write("포트폴리오에 대한 질문을 입력해보세요. 예: 주제가 뭔가요?")

user_input = st.text_input("user", "")

if st.button("Submit"):
    if user_input:
        get_response(user_input)
        user_input = ""  # 입력 초기화

# 대화 이력 표시
for message in st.session_state.history:
    st.write(f"**사용자**: {message['user']}")
    st.write(f"**챗봇**: {message['bot']}")