# ToDo API

This is a simple To-Do API that allows users to manage their tasks through CRUD operations. The API is built using Flask and does not use an ORM.

View postman documentation -> https://documenter.getpostman.com/view/34385721/2sAXjDfwCr

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
http://127.0.0.1:4000/api
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
      "message": "User created successfully"
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
      "message": "User authenticated successfully"
    }
    ```

### Task

- **Create a Task**

  - **Endpoint:** `/tasks`
  - **Method:** `POST`
  - **Request Body:**

    ```json
    {
      "description": "string",
      "priority": "string",
      "date": "YYYY/MM/DD",
      "time": "HH:MM",
    }
    ```
  - **Response:**

    ```json
    {
      "message": "Task created successfully"
    }
    ```

- **Get All Tasks**

  - **Endpoint:** `/tasks`
  - **Method:** `GET`
  - **Response:**

    ```json
    [
      {
        "id": int,
        "description": "string",
        "priority": "string",
        "date": "YYYY/MM/DD",
        "time": "HH:MM",
        "completed": bool,
        "published": bool
      }
    ]
    ```

- **Update a Task**

  - **Endpoint:** `/tasks/<task_id>`
  - **Method:** `PUT`
  - **Request Body:**

    ```json
    {
      "description": "string",
      "priority": "string",
      "date": "YYYY/MM/DD",
      "time": "HH:MM",
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
  - `id` (int): A unique identifier for the task.
  - `description` (string): A brief description of the task.
  - `priority` (string): Priority level of the task (e.g., Very Low, Low, Medium, High).
  - `date` (date): The date for the task, formatted as `YYYY/MM/DD`.
  - `time` (time): The time for the task, formatted as `HH:MM`.
  - `completed` (bool): Whether the task is completed.
  - `published` (bool): Whether the task is published.

## Error Handling

The API returns appropriate HTTP status codes and error messages when something goes wrong, such as:

- `400 Bad Request`: Invalid input data.
- `401 Unauthorized`: Authentication failed.
- `404 Not Found`: The requested resource was not found.
- `500 Internal Server Error`: An error occurred on the server.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
