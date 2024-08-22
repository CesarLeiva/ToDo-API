# ToDo API

This is a simple To-Do API that allows users to manage their tasks through CRUD operations. The API is built using Flask and does not use an ORM.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Models](#models)
- [Error Handling](#error-handling)
- [License](#license)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CesarLeiva/ToDo-API.git
   cd ToDo-API
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**

   ```bash
   flask run
   ```

## Usage

Once the server is running, you can interact with the API using tools like Postman, cURL, or any HTTP client.

### Base URL

```
http://127.0.0.1:5000/api
```

## Endpoints

### User

- **Create a User**

  - **Endpoint:** `/signup`
  - **Method:** `POST`
  - **Request Body:**

    ```json
    {
      "account": "string",
      "password": "string",
      "name": "string",
      "id": "string"
    }
    ```
  - **Response:**

    ```json
    {
      "message": "User created successfully",
      "user_id": "unique_user_id"
    }
    ```

- **Authenticate a User**

  - **Endpoint:** `/login`
  - **Method:** `POST`
  - **Request Body:**

    ```json
    {
      "account": "string",
      "password": "string"
    }
    ```
  - **Response:**

    ```json
    {
      "message": "User authenticated successfully",
      "token": "auth_token"
    }
    ```

### Task

- **Create a Task**

  - **Endpoint:** `/tasks`
  - **Method:** `POST`
  - **Headers:** `Authorization: Bearer <token>`
  - **Request Body:**

    ```json
    {
      "title": "string",
      "description": "string",
      "due_date": "YYYY-MM-DD",
      "priority": "string"
    }
    ```
  - **Response:**

    ```json
    {
      "message": "Task created successfully",
      "task_id": "unique_task_id"
    }
    ```

- **Get All Tasks**

  - **Endpoint:** `/tasks`
  - **Method:** `GET`
  - **Headers:** `Authorization: Bearer <token>`
  - **Response:**

    ```json
    [
      {
        "id": "task_id",
        "title": "string",
        "description": "string",
        "due_date": "YYYY-MM-DD",
        "priority": "string",
        "status": "string"
      },
      ...
    ]
    ```

- **Update a Task**

  - **Endpoint:** `/tasks/<task_id>`
  - **Method:** `PUT`
  - **Headers:** `Authorization: Bearer <token>`
  - **Request Body:**

    ```json
    {
      "title": "string",
      "description": "string",
      "due_date": "YYYY-MM-DD",
      "priority": "string",
      "status": "string"
    }
    ```
  - **Response:**

    ```json
    {
      "message": "Task updated successfully"
    }
    ```

- **Delete a Task**

  - **Endpoint:** `/tasks/<task_id>`
  - **Method:** `DELETE`
  - **Headers:** `Authorization: Bearer <token>`
  - **Response:**

    ```json
    {
      "message": "Task deleted successfully"
    }
    ```

## Models

### User

- **Attributes:**
  - `account` (string): The user's account identifier.
  - `password` (string): The user's password (should be hashed).
  - `name` (string): The user's name.
  - `id` (string): A unique identifier for the user.

### Task

- **Attributes:**
  - `title` (string): The title of the task.
  - `description` (string): A brief description of the task.
  - `due_date` (date): The due date for the task.
  - `priority` (string): Priority level of the task (e.g., Low, Medium, High).
  - `status` (string): Current status of the task (e.g., Pending, Completed).

## Error Handling

The API returns appropriate HTTP status codes and error messages when something goes wrong, such as:

- `400 Bad Request`: Invalid input data.
- `401 Unauthorized`: Authentication failed.
- `404 Not Found`: The requested resource was not found.
- `500 Internal Server Error`: An error occurred on the server.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
