# Purchasing Service

HackerLogin CTF 문제 패키지입니다.

## 구조

```text
Purchasing service/
├─ Description.md
├─ Specfile
├─ Dockerfile
├─ public/
└─ private/
```

- `Description.md`: 참가자에게 공개되는 문제 설명
- `Specfile`: 문제 메타데이터
- `public/`: 참가자 제공 파일
- `private/`: 플래그, 풀이, 배포 전용 내부 파일
- `private/runtime.py`: 플래그 읽기, 대리구매 내부 요청, 원장 메타데이터 렌더링

## 로컬 실행

```bash
docker build -t purchasing-service .
docker run --rm -p 8000:8000 purchasing-service
```

브라우저에서 `http://127.0.0.1:8000`으로 접속합니다.
