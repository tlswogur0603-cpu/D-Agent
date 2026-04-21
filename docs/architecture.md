# 아키텍처 및 디렉터리 구조 — D-Agent

본 문서는 **현재 저장소의 실제 폴더·파일**을 기준으로 합니다. (개발 시 생성되는 `__pycache__` 등은 생략합니다.)

---

## 1. 저장소 최상위

```
D-Agent/
├── .gitignore
├── README.md
├── docker-compose.yml
├── backend/
├── docs/
└── frontend/
```

| 경로 | 역할 |
|------|------|
| `README.md` | 프로젝트 소개, 실행 방법, API 요약, 배포 개요 |
| `docker-compose.yml` | 백엔드 이미지 빌드, 포트 `8000`, `backend/.env` 주입, 소스 볼륨 마운트 |
| `docs/` | 기획·아키텍처·요구사항 문서 (`PRD.md`, `architecture.md`, `requirements.md` 등) |
| `backend/` | FastAPI 애플리케이션, Docker 빌드 컨텍스트 |
| `frontend/` | Next.js 기반 UI(현재 플레이스홀더 수준) |

---

## 2. backend/

```
backend/
├── .dockerignore
├── .env                 # 로컬/컨테이너 환경 변수 (Git에 커밋하지 않음)
├── Dockerfile
├── main.py              # 스텁 앱(/health) — 운영 진입점 아님
├── requirements.txt
├── app/
└── tests/
```

| 경로 | 역할 |
|------|------|
| `Dockerfile` | Python 3.11, 의존성 설치, `uvicorn app.main:app` 실행, `PYTHONPATH=/app` |
| `requirements.txt` | FastAPI, Uvicorn, google-generativeai, pydantic-settings, supabase(의존성만) 등 |
| `main.py` | 별도 최소 FastAPI 앱; Docker CMD는 **`app.main:app`** 사용 |
| `.dockerignore` | 이미지 빌드 시 제외 파일 |
| `app/` | 실제 API·에이전트·설정 패키지 (아래 §3) |
| `tests/` | 테스트 자리(`.gitkeep`); 시나리오 테스트는 추후 확장 |

---

## 3. backend/app/

```
backend/app/
├── main.py              # FastAPI 앱, CORS, 라우터 등록, /, 404 핸들러
├── agents/
│   ├── orchestrator.py  # Gemini 호출, LogAnalysisResponse 생성
│   └── tools/
│       ├── log_tool.py  # AI용 로그 전처리 진입
│       └── .gitkeep
├── api/
│   └── v1/
│       ├── agent.py     # POST .../analyze
│       ├── logs.py      # 스텁(라우터만 import)
│       └── notify.py    # 스텁(라우터만 import)
├── core/
│   ├── config.py        # 환경 변수, backend/.env 로드, Settings 싱글톤
│   └── security.py      # OAuth2 등 확장용(현재 최소)
├── schemas/
│   ├── agent.py         # LogAnalysisRequest/Response
│   ├── common.py        # 공통 스키마 확장용
│   └── log.py           # LogRead 등 구조화 로그 모델(향후 DB/API 연계용)
└── services/
    ├── log_service.py   # ERROR 라인 필터, 타임스탬프·최근 10분 등
    └── slack_service.py # 알림 연동 확장용(현재 최소)
```

| 경로 | 역할 |
|------|------|
| `main.py` | 앱 인스턴스 생성, CORS, `agent` 라우터를 `/api/v1/agent`에 마운트, 루트·404 응답 |
| `agents/orchestrator.py` | Gemini(`gemini-2.5-flash`)로 JSON 응답 강제, Pydantic 검증 |
| `agents/tools/log_tool.py` | `log_service.get_filtered_logs` 래퍼 |
| `api/v1/agent.py` | 분석 API 엔드포인트 구현 |
| `api/v1/logs.py`, `notify.py` | 향후 로그·알림 API용 자리 |
| `core/config.py` | `GEMINI_API_KEY` 필수 등 설정 |
| `schemas/agent.py` | API 요청/응답 계약 |
| `services/log_service.py` | 텍스트 로그에서 ERROR 컨텍스트 추출 등 순수 로직 |

---

## 4. frontend/

```
frontend/
├── package.json
├── package-lock.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── next-env.d.ts
├── public/
│   └── .gitkeep
└── src/
    ├── app/
    │   ├── globals.css      # Tailwind 전역 스타일
    │   ├── layout.tsx       # 루트 레이아웃(lang=ko)
    │   └── page.tsx         # 메인 페이지 엔트리
    ├── features/
    │   └── dashboard/
    │       ├── api.ts
    │       ├── hooks.ts
    │       ├── types.ts
    │       ├── container/
    │       │   └── DashboardContainer.tsx
    │       └── components/
    │           ├── HistoryList.tsx
    │           ├── ResultCard.tsx
    │           └── RiskScore.tsx
    ├── shared/
    │   ├── lib/
    │   │   └── axios.ts
    │   ├── hooks/
    │   │   └── .gitkeep
    │   └── ui/
    │       └── .gitkeep
    └── types/
        └── .gitkeep
```

| 경로 | 역할 |
|------|------|
| `src/app/` | Next.js App Router 페이지·레이아웃 |
| `src/app/globals.css` | Tailwind CSS 전역 스타일 진입점 |
| `src/features/` | 도메인(기능) 단위로 모듈을 분리하는 최상위 경로 |
| `src/features/*/api.ts` | API 호출 로직(네트워크 I/O)만 담당 |
| `src/features/*/hooks.ts` | 데이터 fetching/상태 관리(비즈니스 로직) 담당 |
| `src/features/*/components/` | 프레젠테이션(UI) 컴포넌트. props만 사용(비즈니스 로직/API 호출 금지) |
| `src/features/*/container/` | hooks와 UI를 연결(데이터 주입/이벤트 연결) |
| `src/shared/lib/` | 앱 전반에서 공유하는 클라이언트/유틸(API client 등) |
| `src/shared/ui/` | 전역 공유 UI 컴포넌트 확장용 디렉터리 |
| `src/shared/hooks/` | 전역 공유 hooks 확장용 디렉터리 |
| `src/types/` | 전역 타입 확장용 디렉터리 |
| `tailwind.config.js` | Tailwind CSS 설정 |
| `postcss.config.js` | Tailwind/PostCSS 플러그인 설정 |
| `next-env.d.ts` | Next.js 자동 생성 타입 선언 파일 (수정 금지) |

---

### 프론트엔드 아키텍처(구조 분리 원칙)

- **UI(프레젠테이션) 계층**: `features/*/components/`
  - props 기반 렌더링만 담당하며, 네트워크/상태/도메인 로직을 포함하지 않습니다.

- **비즈니스 로직(상태) 계층**: `features/*/hooks.ts`
  - 데이터 fetching, 로딩/에러 처리, 상태 관리를 담당합니다.

- **I/O(API) 계층**: `features/*/api.ts`
  - 백엔드와의 HTTP 통신만 담당하며, UI/상태 로직에 의존하지 않습니다.

- **연결(컨테이너) 계층**: `features/*/container/`
  - hooks에서 가져온 데이터를 UI 컴포넌트에 주입하고, UI 이벤트를 연결합니다.

---

> 참고:
> - 프론트엔드는 Next.js App Router 기반으로 동작합니다.
> - 현재 구조는 `dashboard` 기능을 중심으로 feature-first 아키텍처를 적용했습니다.
> - 공통 UI/훅은 `shared/` 디렉터리를 통해 확장 가능하도록 설계되어 있습니다.
> - `tsconfig.json`에 path alias가 없어 import는 상대 경로 기준으로 유지합니다.

## 5. docs/

```
docs/
├── PRD.md
├── architecture.md      # 본 문서
└── requirements.md      # 기술 요구사항·API·Supabase 명세
```

---

## 6. 런타임 관계(요약)

- **백엔드 진입점(Docker/문서 기준):** `uvicorn app.main:app` → `backend/app/main.py`  
- **LLM:** `app/agents/orchestrator.py`에서 Gemini API 사용  
- **DB(Supabase):** 의존성(`requirements.txt`)만 존재; 저장·연결 코드는 미구현 — 상세는 [`requirements.md`](./requirements.md) 참고  

이 구조는 기능 추가 시 `api/v1`에 라우터를 등록하고, 영속화는 `services/` 또는 전용 `repositories/` 계층을 두어 Supabase/Postgres와 연동하기 쉽게 나뉘어 있습니다.
