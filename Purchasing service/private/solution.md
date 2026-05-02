# 풀이

1. `guest / guest123`으로 로그인한다.
2. 상점에서 플래그 상품을 직접 구매하면 크레딧 부족으로 실패하는 것을 확인한다.
3. 대리구매 화면으로 이동한다.
4. 대리구매 URL 요청 폼을 인터셉트한다.
5. `leader_active=false`를 `leader_active=true`로 바꾼다.
6. `buyer=guest`를 `buyer=leader`로 바꾼다.
7. 요청 URL을 `/buy?product_id=5`로 바꾼다.
8. 서버가 leader 세션으로 내부 구매 요청을 보내고, leader가 플래그 상품을 구매한다.
9. 구매 원장 페이지를 다시 열고 HTML 응답 소스를 확인한다.
10. `GIFT-...` 형식의 기프트 코드를 찾는다.
11. `/redeem`에서 기프트 코드를 교환해 플래그를 획득한다.
