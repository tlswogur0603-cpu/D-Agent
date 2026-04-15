```python
backend/
├── app/
│   ├── api/                # API 엔드포인트 (라우터)
│   │   ├── v1/
│   │   │   ├── logs.py     # 로그 관련 API
│   │   │   ├── notify.py   # 알림(Slack 등) API
│   │   │   └── agent.py    # AI 에이전트 실행 API
│   ├── core/               # 프로젝트 공통 설정
│   │   ├── config.py       # 환경 변수 (API KEY 등)
│   │   └── security.py     # 인증/인가 및 RLS 정책 관련
│   ├── schemas/            # Pydantic 모델 (Data Validation)
│   │   ├── log.py
│   │   └── common.py       # 공통 응답 포맷
│   ├── services/           # 비즈니스 로직 (순수 기능)
│   │   ├── log_service.py
│   │   └── slack_service.py
│   ├── agents/             # **핵심: Agent 오케스트레이션**
│   │   ├── tools/          # 에이전트가 사용하는 도구 정의 (Function Definition)
│   │   └── orchestrator.py # Gemini와 소통하며 실행 흐름 제어
│   └── main.py             # FastAPI 앱 실행 파일
├── tests/                  # 테스트 코드
├── Dockerfile              # 컨테이너화 (공고 우대사항)
└── requirements.txt
```

```python
frontend/
├── src/
│   ├── app/                # App Router 기반 페이지
│   │   ├── layout.tsx
│   │   └── page.tsx        # 메인 챗봇/대시보드 UI
│   ├── components/         # 재사용 가능한 UI 컴포넌트
│   │   ├── chat/           # 채팅창, 메시지 버블
│   │   └── dashboard/      # 로그 차트, 상태 모니터링
│   ├── hooks/              # API 호출 및 상태 관리 커스텀 훅
│   ├── lib/                # 외부 라이브러리 설정 (API Client 등)
│   └── types/              # TypeScript 인터페이스 정의
├── public/                 # 정적 자산 (이미지 등)
└── tailwind.config.ts      # 스타일 설정
```
