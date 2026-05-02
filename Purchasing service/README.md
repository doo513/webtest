# Purchasing Service

HackerLogin CTF 문제 패키지입니다.

## 문제 요약

`guest / guest123` 계정으로 접속할 수 있는 사내 구매 서비스입니다. 일반 사용자는 상점에서 상품을 구매할 수 있지만, 플래그 상품을 살 만큼의 크레딧은 가지고 있지 않습니다.

대리구매 화면에는 내부 URL로 요청을 보내는 기능이 남아 있습니다. `leader` 계정은 비활성화되어 일반 로그인은 불가능하지만 충분한 크레딧을 가지고 있으며, 잘못 신뢰된 대리구매 요청을 통해 플래그 상품을 구매하게 만들 수 있습니다.

구매 원장 화면에는 일반 구매 내역만 보이지만, 응답에는 추가 메타데이터가 포함될 수 있습니다.

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
