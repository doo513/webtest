# Purchasing Service

HackerLogin CTF challenge package.

## Structure

- `Description.md`: participant-facing challenge description
- `Specfile`: challenge metadata
- `Dockerfile`: single-container deployment
- `public/`: files provided to participants
- `private/`: flag and solution
- `web/`: deployed Flask service

## Local Run

```bash
docker build -t purchasing-service .
docker run --rm -p 8000:8000 purchasing-service
```

Open `http://127.0.0.1:8000`.
