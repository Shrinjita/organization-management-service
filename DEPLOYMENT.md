# Deployment Guide

## Prerequisites

### Development
- Python 3.9+
- MongoDB 4.4+
- Git

### Production
- Docker & Docker Compose
- NGINX (optional, for reverse proxy)
- SSL certificates (for HTTPS)

## Local Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd organization-management-service
2. Set Up Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Configure Environment
bash
cp .env.example .env
# Edit .env with your configuration
5. Start MongoDB
bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:6

# Or install MongoDB locally
# Follow MongoDB installation guide for your OS
6. Run Application
bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
7. Access Application
API: http://localhost:8000

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc