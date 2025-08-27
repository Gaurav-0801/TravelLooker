# Travel Booking Application

A comprehensive travel booking system built with Django, MySQL, Vite, React, and Tailwind CSS, featuring user authentication, travel option management, and booking functionality.

## Features

### 🔐 User Management
- User registration, login, and logout  
- Profile management with additional fields  
- Django's built-in authentication system  
- REST API authentication with tokens  

### ✈️ Travel Options
- Support for flights, trains, and buses  
- Comprehensive travel information (source, destination, schedule, pricing)  
- Advanced search and filtering capabilities  
- Seat availability management  

### 📅 Booking System
- Create, view, and manage bookings  
- Automatic seat allocation  
- Booking confirmation and cancellation  
- Passenger details management  
- Booking status tracking  

### 🛠️ Technical Features
- MySQL database integration  
- REST API endpoints  
- Input validation and error handling  
- Unit tests for critical features  
- Admin interface for management  

---

## Quick Setup

### Prerequisites
- Python 3.8+  
- MySQL 5.7+  
- Node.js & npm  

### Backend Setup (Django)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd backend
Create virtual environment

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Database Setup

# Log in to MySQL
mysql -u root -p

# Create database
CREATE DATABASE travel_booking_db;

exit


Environment Configuration

# Copy example environment file
cp .env.example .env
# Edit .env with your database credentials
nano .env


Run Migrations

python manage.py makemigrations
python manage.py migrate


Create Superuser

python manage.py createsuperuser


Start Development Server

python manage.py runserver


The backend will be available at http://127.0.0.1:8000.

Frontend Setup (Vite + React)

Navigate to the root project folder:

cd <project-root>


Install dependencies:

npm install


Start the development server:

npm run dev

API Endpoints
Authentication

POST /api/accounts/register/ - User registration

POST /api/accounts/login/ - User login

POST /api/accounts/logout/ - User logout

GET/PUT /api/accounts/profile/ - User profile

Travel Options

GET /api/travel-options/ - List travel options

GET /api/travel-options/{id}/ - Travel option details

POST /api/travel-options/search/ - Advanced search

Bookings

GET /api/bookings/ - User's bookings

POST /api/bookings/create/ - Create booking

GET /api/bookings/{id}/ - Booking details

POST /api/bookings/{id}/cancel/ - Cancel booking

Environment Variables

Create a .env file with the following:

# Database Configuration
DB_NAME=travel_booking_db
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=3306

# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True

Database Models
CustomUser

Extended Django user model with additional fields:

Phone number

Date of birth

Address

Profile picture

TravelOption

Core travel information:

Travel ID, type (Flight/Train/Bus)

Source and destination

Schedule (departure/arrival times)

Pricing and seat information

Operator details and amenities

Booking

Booking management:

Unique booking ID

User and travel option references

Seat quantity and total price

Booking status and dates

Passenger details and contact information

Testing

Run the test suite:

# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test travel_options
python manage.py test bookings

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report

Admin Interface

Access at http://127.0.0.1:8000/admin/ with your superuser credentials.

Features:

User management

Travel option management

Booking oversight

Advanced filtering and search

Production Deployment
AWS Deployment

Set up EC2 instance with Ubuntu

Install required packages

Configure MySQL RDS

Set up environment variables

Configure web server (nginx + gunicorn)

PythonAnywhere Deployment

Upload code to PythonAnywhere

Set up virtual environment

Configure MySQL database

Update WSGI configuration

Set environment variables

Development Guidelines
Code Style

Follow PEP 8 guidelines

Use meaningful variable names

Add docstrings to functions and classes

Keep functions small and focused

Database

Use migrations for all schema changes

Add appropriate indexes for query optimization

Use database constraints for data integrity

Security

Validate all user inputs

Use Django's built-in security features

Keep sensitive data in environment variables

Regular security updates

Troubleshooting
Common Issues

MySQL Connection Error

Check database credentials in .env

Ensure MySQL service is running

Verify database exists

Migration Issues

Delete migration files and recreate:

python manage.py makemigrations --empty appname


Reset migrations:

python manage.py migrate --fake appname zero


Permission Errors

Check user permissions in MySQL

Verify file permissions for media uploads

Contributing

Fork the repository

Create a feature branch

Add tests for new functionality

Ensure all tests pass

Submit a pull request

License

This project is licensed under the MIT License.


This is the **full README** for your project.  

If you want, I can also make a **`.gitignore` for both Django backend and Vite frontend** so your `venv`, build files, and other unnecessary files are excluded. This will help avoid Git warnings you saw earlier.  

Do you want me to make that too?
