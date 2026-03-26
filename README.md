# Travel Planner API

## How to Run

Before starting the app, make sure to complete your `.env` file with required variables:

- `SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `ART_INSTITUTE_URL`

### Run with Docker

```bash
docker compose up --build
```

After startup:

- API base URL: `http://localhost:8000/api/`
- Admin panel: `http://localhost:8000/admin/`

## API Documentation

- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`
