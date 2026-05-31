# AI Resume Analyzer

AI Resume Analyzer is a Flask-based web application that allows users to upload resumes in PDF format and receive AI-powered feedback, ATS scoring, skill analysis, and improvement suggestions.

The application extracts text from uploaded resumes, analyzes the content using OpenRouter AI models, and stores previous analyses for future reference.

---

## Features

* User Registration and Login
* Password Hashing using Werkzeug
* Session-Based Authentication
* PDF Resume Upload
* Resume Text Extraction using PyPDF2
* AI-Powered Resume Analysis
* ATS Score Generation
* Skill Identification
* Weakness Detection
* Resume Improvement Suggestions
* Analysis History Tracking
* MySQL Database Integration

---

## Tech Stack

### Backend

* Python
* Flask
* MySQL

### AI

* OpenRouter API
* GPT-4o Mini

### Frontend

* HTML
* CSS
* Jinja2 Templates

### Libraries

* PyPDF2
* Requests
* Werkzeug
* Python Dotenv

---

## Project Structure

AI_Resume_Analyzer/

├── app.py

├── requirements.txt

├── .env

├── uploads/

├── static/

│   └── style.css

└── templates/

```
├── index.html

├── register.html

├── login.html

├── dashboard.html

├── upload_resume.html

├── result.html

└── history.html
```

---

## Installation

### Clone Repository

git clone <your-repository-url>

cd AI_Resume_Analyzer

---

### Create Virtual Environment

python -m venv venv

---

### Activate Environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

---

### Install Dependencies

pip install -r requirements.txt

---

## Configure Environment Variables

Create a .env file:

OPENROUTER_API_KEY=your_api_key_here

---

## Configure Database

Create database:

CREATE DATABASE new;

---

Create users table:

CREATE TABLE users(

id INT PRIMARY KEY AUTO_INCREMENT,

name VARCHAR(100),

email VARCHAR(100) UNIQUE,

password VARCHAR(255)

);

---

Create resumes table:

CREATE TABLE resumes(

id INT PRIMARY KEY AUTO_INCREMENT,

user_id INT,

filename VARCHAR(255),

upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

---

Create analysis_history table:

CREATE TABLE analysis_history(

id INT PRIMARY KEY AUTO_INCREMENT,

user_email VARCHAR(100),

score VARCHAR(20),

analysis TEXT

);

---

## Run Application

python app.py

---

## Future Improvements

* Role-Based ATS Scoring
* Resume Improvement Generator
* Downloadable Reports
* Resume Comparison
* Admin Dashboard
* Dark Mode
* Email Reports

---

## Learning Outcomes

This project demonstrates:

* Flask Development
* Authentication Systems
* Session Management
* PDF Processing
* REST API Integration
* AI Application Development
* MySQL Database Operations
* Prompt Engineering

---

## Author

Avinash Rayavarapu

GitHub: https://github.com/Avinash1905
