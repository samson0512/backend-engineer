# RESTful API for Project Management
A comprehensive RESTful API for a simple project management system, built with FastAPI, SQLAlchemy, and containerized with Docker for easy setup and deployment.

# Features
"User Authentication:" JWT-based authentication for secure access.

User Management: Create and manage user accounts.

Project Management: Create, view, update, and delete projects.

Task Management: Create, view, update, and delete tasks within projects.

# Getting Started
The recommended way to run this project is with Docker.

Prerequisites:

Docker Desktop installed and running.

Instructions:

Clone the repository and navigate to the project directory:

git clone [https://github.com/samson0512/backend-engineer.git](https://github.com/samson0512/backend-engineer.git)
cd backend-engineer/problems/problem-1

Build and Run the Docker Container:
Run the following commands in your terminal.

# Build the image
docker build -t project-management-api .

# Run the container
docker run -d -p 8000:8000 --env-file .env project-management-api

Access the API:
The application is now running and accessible at http://localhost:8000. You can view the interactive documentation at http://localhost:8000/docs.

API Endpoints Explained
The API is structured using routers for clear separation of concerns. Once the application is running, you can access the interactive API documentation (powered by Swagger UI) at http://localhost:8000/docs.

Authentication Routes (/auth)
Handles user registration and login to get a JWT access token.

POST /auth/register:

Description: Creates a new user account. This is the registration endpoint.

Request Body: A JSON object with email and password.

Response: The newly created user's information (excluding the password).

POST /auth/login:

Description: Authenticates a user and returns a JWT access token.

Request Body: Expects form data with username (the user's email) and password.

Response: Returns an access_token and token_type.

User Routes (/users)
Handles user creation and data retrieval.

POST /users/:

Description: Creates a new user in the database. (This is the same function as the register endpoint).

Request Body: A JSON object with email and password.

Response: The newly created user's information (excluding the password).

GET /users/me:

Description: Retrieves the details of the currently authenticated user based on the provided JWT token. This is a protected endpoint.

Headers: Requires an Authorization header with the value Bearer <your_access_token>.

Response: The current user's information (excluding the password).

GET /users/{id}:

Description: Retrieves a specific user by their ID. Requires authentication.

Response: The user's information.

Project Routes (/projects)
Handles all operations related to projects. Requires authentication for all endpoints.

POST /projects/:

Description: Creates a new project.

Request Body: A JSON object with title and description.

Response: The newly created project's details.

GET /projects/:

Description: Retrieves a list of all projects created by the authenticated user.

Response: A list of projects.

GET /projects/{id}:

Description: Retrieves a single project by its ID.

Response: The project's details.

PUT /projects/{id}:

Description: Updates an existing project.

Request Body: A JSON object with the new title and description.

Response: The updated project's details.

DELETE /projects/{id}:

Description: Deletes a project by its ID.

Response: A success message.

Task Routes (/tasks)
Handles all operations related to tasks. Requires authentication for all endpoints.

POST /tasks/:

Description: Creates a new task associated with a project.

Request Body: A JSON object with title, description, status, and project_id.

Response: The newly created task's details.

GET /tasks/:

Description: Retrieves a list of all tasks. Can be filtered by project_id.

Response: A list of tasks.

GET /tasks/{id}:

Description: Retrieves a single task by its ID.

Response: The task's details.

PUT /tasks/{id}:

Description: Updates an existing task.

Request Body: A JSON object with the new title, description, and status.

Response: The updated task's details.

DELETE /tasks/{id}:

Description: Deletes a task by its ID.

Response: A success message.
