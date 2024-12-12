# Tasks Module API Documentation

## Overview

The `tasks` module provides a set of REST API endpoints for managing tasks within projects. It extends the functionality of the `projects` module, allowing you to create, read, update, and delete tasks, as well as filter them by associated project.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
   - [List and Create Tasks](#list-and-create-tasks)
   - [Retrieve, Update, and Delete a Task](#retrieve-update-and-delete-a-task)
5. [Filtering by Project](#filtering-by-project)
6. [Request and Response Examples](#request-and-response-examples)
7. [Error Handling](#error-handling)
8. [Testing](#testing)

---

## Introduction

Each `Task` is associated with a `Project` (defined in the `projects` module). A task can have:
- A name and description
- Start and end datetime
- A location type (0 - No location, 1 - QR Code scan, 2 - GPS location)

**Key Features:**
- Create, read, update, and delete tasks.
- Filter tasks by `project_id`.

---

## Prerequisites

- A running Django server with the `accounts`, `projects`, and `tasks` apps installed and migrated.
- The `accounts` module for user authentication.
- A valid `auth_token` cookie obtained through `/api/login/`.

---

## Authentication

All endpoints in the `tasks` module require the user to be authenticated. The authentication is handled via a cookie named `auth_token` set by the `/api/login/` endpoint.

Make sure that `auth_token` is sent with each request, either automatically by your browser or manually configured in your HTTP client.

---

## Endpoints

All endpoints are accessible under `/api/tasks/` and use standard REST patterns.

### List and Create Tasks

- **GET `/api/tasks/`**:  
  Returns a list of all tasks. This can be filtered by `project_id` (see [Filtering by Project](#filtering-by-project)).

- **POST `/api/tasks/`**:  
  Creates a new task. Requires a `project` field referencing a valid project ID, and a `name`. Other fields (`description`, `startdatetime`, `enddatetime`, `locationType`) are optional but can be provided.

**Request Body (POST):**
```json
{
  "project": 1,
  "name": "New Task",
  "description": "Description of the task",
  "startdatetime": "2024-12-31T10:00:00Z",
  "enddatetime": "2024-12-31T12:00:00Z",
  "locationType": "2"
}
```

**Response on Success (201 Created):**
```json
{
  "id": 1,
  "project": 1,
  "name": "New Task",
  "description": "Description of the task",
  "startdatetime": "2024-12-31T10:00:00Z",
  "enddatetime": "2024-12-31T12:00:00Z",
  "locationType": "2"
}
```

---

### Retrieve, Update, and Delete a Task

- **GET `/api/tasks/{id}/`**:  
  Retrieves details for a single task.

- **PUT `/api/tasks/{id}/`**:  
  Updates a task’s details. Requires at least the `project` and `name` fields. Other fields are optional.

- **DELETE `/api/tasks/{id}/`**:  
  Deletes the specified task.

**Response on Success (GET 200 OK):**
```json
{
  "id": 1,
  "project": 1,
  "name": "New Task",
  "description": "Description of the task",
  "startdatetime": "2024-12-31T10:00:00Z",
  "enddatetime": "2024-12-31T12:00:00Z",
  "locationType": "2"
}
```

---

## Filtering by Project

You can filter tasks by a specific project using the `?project_id=` query parameter.

**Example:**
```
GET /api/tasks/?project_id=1
```

This will return only the tasks associated with the project whose ID is 1.

---

## Request and Response Examples

**Create a Task (POST `/api/tasks/`):**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"project":1,"name":"Backend Setup","description":"Initialize the backend services"}' \
  --cookie "auth_token=<your_token_here>"
```

**Retrieve All Tasks (GET `/api/tasks/`):**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  --cookie "auth_token=<your_token_here>"
```

**Filter Tasks by Project (GET `/api/tasks/?project_id=1`):**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?project_id=1" \
  --cookie "auth_token=<your_token_here>"
```

---

## Error Handling

Common error scenarios:

- **401 Unauthorized:** Missing or invalid `auth_token`.
- **400 Bad Request:** Invalid data (e.g., missing required fields like `project` or `name`).
- **404 Not Found:** Task or Project does not exist.

Error responses generally follow the format:
```json
{
  "detail": "Descriptive error message."
}
```

---

## Testing

To test these endpoints:
1. **Authenticate** using `/api/login/` to obtain `auth_token`.
2. **Include the cookie** in subsequent requests.
3. **Verify responses** for correct behavior and error handling.

Recommended tools: `curl`, `Postman`, or `HTTPie`.