# Deployment 

Deploy the complete service stack locally in minutes:

```bash
# Clone the repository
git clone https://github.com/yourusername/organization-management-service.git
cd organization-management-service

# Start all services with Docker Compose
docker-compose up --build -d

# Verify services are running
curl http://localhost:8000/health
```

## 📋 Prerequisites

### Required Software
- **Docker** & **Docker Compose** (for local deployment)
- **Git** (for source control)
- **Python 3.9+** (for development)

### Verify Installation
```bash
# Check Docker
docker --version
docker-compose --version

# Check Python
python --version
```

## 🐳 Local Deployment with Docker

### Option A: Full Stack (Recommended)
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option B: Development Mode
```bash
# Start only MongoDB
docker-compose up mongodb -d

# Run service in development mode
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Service Ports
| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| API Server | 8000 | http://localhost:8000 | Main API endpoints |
| MongoDB | 27017 | mongodb://localhost:27017 | Database |
| API Docs | 8000 | http://localhost:8000/docs | Interactive API documentation |

## ☁️ Cloud Deployment on Render (Free Tier)

### Step 1: Prepare Your Repository
1. Ensure all required files exist:
   - `main.py` (FastAPI application)
   - `requirements.txt` (Python dependencies)
   - `Dockerfile` (Container configuration)
   - `render.yaml` (Optional: Render configuration)

2. Push final code to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Set Up MongoDB Atlas (Free)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a **FREE M0 cluster**
3. Configure network access: Add IP `0.0.0.0/0` (temporarily)
4. Create database user
5. Get connection string:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
   ```

### Step 3: Deploy to Render
1. **Sign up** at [Render](https://render.com) (GitHub login recommended)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure service:

| Setting | Value |
|---------|-------|
| **Name** | `organization-management-service` |
| **Environment** | `Docker` |
| **Plan** | `Free` |
| **Region** | `Oregon (US West)` or closest |
| **Branch** | `main` |

5. **Add Environment Variable:**
   - Key: `MONGODB_URI`
   - Value: Your MongoDB Atlas connection string

6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment

### Step 4: Verify Deployment
```bash
# Test your deployed service
curl https://organization-management-service.onrender.com/health

# Expected response:
{"status":"healthy","database":"connected","service":"Organization Management Service"}
```

## 🔧 Manual Deployment (Without Docker)

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# MONGODB_URI=mongodb://localhost:27017/organization_db
```

### 3. Start MongoDB
```bash
# Using Docker (easiest)
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or install MongoDB locally
# Follow official MongoDB installation guide
```

### 4. Run the Application
```bash
# Development mode (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGODB_URI` | Yes | `mongodb://localhost:27017` | MongoDB connection string |
| `DATABASE_NAME` | No | `organization_db` | Database name |
| `API_PREFIX` | No | `/api/v1` | API path prefix |
| `DEBUG` | No | `False` | Enable debug mode |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## 📦 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_DATABASE=organization_db

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/organization_db
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  mongodb_data:
```

## 🧪 Testing the Deployment

### Health Check
```bash
# Local
curl http://localhost:8000/health

# Render
curl https://organization-management-service.onrender.com/health
```

### Create Test Organization
```bash
curl -X POST http://localhost:8000/organizations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Corp",
    "description": "Test organization",
    "industry": "Technology",
    "employee_count": 10
  }'
```

### List Organizations
```bash
curl http://localhost:8000/organizations
```

## 🔍 Troubleshooting

### Common Issues

1. **Port 8000 already in use**
```bash
# Find and kill process
sudo lsof -i :8000
sudo kill -9 <PID>

# Or use different port
uvicorn main:app --host 0.0.0.0 --port 8001
```

2. **Cannot connect to MongoDB**
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Test MongoDB connection
mongosh "mongodb://localhost:27017"
```

3. **Render deployment fails**
- Check Render logs in dashboard
- Verify `requirements.txt` is correct
- Ensure `MONGODB_URI` environment variable is set

4. **Docker build fails**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

### Logs Inspection
```bash
# Docker Compose logs
docker-compose logs -f

# Specific service logs
docker-compose logs api
docker-compose logs mongodb

# Render logs (via dashboard)
# Navigate to your service → Logs
```

## 📊 Monitoring

### Health Endpoints
- `GET /health` - Service and database health
- `GET /metrics` - Prometheus metrics (if configured)
- `GET /docs` - API documentation

### Log Files
- Application logs: `logs/app.log`
- Error logs: `logs/error.log`
- Access logs: `logs/access.log`

## 🔄 Update Deployment

### Local Update
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Render Update
- Push to GitHub: `git push origin main`
- Render automatically redeploys
- Monitor deployment in Render dashboard

## 🗑️ Cleanup

### Local Cleanup
```bash
# Stop and remove containers
docker-compose down -v

# Remove Docker images
docker rmi organization-management-service_api

# Remove unused resources
docker system prune
```

### Render Cleanup
1. Go to Render dashboard
2. Navigate to your web service
3. Click "Settings" → "Delete Service"

## 📞 Support
For deployment issues:
1. Check logs: `docker-compose logs`
2. Verify environment variables
3. Ensure ports are available
4. Contact team if issues persist

## 📚 Additional Resources
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Docker Documentation](https://docs.docker.com/)
- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas Guide](https://www.mongodb.com/docs/atlas/)
</div>

