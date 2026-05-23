# DevConnect Portal

DevConnect is a full-stack developer community platform built using Flask and MySQL.  
The application allows developers to create profiles, upload profile images, search developers by skill, and manage their accounts through authentication and session-based access control.

The project was built to practice backend development concepts such as authentication, REST APIs, file uploads, session handling, and CRUD operations.

---

# Features

- User Registration & Login
- Password Hashing
- Session-Based Authentication
- Profile Image Upload
- Developer Search by Skill
- CRUD Operations
- Individual Developer Profiles
- REST API Endpoint
- Flash Messages
- Protected Routes

---

# Tech Stack

## Backend
- Python
- Flask
- MySQL

## Frontend
- HTML
- CSS
- Jinja2 Templates

## Security
- Werkzeug Password Hashing
- Flask Sessions

---

# Project Structure

```bash
project/

├── app.py
├── requirements.txt
├── static/
│   ├── style.css
│   └── uploads/
│
└── templates/
    ├── index.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    ├── developers.html
    ├── developer_profile.html
    ├── update.html
    ├── delete.html
    ├── search.html
    └── search_user.html
```

---

# Installation

## Clone Repository

```bash
git clone <your-github-repo-link>
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure MySQL

Create a database:

```sql
CREATE DATABASE new;
```

---

Create table:

```sql
CREATE TABLE developers(

    id INT PRIMARY KEY AUTO_INCREMENT,

    name VARCHAR(100),

    email VARCHAR(100),

    skill VARCHAR(100),

    experience VARCHAR(100),

    password VARCHAR(255),

    profile_image VARCHAR(255)

);
```

---

## Run Application

```bash
python app.py
```

---

# REST API

## Get All Developers

```http
GET /api/developers
```

### Example Response

```json
[
  {
    "id": 1,
    "name": "Avinash",
    "email": "avinash@gmail.com",
    "skill": "Flask",
    "experience": "Intermediate"
  }
]
```

---

# Authentication Flow

- User registers with email and password
- Password is securely hashed before storing in database
- Login validates hashed passwords
- Sessions are used to protect routes
- Logout clears session data

---

# Future Improvements

- Admin Dashboard
- Resume Upload
- Email Verification
- JWT Authentication
- Pagination
- Dark Mode
- Deployment

---

# Learning Outcomes

This project helped in understanding:

- Flask Routing
- MySQL Integration
- Authentication Systems
- REST APIs
- Session Management
- File Upload Handling
- Backend Architecture

---

# Author

Avinash