# Organization Management Service

A multi-tenant backend service for managing organizations with dynamic MongoDB collections. Built with FastAPI and MongoDB.

## Features

- **Multi-tenant Architecture**: Master database for metadata with dynamic collections per organization
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Organization CRUD**: Create, read, update, and delete organizations
- **Dynamic Collection Creation**: Automatically creates MongoDB collections for each organization
- **Admin Management**: Admin users with organization-specific permissions
- **RESTful APIs**: Clean, well-documented API endpoints
- **Production Ready**: Error handling, logging, and validation

## Architecture

<img width="550" height="483" alt="_- visual selection (2)" src="https://github.com/user-attachments/assets/fb0d27ad-8678-491d-95c2-b41f023cfacc" />

## 📋 Prerequisites

- Python 3.9 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)
- Git (for version control)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd organization-management-service
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Required: MONGODB_URI, JWT_SECRET_KEY
```

Example `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017
MASTER_DB_NAME=organization_master
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### 5. Start MongoDB (if using local MongoDB)

```bash
# macOS (using Homebrew)
brew services start mongodb-community

# Ubuntu/Debian
sudo systemctl start mongod

# Windows
net start MongoDB
```

### 6. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access the Application

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
organization-management-service/
├── src/
│   ├── config/           # Configuration settings
│   ├── db/              # Database connection and models
│   ├── models/          # Data models and schemas
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── routes/          # API routes
│   ├── utils/           # Utilities (password, JWT, validators)
│   └── middleware/      # Custom middleware
├── tests/               # Test files
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── main.py             # Application entry point
└── README.md           # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /admin/login` - Admin login (returns JWT token)
- `GET /admin/verify` - Verify JWT token

### Organization Management
- `POST /org/create` - Create new organization
- `GET /org/get?organization_name={name}` - Get organization details
- `PUT /org/update` - Update organization details
- `DELETE /org/delete` - Delete organization

### Health & Monitoring
- `GET /health` - Health check endpoint
- `GET /metrics` - Application metrics

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Module

```bash
pytest tests/test_auth.py
pytest tests/test_organization.py
```

### Run Tests with Coverage

```bash
pytest --cov=src --cov-report=html
```

## 🔐 Security Features

- **Password Hashing**: bcrypt with configurable rounds
- **JWT Tokens**: Signed tokens with expiration
- **Input Validation**: Pydantic schemas for all inputs
- **CORS Protection**: Configured CORS middleware
- **Rate Limiting**: Ready for implementation
- **SQL Injection Protection**: MongoDB ObjectId validation
- **Environment Variables**: Sensitive data in environment

## 📊 Database Design

### Master Database Collections

1. **organizations**
   - `_id`: ObjectId
   - `organization_name`: string (unique)
   - `collection_name`: string (unique)
   - `admin_email`: string (unique)
   - `admin_user_id`: ObjectId
   - `created_at`: datetime
   - `updated_at`: datetime

2. **admin_users**
   - `_id`: ObjectId
   - `email`: string (unique)
   - `hashed_password`: string
   - `organization_name`: string
   - `created_at`: datetime
   - `updated_at`: datetime
   - `is_active`: boolean

### Dynamic Collections
- Created per organization: `org_{organization_name_sanitized}`
- Initialized with basic schema
- Can store organization-specific data

## 🚀 Deployment

### Using Docker

```bash
# Build Docker image
docker build -t organization-management-service .

# Run container
docker run -p 8000:8000 --env-file .env organization-management-service
```

### Manual Deployment

1. **Set up production environment variables**
2. **Use production WSGI server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```
3. **Set up reverse proxy** (Nginx/Apache)
4. **Configure SSL/TLS** for HTTPS
5. **Set up monitoring and logging**

## 🔄 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `MASTER_DB_NAME` | Master database name | `organization_master` |
| `JWT_SECRET_KEY` | Secret for JWT token signing | Required |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `DEBUG` | Enable debug mode | `False` |
| `BCRYPT_ROUNDS` | Password hashing rounds | `12` |

## 📈 Monitoring & Logging

- **Application logs**: `logs/app.log`
- **Error logs**: `logs/error.log`
- **Access logs**: `logs/access.log`
- **Health endpoint**: `/health`
- **Metrics endpoint**: `/metrics`

## 🔍 API Examples

### Create Organization
```bash
curl -X POST "http://localhost:8000/org/create" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "TechCorp",
    "email": "admin@techcorp.com",
    "password": "SecurePass123"
  }'
```

### Admin Login
```bash
curl -X POST "http://localhost:8000/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@techcorp.com",
    "password": "SecurePass123"
  }'
```

### Get Organization (with authentication)
```bash
curl -X GET "http://localhost:8000/org/get?organization_name=TechCorp" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB connection failed**
   - Ensure MongoDB is running: `mongod --version`
   - Check connection string in `.env` file
   - Test connection: `mongosh "your_connection_string"`

2. **Port already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

3. **Module not found errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

4. **JWT token validation failed**
   - Ensure `JWT_SECRET_KEY` is set and consistent
   - Check token expiration

### Logs Location
- Application logs: `logs/app.log`
- Error details in console when `DEBUG=True`
