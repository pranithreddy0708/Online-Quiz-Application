# 📝 Online Quiz Application (Flask & MySQL)

A complete, modern, professional, and fully responsive **Online Quiz Application** built using **Python Flask**, **MySQL**, **SQLAlchemy**, **HTML5**, **CSS3**, **Bootstrap 5**, and **JavaScript**.

---

## 🌐 Live Server Access & Application Links

When running the application locally (`python app.py`), access the server via:

- 🏠 **Main Application URL**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- 🛡️ **Admin Portal**: [http://127.0.0.1:5000/admin/login](http://127.0.0.1:5000/admin/login)
  - **Username**: `pranith0708`
  - **Password**: `mrec2024`
- 👤 **User Login**: [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
  - **Email**: `john@example.com`
  - **Password**: `user123`

---


## 🌟 Key Features

### 👤 User Module
- **Registration & Authentication**: Secure sign-up and log in with password hashing using Werkzeug.
- **Interactive Dashboard**: View personal quiz performance, quick stats (total attempts, average percentage, top score), profile overview, and recent activity.
- **Browse & Search Quizzes**: Filter quizzes by categories, search by keyword, with clean server-side pagination.
- **Interactive Quiz Player**:
  - Live countdown timer with automatic form submission when time expires.
  - Real-time question progress counter (*e.g., "X of Y Answered"*).
  - Randomized question ordering per session.
- **Instant Result Breakdown**: View detailed score, percentage badge, and review every question with correct vs user-selected choices.
- **Global Leaderboard**: Live ranking board featuring top learners with rank badges (Gold, Silver, Bronze).
- **Quiz History**: Complete log of all past attempts with result review links.
- **Profile Management**: Update profile details and change account passwords securely.

### 🛡️ Admin Module
- **Admin Dashboard**: Real-time platform metrics (Total Users, Quizzes, Questions, Attempts).
- **Category Management**: Add and delete quiz categories.
- **Quiz Management**: Create, edit, and delete quizzes with custom time limits and target question counts.
- **Question Bank Management**: Manage Multiple Choice Questions (MCQ) for any quiz with options A, B, C, D and correct key selection.
- **User Management**: Inspect registered users and delete user accounts.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask framework, Flask-SQLAlchemy (ORM), Werkzeug (Security & Password Hashing).
- **Database**: MySQL (supported via PyMySQL driver) / SQLite fallback option.
- **Frontend**: HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, JavaScript (ES6+).

---

## 📁 Project Structure

```
Online_Quiz_Application/
│
├── app.py                     # Main Flask application initialization & error handlers
├── config.py                  # Database & application configuration settings
├── seed_data.py               # Script to seed default database tables & 50 sample questions
├── database.sql               # MySQL DDL schema and sample SQL seed statements
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Comprehensive setup and user guide
│
├── models/                    # SQLAlchemy database models
│   ├── __init__.py
│   ├── user.py                # User model with password hashing methods
│   ├── admin.py               # Admin model for administrator authentication
│   ├── quiz.py                # Category & Quiz models
│   ├── question.py            # Question model (MCQ)
│   └── result.py              # Quiz result & scoring model
│
├── routes/                    # Flask Blueprints (Modular Route Handlers)
│   ├── __init__.py
│   ├── auth_routes.py         # Login, registration, and logout routes
│   ├── user_routes.py         # User dashboard, profile edit, password change, history
│   ├── quiz_routes.py         # Browse, search, start, submit quiz, results, leaderboard
│   └── admin_routes.py        # Admin panel, categories, quizzes, questions, user management
│
├── static/                    # Frontend static assets
│   ├── css/
│   │   └── style.css          # Custom styling and modern design system
│   ├── js/
│   │   └── script.js         # Client timer, progress updates, auto-submission
│   └── images/
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Core layout with Bootstrap navigation & footer
│   ├── index.html             # Landing page with hero banner & featured quizzes
│   ├── login.html             # User & Admin tabbed login
│   ├── register.html          # Registration page
│   ├── dashboard.html         # User dashboard
│   ├── quiz_list.html         # Quiz catalog with search and category filters
│   ├── quiz.html              # Quiz execution interface with countdown timer
│   ├── result.html            # Score report & answer key review
│   ├── leaderboard.html       # Platform leaderboard
│   ├── history.html           # User quiz attempt history
│   ├── admin_dashboard.html   # Admin control panel
│   ├── manage_quizzes.html    # Admin quiz CRUD interface
│   ├── manage_questions.html  # Admin question CRUD interface
│   ├── manage_users.html      # Admin user management
│   ├── edit_profile.html      # Profile edit page
│   ├── change_password.html   # Password update page
│   └── error.html             # 404 / 500 error page
│
└── utils/                     # Utility functions & helpers
    ├── __init__.py
    └── helpers.py             # Login & Admin authentication decorator functions
```

---

## ⚡ Quick Setup & Installation Guide

### Prerequisites
- Python 3.8+ installed on your computer.
- MySQL Server (e.g. MySQL Community Server, XAMPP, or WAMP) installed and running.

---

### Step 1: Clone or Extract Project
Extract the ZIP package or navigate to the project directory:
```bash
cd Online_Quiz_Application
```

### Step 2: Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Settings
1. Create a MySQL database named `online_quiz_db`:
   ```sql
   CREATE DATABASE online_quiz_db;
   ```
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Update `.env` with your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=online_quiz_db
   ```
*(Note: If no MySQL credentials are provided, the app can automatically fall back to SQLite `online_quiz.db` for instant offline testing!)*

### Step 5: Initialize & Seed Database
You can initialize the database tables and populate the 5 sample quizzes with 50 MCQ questions using either method below:

**Method A (Python Seed Script - Recommended):**
```bash
python seed_data.py
```

**Method B (MySQL Command Line / Workbench Import):**
Import the provided `database.sql` script into your MySQL database.

---

### Step 6: Run the Flask Application
```bash
python app.py
```
Open your browser and visit: **`http://127.0.0.1:5000`**

---

## 🔑 Default Credentials

### 🛡️ Admin Account
- **URL**: `http://127.0.0.1:5000/admin/login`
- **Username**: `pranith0708`
- **Password**: `mrec2024`


### 👤 Sample User Account
- **URL**: `http://127.0.0.1:5000/login`
- **Email**: `john@example.com`
- **Password**: `user123`

---

## 📚 Included Pre-populated Quizzes (50 Questions Total)

1. **Python Basics** (10 MCQ questions)
2. **HTML & CSS** (10 MCQ questions)
3. **JavaScript** (10 MCQ questions)
4. **SQL** (10 MCQ questions)
5. **General Aptitude** (10 MCQ questions)

---

## 📄 License
This project is open-source under the MIT License.
