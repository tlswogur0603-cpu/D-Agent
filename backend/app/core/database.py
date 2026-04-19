"""
SQLAlchemy ORM용 DB 구성 모듈입니다.
Engine은 DB 연결/풀을 관리하는 전역 객체, SessionLocal은 요청 단위 세션(트랜잭션) 생성기,
Base는 모든 ORM 모델이 상속하는 선언형(Declarative) 베이스입니다.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

