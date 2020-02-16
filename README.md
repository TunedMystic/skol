Markette
---

A simple marketplace api, built with starlette and asyncpg.

<br />

Run postgres container
```
docker run -d -p 5432:5432 --name db postgres:11-alpine
```

Run the app
```
uvicorn markette.app:app --reload
```

Run tests
```
ENV=test pytest tests
```
