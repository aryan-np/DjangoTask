# Django User Authentication and API Project

This project contains two main parts demonstrating user authentication and API handling in Django:

- **Task 2:** API for a Simple Todo App using Django REST Framework.
- **Task 3:** User Registration and Login with Custom Profile.

---

## Task 2: API with Token Authentication

### Features
## CRUD Operations

# Create Todo (POST `/todos/`)
Creates a new todo item for the authenticated user with `title` and `description`.

# Read Todos (GET `/todos/`)
Retrieves a paginated list of todos owned by the authenticated user.  
Supports filtering by completion status using the query parameter:  
`?completed=true` or `?completed=false`

# Read Single Todo (GET `/todos/<id>/`)
Retrieves details of a single todo item by ID, only if owned by the authenticated user.

# Update Todo (PUT/PATCH `/todos/<id>/`)
Updates the `title`, `description`, and/or `completed` status of the specified todo if owned by the user.

# Delete Todo (DELETE `/todos/<id>/`)
Deletes the specified todo item if owned by the authenticated user.

---

## Authentication

# Login (POST `/login/`)
Validates user credentials and returns an authentication token.

# Register (POST `/register/`)
Registers a new user and returns an authentication token.

### Key Components
- **Login API** that accepts username and password, returns tokens.
- **Refresh Token API** to renew the access token using a refresh token.
- Protected API views require a valid token in the `Authorization` header.
- Uses `djangorestframework-simplejwt` (or similar) for token management.

### How to Use
1. Run migrations and create a superuser.
2. Obtain a token by POSTing credentials to the login endpoint.
3. Use the access token in the `Authorization: Bearer <token>` header to access protected endpoints.
4. Refresh tokens using the refresh endpoint when the access token expires.

---

## Task 3: User Registration and Login with Custom Profile

### Features
- User registration, login, logout using Django's built-in User model.
- Extended user profile with additional fields (`bio` and `profile_picture`).
- Profile page showing user's username, email, and profile details.
- Profile editing form to update bio and profile picture URL.
- Password reset functionality using Django's built-in password reset views with console email backend.

### Models
- `Profile` model with OneToOne relation to Django's User model.
- Fields: `bio` (TextField), `profile_picture` (CharField for URL).

### Views
- `register`: Register new users.
- `login`: User login using Django auth forms.
- `profile`: View and edit user profile (requires login).
- `logout_view`: Logs out the user.
- Password reset views using Django's built-in views.

### URLs
- `/register/` — User registration.
- `/login/` — User login.
- `/logout/` — Logout user.
- `/profile/` — Profile view/edit.
- Password reset URLs (`password_reset/`, `password_reset/done/`, etc.)

### Templates
- Simple templates for registration, login, and profile pages.
- Profile page displays username, email, profile picture, and form to update profile details.

---

## Setup and Running

1. **Clone the repo** and create a virtual environment.
    python -m venv (venv name)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run Migrations:
    python manage.py migrate
4. Create a superuser (optional for admin access):
    python manage.py createsuperuser
5. Run the development server:
    python manage.py runserver


## Notes

1. Password reset emails are sent to the console for development purposes.

2. Tokens must be included in the Authorization header for API access:

    Authorization: Token <access_token>
3.Profile picture URL is expected to be a valid image URL.
