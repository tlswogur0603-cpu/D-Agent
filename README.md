# D-Agent

FastAPI + Docker + AWS EC2 + Gemini AI 기반 **보안 로그 분석 서비스**입니다.  
보안/운영 로그를 입력하면 Gemini를 활용해 이상 징후와 원인/대응 방안을 요약해, 운영자가 빠르게 트리아지할 수 있도록 돕습니다.

### 핵심 링크

- **API 문서(Swagger)**: `http://localhost:8000/docs`
- **헬스/안내 엔드포인트**: `GET /`
- **로그 분석 API**: `POST /api/v1/agent/analyze`

---

### Current Status

- **Supabase(DB) 연동을 진행 중**입니다. 현재는 분석 요청/응답이 API 호출 단위로 처리되며, 다음 단계로 분석 히스토리를 DB에 자동 저장하는 방향으로 확장하고 있습니다.

---

### 시스템 아키텍처

```mermaid
flowchart LR
  U[사용자/클라이언트] -->|HTTP| EC2[AWS EC2\nFastAPI (Docker)]
  EC2 -->|LLM 요청| G[Gemini AI]
  EC2 -->|분석 히스토리 저장/조회| DB[Supabase\nPostgreSQL]
  EC2 -->|Swagger| DOCS[/docs]
```

---

### 주요 기능

- **Gemini 기반 로그 분석**
  - 로그를 입력받아 보안 관점의 이벤트 요약, 의심 포인트, 조치 권고를 생성
- **표준화된 API 제공(FastAPI)**
  - Swagger(`/docs`)로 호출 스펙을 즉시 확인 가능
- **컨테이너 기반 배포(Docker / Docker Compose)**
  - 로컬 개발/테스트 및 EC2 배포에 동일한 런타임 재현
- **친절한 기본 응답**
  - `GET /` 요청 시 프로젝트 정보/상태/문서 링크 및 주요 API 경로 안내
  - 정의되지 않은 경로 접근 시 전역 404 핸들러가 요청 경로와 `/docs`를 안내

---

### 기술 스택(선정 이유 포함)

- **FastAPI**: 타입 기반 스키마/Swagger 자동 문서화로 API 개발·검증 속도 향상
- **Uvicorn(ASGI)**: 비동기 처리에 적합한 경량 서버로 배포 단순화
- **Docker / Docker Compose**: 로컬과 서버 환경을 동일하게 맞춰 재현성/운영 안정성 확보
- **AWS EC2**: 초기 단계에서 비용/구성 복잡도를 낮추면서도 확장 가능한 표준 런타임 제공
- **Gemini AI**: 보안 로그 요약/근거/대응 권고 생성에 적합한 LLM 활용
- **Supabase(PostgreSQL)**: 분석 히스토리 저장 및 조회 기능 확장을 위한 관리형 DB 선택(연동 진행 중)

---

### 설치 및 실행

#### 1) 사전 준비물

- Python 3.11+
- (권장) Docker Desktop
- Gemini API Key

#### 2) 환경 변수 설정

`backend/.env` 파일을 준비합니다.

- **필수**
  - `GEMINI_API_KEY`: Gemini API 키
- **선택**
  - `PROJECT_NAME`: 기본값 `D-Agent`
  - `DEBUG`: `True/False`

예시:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
PROJECT_NAME=D-Agent
DEBUG=True
```

#### 3) Docker Compose로 실행(권장)

프로젝트 루트에서 실행합니다.

```bash
docker compose up --build
```

실행 후 다음에서 확인할 수 있습니다.

- `GET http://localhost:8000/`
- `http://localhost:8000/docs`

#### 4) 로컬(Python)로 실행

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### API 사용 예시

#### 로그 분석

`POST /api/v1/agent/analyze`

요청 바디(개념 예시):

```json
{
  "logs": "여기에 분석할 로그 문자열을 전달합니다"
}
```

정확한 스키마/응답은 Swagger(` /docs `)에서 확인해주세요.

---

### 배포(AWS EC2) 가이드(요약)

운영 환경에서는 **EC2에서 Docker로 백엔드 컨테이너를 실행**하는 구성을 기준으로 합니다.

#### 1) 환경 변수 준비

운영 서버에는 소스에 키를 포함하지 않고, 환경 변수로만 주입합니다(권장: 시크릿 매니저/동등 개념으로 중앙 관리).

필수 예시:

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
export PROJECT_NAME="D-Agent"
export DEBUG="False"
```

#### 2) Docker 이미지 빌드 및 실행(예시)

```bash
cd backend
docker build -t d-agent-backend:latest .

docker run -d --name d-agent-backend \
  -p 8000:8000 \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  -e PROJECT_NAME="$PROJECT_NAME" \
  -e DEBUG="$DEBUG" \
  --restart always \
  d-agent-backend:latest
```

#### 3) 보안 그룹(Security Group) 권장 설정

- 인바운드 `8000/tcp`는 **허용 IP를 최소화**하여 운영(개발용 전체 오픈 지양)
- 가능하면 리버스 프록시/HTTPS 종단(Nginx 등)과 함께 운영(추후 확장 포인트)

---

### 디렉터리 구조(요약)

- `backend/`: FastAPI 서버 및 에이전트 로직
- `frontend/`: 프론트엔드(UI)
- `docs/`: 아키텍처/기획 등 프로젝트 문서

---

### 라이선스 / 참고

내부/개인 프로젝트 성격에 맞게 사용 정책을 정해 운영하세요.

