# 기술 요구사항 (Technical Requirements) — D-Agent

본 문서는 [`PRD.md`](./PRD.md)와 루트 [`README.md`](../README.md)의 제품·운영 요구를 바탕으로, **현재 저장소의 실제 구현**을 기준으로 기술 요구사항과 명세를 정리합니다. PRD의 To-Be 항목은 **구현 상태**를 구분해 기술합니다.

---

## 1. 문서 정보

| 항목 | 내용 |
|------|------|
| 대상 시스템 | D-Agent 백엔드(FastAPI) 및 향후 Supabase(PostgreSQL) 연동 |
| 기준 시점 | 저장소 코드 기준 (문서 작성 시점의 `backend/`, `frontend/`) |

---

## 2. 런타임 및 배포

| 요구사항 | 명세 | 구현 상태 |
|----------|------|-----------|
| Python | 3.11 (`backend/Dockerfile` 기준) | 적용 |
| ASGI 서버 | Uvicorn, `app.main:app`, `--host 0.0.0.0`, 포트 `8000` | 적용 |
| 컨테이너 | `backend/Dockerfile` 빌드, 루트 `docker-compose.yml`로 포트·환경 주입 | 적용 |
| 작업 디렉터리 / 모듈 경로 | 컨테이너 내 `WORKDIR /app`, `PYTHONPATH=/app`, 패키지 루트는 `app/` | 적용 |

**참고:** `backend/main.py`는 `FastAPI` 스텁(`/health`만 존재)이며, Docker 및 문서에서 안내하는 실행 진입점은 **`app.main:app`**(`backend/app/main.py`)입니다.

---

## 3. 환경 변수 및 설정

설정은 `backend/app/core/config.py`의 Pydantic `Settings`와 `python-dotenv`로 로드됩니다. `.env` 파일 경로는 **`backend/.env`**( `config.py` 기준 프로젝트 루트 = `backend/` )입니다.

| 변수 | 필수 | 설명 |
|------|------|------|
| `GEMINI_API_KEY` | 예 | Gemini API 호출에 사용 |
| `PROJECT_NAME` | 아니오 | 기본값 `D-Agent` |
| `DEBUG` | 아니오 | 기본값 `True` |

**Supabase 관련:** 현재 `Settings`에는 Supabase URL/키가 **정의되어 있지 않으며**, 애플리케이션 기동에도 필요하지 않습니다. DB 연동 시에는 예를 들어 아래와 같은 변수를 추가하는 방식이 일반적입니다(실제 키 이름은 도입 시 `Settings`와 일치시켜야 함).

- `SUPABASE_URL` — Supabase 프로젝트 URL  
- `SUPABASE_SERVICE_ROLE_KEY` — 서버 전용(비밀). 서버에서 RLS를 우회해 저장·관리 작업을 할 때 사용하는 패턴이 흔함  
- (대안) `SUPABASE_ANON_KEY` — 클라이언트/공개 API용. 서버에서 사용 시 **Row Level Security(RLS)** 설계 필수  

운영 시 PRD의 비기능 요구(시크릿 비하드코딩, Secrets Manager 등)를 함께 충족해야 합니다.

---

## 4. API 통신 방식

### 4.1 공통

| 항목 | 명세 |
|------|------|
| 프로토콜 | HTTP/HTTPS |
| 데이터 형식 | JSON (`Content-Type: application/json`) |
| API 문서 | OpenAPI(Swagger) UI — `GET /docs` |
| CORS | `app/main.py`에서 허용 Origin: `http://localhost:3000`, `http://127.0.0.1:3000`, `http://localhost:8000` |

### 4.2 엔드포인트 (현재 등록된 라우터 기준)

`app/main.py`에는 **`app.api.v1.agent`** 라우터만 `include_router` 되어 있습니다. `api/v1/logs.py`, `notify.py`는 모듈만 존재하고 **라우터 등록 및 엔드포인트 구현은 없음**(스텁).

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 프로젝트명, 상태, `/docs` 링크, 주요 API 경로 안내(JSON) |
| `POST` | `/api/v1/agent/analyze` | 로그 분석 요청·응답 |

### 4.3 `POST /api/v1/agent/analyze`

**요청 스키마** (`app/schemas/agent.py` — `LogAnalysisRequest`)

- `logs`: `string[]` — 분석할 로그를 **줄 단위 문자열 배열**로 전달 (빈 배열이면 400).

**응답 스키마** (`LogAnalysisResponse`)

- `error_summary`: `string`
- `risk_score`: `integer` — 1~10
- `detected_issues`: `string[]`
- `suggested_solutions`: `string[]`

**처리 흐름**

1. 라우터(`app/api/v1/agent.py`)가 `analyze_logs(request.logs)` 호출  
2. 오케스트레이터(`app/agents/orchestrator.py`)가 `google-generativeai`로 `gemini-2.5-flash` 호출, 응답을 JSON으로 파싱 후 Pydantic 검증  
3. 로그 전처리는 `app/agents/tools/log_tool.py` → `app/services/log_service.py`의 `get_filtered_logs` (ERROR 라인·타임스탬프·최근 10분 등 필터)

**에러 처리**

- 빈 `logs`: HTTP 400  
- 그 외 예외: HTTP 500 (일반 메시지; 세부는 로그에 의존)

동기 함수(`def`)로 처리되며, 현재 별도 타임아웃/재시도 미들웨어는 코드에 명시되어 있지 않습니다(PR에서는 향후 NFR).

---

## 5. Supabase(DB) 연동 — 현재 코드 vs 목표 명세

### 5.1 현재 구현 상태

| 항목 | 상태 |
|------|------|
| `supabase` 패키지 | `backend/requirements.txt`에 **선언됨** |
| DB 클라이언트 생성·쿼리 | **미구현** — `supabase`, `create_client`, PostgREST 직접 호출 등 **애플리케이션 코드에 없음** |
| 연결 정보 환경 변수 | `config.py` **미정의** |
| 분석 결과 영구 저장 | **없음** — 응답은 요청 단위로만 반환 |

즉, README/PRD에서 말하는 “Supabase 연동 진행 중”은 **의존성 준비 수준**이며, 저장 로직은 **추가 구현 대상**입니다.

### 5.2 목표 데이터 모델 (PRD 초안과의 정렬)

PRD §6.2에 기술된 필드는 향후 PostgreSQL(Supabase) 테이블 설계 시 기준으로 삼을 수 있습니다.

- `id` — UUID, PK  
- `log_hash` — 원문 로그 해시(SHA-256 등), 중복 방지·캐시 키  
- `risk_score` — 정규화 점수(예: 0~100; 현재 API는 1~10이므로 매핑 정책 필요)  
- `analysis_result` — JSONB (구조화된 분석 결과)  
- `created_at` — `timestamptz`  
- `source` — 입력 채널 (manual, api 등)  
- `model` — 모델 식별자/버전  
- `meta` — JSONB (요청 컨텍스트 등)  

Supabase에서는 일반적으로 **SQL 마이그레이션**으로 테이블을 만들고, 백엔드에서는 **`supabase` Python 클라이언트**로 `insert` / `select` 하거나, 필요 시 **Postgres 연결 문자열**로 SQLAlchemy/asyncpg 등을 사용할 수 있습니다. 프로젝트 정책에 맞게 하나를 표준으로 정하면 됩니다.

### 5.3 연동 시 기술 명세(권장 패턴)

아래는 `supabase-py`를 쓸 때의 일반적인 서버 측 패턴입니다(실제 도입 시 모듈 위치·이름은 통일 필요).

1. **연결**  
   - 환경 변수에서 `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` 로드  
   - `from supabase import create_client` 후 `create_client(url, key)` 한 번 생성해 앱 수명 주기 동안 재사용(또는 `lru_cache`/의존성 주입)

2. **데이터 저장**  
   - 분석 완료 후 `analysis_result`, `risk_score`, `log_hash`, `model`, `source`, `meta` 등을 dict로 구성  
   - `client.table("analysis_history").insert({...}).execute()` 형태(PostgREST) 또는 RPC/트랜잭션  

3. **보안**  
   - 서비스 롤 키는 **서버에만** 보관, Git/이미지에 포함 금지  
   - 공개 API용으로는 Anon 키 + RLS 정책(`app/core/security.py` 확장 여지) 검토  

4. **관측성**  
   - 저장 실패 시 분석 API 전체를 실패시킬지, “저장만 실패”로 로깅하고 분석 결과는 반환할지 **정책 결정** 필요  

---

## 6. 프론트엔드 (현재)

| 항목 | 상태 |
|------|------|
| 스택 | Next.js(App Router), `frontend/src/app/` |
| 백엔드 호출 | `page.tsx`는 플레이스홀더 문구만 있음 — **API 클라이언트·`fetch` 연동 미구현** |

향후 `localhost:8000` API를 호출할 때는 위 CORS 설정과 요청 본문 형식(`logs` 배열)을 맞추면 됩니다.

---

## 7. 비기능 요구(PR과 코드의 갭)

PRD §7(NFR) 중 일부는 **정책/향후 작업**으로 남아 있습니다.

- 시크릿: 코드 비하드코딩 — 현재는 env 기반(`GEMINI_API_KEY` 필수)  
- 민감정보 마스킹: `log_service`는 ERROR 추출·시간 필터 중심이며, **마스킹 룰은 미구현**  
- 구조화 로그·타임아웃/재시도: **명시적 구현 없음**  

---

## 8. 요약

- **API**: JSON 기반 FastAPI, 현재 핵심은 `POST /api/v1/agent/analyze`와 `GET /`, `GET /docs`.  
- **Supabase**: 의존성만 추가된 상태이며, **연결·저장 로직·환경 변수는 미구현**; 도입 시 PRD 필드와 서비스 롤/RLS 전략을 문서화한 뒤 `Settings`와 저장 서비스 계층을 추가하는 것이 요구사항에 부합합니다.
