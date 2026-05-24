# DevConnect Portal 🚀

DevConnect is a full-stack developer community platform built using Flask and MySQL.

The application allows developers to create profiles, upload profile images, search developers by skill, and interact with an AI-powered assistant integrated using OpenRouter API.

---

# Features

- User Authentication
- Password Hashing
- Session Management
- CRUD Operations
- Developer Search
- Profile Image Upload
- REST APIs
- AI Chatbot Integration
- Dynamic Developer Profiles

---

# Tech Stack

## Backend
- Python
- Flask
- MySQL

## Frontend
- HTML
- CSS
- Jinja2

## APIs & Tools
- OpenRouter API
- REST APIs
- Git & GitHub

---

# Project Structure

```bash
DevConnect/

│── app.py
│── requirements.txt
│── README.md

├── static/
│   ├── style.css
│   └── uploads/

├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── developers.html
│   ├── developer_profile.html
│   ├── update.html
│   ├── delete.html
│   ├── search.html
│   ├── search_user.html
│   └── ai_chat.html
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Avinash1905/DevConnect.git
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure MySQL

Create database:

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

# Run Application

```bash
python app.py
```

---

# REST API Endpoint

## Get All Developers

```http
GET /api/developers
```

---

# AI Assistant

The project includes an AI-powered assistant using OpenRouter API.

The chatbot answers questions using stored developer data from the MySQL database.

Example Questions:

```text
Who knows Flask?
Who has Python skill?
Which developer is intermediate?
```

---

# Security Features

- Password Hashing using Werkzeug
- Session-Based Authentication
- Protected Routes
- Secure File Uploads

---

# Future Improvements

- Resume Upload Feature
- Admin Dashboard
- JWT Authentication
- Chat History
- Deployment
- Responsive UI Improvements

---

# Author

Avinash Rayavarapu

GitHub:
https://github.com/Avinash1905
