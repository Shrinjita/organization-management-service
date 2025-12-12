# Organization Management Service

- **Multi-tenant Architecture**: Master database for metadata with dynamic collections per organization
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Organization CRUD**: Create, read, update, and delete organizations
- **Dynamic Collection Creation**: Automatically creates MongoDB collections for each organization
- **Admin Management**: Admin users with organization-specific permissions
- **RESTful APIs**: Clean, well-documented API endpoints
- **Production Ready**: Error handling, logging, and validation

## ✨ Features

- **🚀 FastAPI Backend**: High-performance API with automatic OpenAPI documentation
- **📊 MongoDB Database**: Flexible NoSQL database for organizational data
- **🐳 Docker Support**: Containerized deployment with Docker Compose
- **☁️ Cloud Ready**: Easy deployment to Render (free tier)
- **🔍 Search & Filter**: Advanced organization search capabilities
- **✅ Input Validation**: Built-in validation with Pydantic
- **🧪 Testing**: Comprehensive test suite with pytest
- **📈 Health Checks**: Service monitoring endpoints
- **🔐 Authentication Ready**: JWT authentication prepared

## 🏗️ Architecture

```
organization-management-service/
├── src/                    # Source code
│   ├── models/            # Pydantic models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   └── database.py        # Database connection
├── tests/                 # Test suite
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-container setup
└── README.md           # This file
```

<img width="550" height="483" alt="_- visual selection (2)" src="https://github.com/user-attachments/assets/fb0d27ad-8678-491d-95c2-b41f023cfacc" />

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose (for containerized deployment)
- Git

### Local Development

#### Option 1: Using Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/organization-management-service.git
cd organization-management-service

# Start all services
docker-compose up --build -d

# Verify services are running
curl http://localhost:8000/health
# Expected: {"status":"healthy","database":"connected","service":"Organization Management Service"}
```

#### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start MongoDB (requires Docker)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/organizations` | List all organizations |
| `POST` | `/organizations` | Create new organization |
| `GET` | `/organizations/{id}` | Get organization by ID |
| `PUT` | `/organizations/{id}` | Update organization |
| `DELETE` | `/organizations/{id}` | Delete organization |
| `GET` | `/organizations/search` | Search organizations |
| `GET` | `/organizations/stats` | Get statistics |

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🐳 Docker Deployment

### Build and Run
```bash
# Build Docker image
docker build -t organization-service .

# Run container
docker run -p 8000:8000 --env-file .env organization-service
```

### Docker Compose
```bash
# Development (with hot reload)
docker-compose up --build

# Production
docker-compose -f docker-compose.yml up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Deploy to Render (Free)

1. **Push code to GitHub**
2. **Create MongoDB Atlas database** (free M0 tier)
3. **Deploy to Render**:
   - Sign up at [render.com](https://render.com)
   - New Web Service → Connect GitHub repo
   - Environment: Docker, Plan: Free
   - Add `MONGODB_URI` environment variable
4. **Access your service**: `https://your-service.onrender.com`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_organizations.py -v
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017/organization_db
DATABASE_NAME=organization_db
DEBUG=True
LOG_LEVEL=INFO
```

### Application Settings
- **Port**: 8000 (configurable via `PORT` env variable)
- **Database**: MongoDB (local or Atlas)
- **Logging**: Structured JSON logging in production

## 📁 Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── organization.py    # Organization Pydantic models
│   │   └── response.py        # API response models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── organizations.py   # Organization endpoints
│   │   └── health.py          # Health check endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   └── organization_service.py  # Business logic
│   └── database.py            # MongoDB connection setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test fixtures
│   ├── test_organizations.py  # Organization tests
│   └── test_health.py         # Health endpoint tests
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Multi-service setup
├── pytest.ini                 # Test configuration
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use meaningful commit messages

## 🐛 Troubleshooting

### Common Issues

**Port 8000 already in use:**
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill the process
sudo kill -9 <PID>
```

**Cannot connect to MongoDB:**
```bash
# Check if MongoDB is running
docker ps | grep mongo
# Start MongoDB if not running
docker start mongodb
```

**Docker build fails:**
```bash
# Clear Docker cache
docker system prune -a
# Rebuild
docker-compose build --no-cache
```

### Logs
```bash
# Application logs
docker-compose logs api

# Database logs
docker-compose logs mongodb

# Follow logs in real-time
docker-compose logs -f
```

## 📊 API Examples

### Create Organization
```bash
curl -X POST http://localhost:8000/organizations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Innovations Inc.",
    "description": "A leading technology company",
    "industry": "Technology",
    "founded_year": 2018,
    "employee_count": 250,
    "location": "San Francisco, CA",
    "website": "https://techinnovations.example.com"
  }'
```

### List Organizations
```bash
curl http://localhost:8000/organizations
```

### Search Organizations
```bash
curl "http://localhost:8000/organizations/search?industry=Technology&min_employees=100"
```

## 🔒 Security

- Input validation with Pydantic
- CORS middleware enabled
- Environment-based configuration
- Secure database connections
- Prepared for JWT authentication

## 📈 Performance

- Async database operations
- Connection pooling
- Efficient query design
- Caching ready architecture


## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [MongoDB](https://www.mongodb.com/) for the database
- [Render](https://render.com/) for free hosting
- [Docker](https://www.docker.com/) for containerization
