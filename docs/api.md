# API Documentation

## Endpoints

### GET /

Returns a simple JSON response.

Response:

```json
{
  "message": "Hello, Flask from Docker!",
  "project": "Flask Docker Sample"
}
```

### GET /health/

Returns application health and environment metadata.

Response:

```json
{
  "status": "ok",
  "environment": "development",
  "project": "Flask Docker Sample"
}
```

### POST /api/v1/echo

Echoes the request message.

Request JSON:

```json
{
  "message": "hello"
}
```

Response:

```json
{
  "echo": "hello"
}
```
