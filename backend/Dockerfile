# 1. 파이썬 3.11 슬림 버전
FROM python:3.11-slim

# 2. 컨테이너 내부 작업 디렉토리
WORKDIR /app

# 3. 의존성 설치 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY . .

# 5. 포트 개방
EXPOSE 8000

# 6. PYTHONPATH를 설정하여 app 패키지를 찾을 수 있게 함
ENV PYTHONPATH=/app

# 7. 실행 명령어 (중요: app.main:app 으로 경로 지정)
# --host 0.0.0.0 은 컨테이너 외부(AWS 등)에서 접속하기 위해 필수입니다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]