# Travel Booking Application - Django Backend

A comprehensive travel booking system built with Django and MySQL, featuring user authentication, travel option management, and booking functionality.

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

## Quick Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   # Create MySQL database
   mysql -u root -p
   CREATE DATABASE travel_booking_db;
   exit
   ```

5. **Environment Configuration**
   ```bash
   # Copy environment file
   cp .env.example .env
   
   # Edit .env with your database credentials
   nano .env
   ```

6. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000`

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `GET/PUT /api/accounts/profile/` - User profile

### Travel Options
- `GET /api/travel-options/` - List travel options
- `GET /api/travel-options/{id}/` - Travel option details
- `POST /api/travel-options/search/` - Advanced search

### Bookings
- `GET /api/bookings/` - User's bookings
- `POST /api/bookings/create/` - Create booking
- `GET /api/bookings/{id}/` - Booking details
- `POST /api/bookings/{id}/cancel/` - Cancel booking

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DB_NAME=travel_booking_db
DB_USER=root
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=3306

# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
```

## Database Models

### CustomUser
Extended Django user model with additional fields:
- Phone number
- Date of birth
- Address
- Profile picture

### TravelOption
Core travel information:
- Travel ID, type (Flight/Train/Bus)
- Source and destination
- Schedule (departure/arrival times)
- Pricing and seat information
- Operator details and amenities

### Booking
Booking management:
- Unique booking ID
- User and travel option references
- Seat quantity and total price
- Booking status and dates
- Passenger details and contact information

## Testing

Run the test suite:
```bash
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
```

## Admin Interface

Access the admin interface at `http://127.0.0.1:8000/admin/` with your superuser credentials.

Features:
- User management
- Travel option management
- Booking oversight
- Advanced filtering and search

## Production Deployment

### AWS Deployment
1. Set up EC2 instance with Ubuntu
2. Install required packages
3. Configure MySQL RDS
4. Set up environment variables
5. Configure web server (nginx + gunicorn)

### PythonAnywhere Deployment
1. Upload code to PythonAnywhere
2. Set up virtual environment
3. Configure MySQL database
4. Update WSGI configuration
5. Set environment variables

## API Documentation

### Search Travel Options
```bash
curl -X POST http://localhost:8000/api/travel-options/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "source": "New York",
    "destination": "Los Angeles",
    "type": "FLIGHT",
    "departure_date": "2024-12-01"
  }'
```

### Create Booking
```bash
curl -X POST http://localhost:8000/api/bookings/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-auth-token" \
  -d '{
    "travel_option_id": 1,
    "number_of_seats": 2,
    "contact_email": "user@example.com",
    "contact_phone": "1234567890"
  }'
```

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused

### Database
- Use migrations for all schema changes
- Add appropriate indexes for query optimization
- Use database constraints for data integrity

### Security
- Validate all user inputs
- Use Django's built-in security features
- Keep sensitive data in environment variables
- Regular security updates

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Check database credentials in `.env`
   - Ensure MySQL service is running
   - Verify database exists

2. **Migration Issues**
   - Delete migration files and recreate: `python manage.py makemigrations --empty appname`
   - Reset migrations: `python manage.py migrate --fake appname zero`

3. **Permission Errors**
   - Check user permissions in MySQL
   - Verify file permissions for media uploads

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.