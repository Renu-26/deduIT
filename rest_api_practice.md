## Tools Used
- Postman
- JSONPlaceholder — a fake online REST API for practice

Base URL: `https://jsonplaceholder.typicode.com`

### GET — Retrieve a post

**Method:** GET

**URL:** `https://jsonplaceholder.typicode.com/posts/1`

A JSON response containing post details.

### Query Parameters

**Method:** GET

**URL:** `https://jsonplaceholder.typicode.com/posts?userId=1`

A list of posts associated with user ID 1.

### POST — Create a post

**Method:** POST

**URL:** `https://jsonplaceholder.typicode.com/posts`

**Body:**
```json
{
  "title": "Learning Postman",
  "body": "My first POST request",
  "userId": 1
}
```

**Output status:** `201 Created`

POST sends data to request creation of a resource.

### PATCH — Update a post

**Method:** PATCH

**URL:** `https://jsonplaceholder.typicode.com/posts/1`

**Body:**
```json
{
  "title": "My Updated Title"
}
```

**Output status:** `200 OK`

PATCH requests a partial update to an existing resource.

###  DELETE — Delete a post

**Method:** DELETE

**URL:** `https://jsonplaceholder.typicode.com/posts/1`

**Body:** Empty

DELETE requests removal of a resource identified by the URL.