# API Documentation

## Web Pages

### GET / (Home)
Home page showcasing all available features.

### GET /about
About page with project information and technologies.

### GET /contact
Contact page with next steps and suggestions.

### GET /calendar
Interactive monthly calendar displaying events.

### GET /tasks
Task manager page for creating and managing tasks.

## JSON Endpoints

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

Response (201 Created):

```json
{
  "echo": "hello"
}
```

## Form Pages

### POST /tasks

Create a new task via form submission.

Form Data:
- `title` (required) - Task title
- `description` (optional) - Task description
- `priority` (optional) - Priority level: `low`, `medium`, or `high`

### POST /tasks/<task_id>/toggle

Toggle task completion status.

### POST /tasks/<task_id>/delete

Delete a task.
