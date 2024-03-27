# FastAPI Chore Management API

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

## Overview

This project is a FastAPI-based API for managing chores. It allows users to create, edit, and complete chores, with authentication implemented to ensure secure access to the API endpoints.

## Features

- **Create Chores:** Users can create new chores with details such as title, description, due date, and assigned user.
- **Edit Chores:** Existing chores can be edited to update their details.
- **Complete Chores:** Users can mark chores as completed.
- **Authentication:** Secure authentication is implemented using JWT tokens. Admin users have elevated privileges for managing chores.

## Technologies Used

- FastAPI
- Python
- PostgreSQL (or your preferred database)
- JWT for authentication

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RemyAde/ChoreApp.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for database connection and JWT secret key.

4. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

The API documentation is automatically generated and can be accessed at `/docs` endpoint when the server is running. It provides detailed information about all available endpoints, request parameters, and response formats.

## Usage

1. Register and authenticate as a user to obtain a JWT token.
2. Use the token to access protected endpoints for managing chores.
3. Follow the API documentation for endpoint usage and payload formats.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## Credits

This project was inspired by the "FastAPI - The complete course" by codingwithroby.