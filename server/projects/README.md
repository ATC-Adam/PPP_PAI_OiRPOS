# Projects Module API Documentation

## Overview

The Projects module provides a set of REST API endpoints to manage projects and their associated users. It integrates with the existing authentication system, requiring users to be authenticated via the `auth_token` cookie.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
    - [List and Create Projects](#list-and-create-projects)
    - [Retrieve, Update, and Delete a Project](#retrieve-update-and-delete-a-project)
    - [Assign a User to a Project](#assign-a-user-to-a-project)
    - [Remove a User from a Project](#remove-a-user-from-a-project)
    - [List Users Assigned to a Project](#list-users-assigned-to-a-project)
5. [Request and Response Examples](#request-and-response-examples)
6. [Error Handling](#error-handling)
7. [Testing](#testing)

---

## Introduction

This module extends the base API by providing CRUD operations on `Project` resources and functionalities to manage user assignments within these projects. Each project can have multiple users assigned, each with an optional role.

**Key Features:**
- Create, read, update, and delete projects.
- Assign and remove users from projects.
- Retrieve detailed information about projects, including assigned users.

---

## Prerequisites

- A running Django server with the `projects` application installed and migrated.
- The `accounts` module for user authentication.
- A valid `auth_token` cookie obtained through the `/api/login/` endpoint.

---

## Authentication

All endpoints in the Projects module require the user to be authenticated. Authentication is handled via a cookie named `auth_token` set by the `/api/login/` endpoint.

Ensure that `auth_token` is included in all requests to protected endpoints. Browsers handle this automatically if cookies are set. For tools like Postman, make sure the cookie is preserved between requests.

---

## Endpoints

All endpoints are prefixed with `/api/`. The `projects` endpoints are provided via a DRF Router and thus available at `/api/projects/` and subsequent paths.

### List and Create Projects

- **GET `/api/projects/`**:  
  Returns a list of all projects.
  
- **POST `/api/projects/`**:  
  Creates a new project. Requires `name`; `description` is optional.

**Request Body (POST):**
```json
{
  "name": "New Project",
  "description": "Project description"
}
```

**Response on Success (201 Created):**
```json
{
  "id": 1,
  "name": "New Project",
  "description": "Project description"
}
```

---

### Retrieve, Update, and Delete a Project

- **GET `/api/projects/{id}/`**:  
  Retrieves detailed information about a single project, including assigned users.
  
- **PUT `/api/projects/{id}/`**:  
  Updates the project's information. Requires `name` and optional `description`.
  
- **DELETE `/api/projects/{id}/`**:  
  Deletes the specified project.

**Response on Success (GET 200 OK):**
```json
{
  "id": 1,
  "name": "New Project",
  "description": "Project description",
  "users": [
    {
      "id": 2,
      "login": "user_login",
      "name": "John",
      "surname": "Doe",
      "role": "Developer"
    }
  ]
}
```

---

### Assign a User to a Project

- **POST `/api/projects/{id}/assign_user/`**:  
  Assigns a user to the specified project. Requires `user_id` in the JSON body. Optional `role` can also be provided.

**Request Body:**
```json
{
  "user_id": 2,
  "role": "Developer"
}
```

**Response on Success (200 OK):**
```json
{
  "detail": "Użytkownik został przypisany do projektu."
}
```

---

### Remove a User from a Project

- **POST `/api/projects/{id}/remove_user/`**:  
  Removes a user from the specified project. Requires `user_id` in the JSON body.

**Request Body:**
```json
{
  "user_id": 2
}
```

**Response on Success (200 OK):**
```json
{
  "detail": "Użytkownik został usunięty z projektu."
}
```

---

### List Users Assigned to a Project

- **GET `/api/projects/{id}/users/`**:  
  Returns a list of all users assigned to the specified project along with their roles.

**Response on Success (200 OK):**
```json
[
  {
    "id": 2,
    "login": "user_login",
    "name": "John",
    "surname": "Doe",
    "role": "Developer"
  }
]
```

---

## Request and Response Examples

**Create a Project (POST `/api/projects/`):**
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Website Redesign","description":"Revamp the company site"}' \
  --cookie "auth_token=<your_token_here>"
```

**Retrieve Project Details (GET `/api/projects/1/`):**
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/ \
  --cookie "auth_token=<your_token_here>"
```

---

## Error Handling

Common error scenarios:

- **401 Unauthorized:** Missing or invalid `auth_token`.
- **400 Bad Request:** Invalid data, such as missing `user_id` or `name`.
- **404 Not Found:** Project or user does not exist.

Error responses generally follow the format:
```json
{
  "detail": "Descriptive error message."
}
```