"""
FastAPI 서버 엔트리포인트(main)입니다.

이 파일에서 수행하는 것:
- FastAPI 앱 인스턴스(app) 생성/재사용
- CORS(브라우저 보안 정책) 설정
- API 라우터(엔드포인트) 등록
- 서버 시작 시(startup) 이벤트 로그 출력
"""

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ------------------------------------------------------------
# 1) 기본 설정: FastAPI 앱 인스턴스(app) 생성/재사용
# ------------------------------------------------------------
# - 이미 다른 코드에서 app = FastAPI()가 만들어져 있다면 그 객체를 그대로 사용합니다.
# - 없다면 여기에서 새로 생성합니다.
try:
    app  # type: ignore[name-defined]
except NameError:
    # FastAPI 애플리케이션 인스턴스를 생성합니다.
    # 이 app 객체에 라우터/미들웨어/이벤트 등을 등록하게 됩니다.
    app = FastAPI()

# ------------------------------------------------------------
# 2) 보안(CORS) 설정: 허용할 Origin(출처)만 화이트리스트로 제한
# ------------------------------------------------------------
# 브라우저는 다른 출처(Origin)에서 API 호출 시 CORS 정책을 적용합니다.
# allow_origins에 등록된 출처만 API 호출을 허용하도록 제한합니다.
allow_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]

# CORSMiddleware를 FastAPI 앱에 추가합니다.
# - allow_methods=["*"]  : 모든 HTTP 메서드(GET/POST/PUT/DELETE 등) 허용
# - allow_headers=["*"]  : 모든 요청 헤더 허용
# - allow_credentials=True: 쿠키/인증정보 포함 요청을 허용(필요 시 프론트에서 사용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# 3) 라우터 연결: /api/v1/agent 하위로 agent 라우터를 등록
# ------------------------------------------------------------
# app.api.v1.agent 모듈에서 router를 가져와 FastAPI 앱에 연결합니다.
# prefix는 /api/v1/agent로 고정하고, Swagger 문서에서 보이도록 tags를 ["agent"]로 지정합니다.
from app.api.v1.agent import router as agent_router  # noqa: E402

app.include_router(
    agent_router,
    prefix="/api/v1/agent",
    tags=["agent"],
)

# ------------------------------------------------------------
# 3-1) 기본 경로(/) 안내: 서버 상태/문서/주요 엔드포인트 안내
# ------------------------------------------------------------
from app.core.config import settings  # noqa: E402


@app.get("/")
async def root() -> dict:
    return {
        "project": settings.PROJECT_NAME,
        "status": "ok",
        "docs": "/docs",
        "message": (
            "서버가 정상 동작 중입니다. "
            "API 문서는 /docs에서 확인할 수 있습니다."
        ),
        "endpoints": {
            "agent_base": "/api/v1/agent",
            "agent_analyze": "/api/v1/agent/analyze",
        },
    }


# ------------------------------------------------------------
# 3-2) 전역 404 예외 처리: 기본 Not Found 대신 친절한 한국어 메시지 반환
# ------------------------------------------------------------
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "error": "요청하신 경로를 찾을 수 없습니다.",
            "requested_path": request.url.path,
            "message": (
                "입력하신 경로가 존재하지 않습니다. "
                "사용 가능한 API 목록은 /docs에서 확인해주세요."
            ),
            "docs": "/docs",
            "hint_endpoints": {
                "agent_base": "/api/v1/agent",
                "agent_analyze": "/api/v1/agent/analyze",
            },
        },
    )


# ------------------------------------------------------------
# 4) 이벤트 로그: 서버 시작(startup) 시 터미널에 안내 메시지 출력
# ------------------------------------------------------------
# FastAPI가 기동될 때 한 번 실행되는 이벤트입니다.
@app.on_event("startup")
async def on_startup() -> None:
    # 서버 시작 시점에 동작 여부를 쉽게 확인할 수 있도록 터미널에 출력합니다.
    print("Security Analysis API is starting...")

