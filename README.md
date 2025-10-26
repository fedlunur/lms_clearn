# LMS Backend

Backend for the Learning Management System (LMS) built with Django and PostgreSQL.

---

## Features

- Django REST API for managing courses, users, and grading.
- JWT Authentication with token blacklisting.
- PostgreSQL database support.
- CORS enabled for frontend integration.
- Admin panel customization using Jazzmin.

---

## Prerequisites

- Python 3.12+
- PostgreSQL
- Git
- (Optional) pgAdmin for database management

---

## Setup Instructions

1. **Install PostgreSQL**  
   - Download and install from [PostgreSQL Official Site](https://www.postgresql.org/download/).  

2. **(Optional) Install pgAdmin**  
   - Provides a GUI to manage your PostgreSQL databases.  

3. **Create Database and Role**  
   Open `psql` or pgAdmin and run:
   ```sql
   CREATE ROLE lms WITH LOGIN PASSWORD 'your_password';
   CREATE DATABASE lms OWNER lms;
