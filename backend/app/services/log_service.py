import logging

import re
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple


_LOGGER = logging.getLogger(__name__)


_TS_CANDIDATE_RE = re.compile(
    r"(?P<ts>"
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?"
    r"|"
    r"\d{4}/\d{2}/\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d{1,6})?"
    r"|"
    r"\d{10}(?:\d{3})?"
    r")"
)


def _parse_timestamp_from_line(line: str) -> Optional[datetime]:
    """
    로그 라인에서 타임스탬프를 최대한 유연하게 추출/파싱합니다.
    - ISO 8601 (예: 2026-04-15T12:34:56Z, 2026-04-15 12:34:56+09:00, 2026-04-15 12:34:56.123)
    - 슬래시 날짜 (예: 2026/04/15 12:34:56)
    - epoch seconds/ms (10자리/13자리)
    """
    m = _TS_CANDIDATE_RE.search(line)
    if not m:
        return None

    raw = m.group("ts").strip()

    # epoch seconds / milliseconds
    if raw.isdigit() and len(raw) in (10, 13):
        try:
            v = int(raw)
            if len(raw) == 13:
                v = v / 1000.0
            return datetime.fromtimestamp(v, tz=timezone.utc)
        except Exception:
            return None

    # normalize
    s = raw.replace(",", ".")
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    # fromisoformat handles many variants (but not bare Z)
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        pass

    # common fallback formats
    fmts = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S.%f",
    )
    for fmt in fmts:
        try:
            dt = datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            continue

    return None


def _is_error_line(line: str) -> bool:
    # 흔한 로그 포맷: "... ERROR ..." / "level=ERROR" / "[ERROR]" 등을 폭넓게 커버
    return bool(re.search(r"(^|\W)ERROR(\W|$)", line))


def get_filtered_logs(logs: List[str]) -> List[List[str]]:
    """
    - 로그 중 'ERROR' 레벨 라인을 찾습니다.
    - ERROR 라인을 발견하면 그 직전의 로그 2~3줄(상황 설명용)을 함께 묶어 가져옵니다. (가능하면 3줄)
    - 인덱스 범위를 벗어나지 않도록 안전하게 처리합니다.
    - 로그에 타임스탬프가 있다면 최근 10분 이내 발생한 로그만 고릅니다. (형식을 유연하게 인식)
    - 조건에 맞는 로그 세트 중 가장 최근 것부터 최대 20개만 반환합니다.
    """
    if not logs:
        return []

    now_utc = datetime.now(timezone.utc)
    window_start = now_utc - timedelta(minutes=10)

    candidates: List[Tuple[Optional[datetime], int, List[str]]] = []

    for i, line in enumerate(logs):
        if not _is_error_line(line):
            continue

        # 2~3줄: 가능하면 3줄을 포함하고, 시작 부분에서는 가능한 만큼만 포함
        start_idx = max(0, i - 3)
        group = logs[start_idx : i + 1]

        # 타임스탬프는 그룹(컨텍스트 포함)에서 파싱 가능한 것 중 가장 최신을 사용
        dts: List[datetime] = []
        for g in group:
            dt = _parse_timestamp_from_line(g)
            if dt is not None:
                dts.append(dt)

        group_dt = max(dts) if dts else None

        # "타임스탬프가 있다면" 최근 10분만 통과. 없으면 시간필터 적용하지 않음.
        if group_dt is not None and group_dt < window_start:
            continue

        candidates.append((group_dt, i, group))

    # 가장 최근 것부터: timestamp 우선 정렬, timestamp가 없다면 원본 등장 순서 기준으로 뒤쪽(최근) 우선
    def _sort_key(item: Tuple[Optional[datetime], int, List[str]]):
        dt, idx, _ = item
        # dt가 없으면 아주 오래된 것으로 간주(끝으로 밀림)
        dt_sort = dt if dt is not None else datetime.min.replace(tzinfo=timezone.utc)
        return (dt_sort, idx)

    candidates.sort(key=_sort_key, reverse=True)

    return [g for _, __, g in candidates[:20]]
