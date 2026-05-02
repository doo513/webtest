# Solution

1. Login with `guest / guest123`.
2. Confirm that buying the Flag product directly fails because the guest balance is too low.
3. Open the delegated purchase page.
4. Intercept the URL request form.
5. Change `bot_active=false` to `bot_active=true`.
6. Change `buyer=guest` to `buyer=bot`.
7. Change the request URL to `/buy?product_id=5`.
8. The delegated purchase bot sends the URL request with the bot session, and the server converts the `/buy` URL into a POST purchase request.
9. Reopen the ledger page and inspect the HTML response source.
10. Find the hidden ledger metadata comment containing `GIFT-...`.
11. Submit the gift code to `/redeem` to receive the flag.
