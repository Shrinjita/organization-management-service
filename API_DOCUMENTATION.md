# Organization Management Service API Documentation

## Base URL
http://localhost:8000

text

## Authentication
All endpoints except `/admin/login` require JWT authentication.

### Headers
Authorization: Bearer <jwt_token>

text

## Endpoints

### 1. Authentication

#### POST `/admin/login`
Admin login to obtain JWT token.

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "SecurePass123"
}
Response:

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "organization_id": "6578a1b2c3d4e5f6a7b8c9d0",
  "admin_id": "6578a1b2c3d4e5f6a7b8c9d1",
  "organization_name": "ExampleOrg"
}
2. Organization Management
POST /org/create
Create a new organization.

Request Body:

json
{
  "organization_name": "ExampleOrg",
  "email": "admin@example.com",
  "password": "SecurePass123"
}
Response:

json
{
  "id": "6578a1b2c3d4e5f6a7b8c9d0",
  "organization_name": "ExampleOrg",
  "collection_name": "org_exampleorg",
  "admin_email": "admin@example.com",
  "admin_id": "6578a1b2c3d4e5f6a7b8c9d1",
  "created_at": "2024-01-01T12:00:00Z"
}
GET /org/get
Get organization details by name.

Query Parameters:

org_name: Organization name

Response:

json
{
  "id": "6578a1b2c3d4e5f6a7b8c9d0",
  "organization_name": "ExampleOrg",
  "collection_name": "org_exampleorg",
  "admin_email": "admin@example.com",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
PUT /org/update
Update organization details.

Request Body:

json
{
  "organization_name": "ExampleOrg",
  "new_organization_name": "UpdatedOrg",
  "email": "newadmin@example.com",
  "password": "NewPass123"
}
Response:

json
{
  "message": "Organization updated successfully",
  "organization_name": "UpdatedOrg",
  "collection_name": "org_updatedorg",
  "admin_email": "newadmin@example.com"
}
DELETE /org/delete
Delete an organization.

Request Body:

json
{
  "organization_name": "ExampleOrg"
}
Response:

json
{
  "message": "Organization 'ExampleOrg' deleted successfully"
}
3. Health & System
GET /
Root endpoint - API health check.

Response:

json
{
  "message": "Organization Management Service is running",
  "status": "healthy",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
GET /health
Health check with database connectivity.

Response:

json
{
  "status": "healthy",
  "database": "connected",
  "service": "Organization Management Service"
}
Error Responses
400 Bad Request
json
{
  "detail": "Organization 'ExampleOrg' already exists"
}
401 Unauthorized
json
{
  "detail": "Invalid authentication credentials"
}
403 Forbidden
json
{
  "detail": "Access denied to this organization"
}
404 Not Found
json
{
  "detail": "Organization 'ExampleOrg' not found"
}
500 Internal Server Error
json
{
  "detail": "Internal server error"
}
Rate Limiting
Currently not implemented. In production, consider implementing rate limiting.

Versioning
API versioning will be implemented via URL path:

v1/ for version 1 (current)

Future versions will use v2/, v3/, etc.

text

## **Step 52: Create architecture diagram file**
**Action:** Create architecture diagram
**VS Code:** Explorer → New File → "ARCHITECTURE.md"
**Content:**
```markdown
# System Architecture

## High-Level Architecture
┌─────────────────────────────────────────────────────────────┐
│ Client Applications │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Web App │ │ Mobile App │ │ CLI Tool │ │
│ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ │
└─────────┼─────────────────┼─────────────────┼───────────────┘
│ │ │
└─────────────────┼─────────────────┘
│
┌──────────────────▼──────────────────┐
│ Load Balancer (NGINX) │
└──────────────────┬──────────────────┘
│
┌──────────────────▼──────────────────┐
│ FastAPI Application Servers │
│ ┌─────────────┐ ┌─────────────┐ │
│ │ Worker 1 │ │ Worker N │ │
│ └──────┬──────┘ └──────┬──────┘ │
└─────────┼─────────────────┼─────────┘
│ │
┌─────────▼─────────────────▼─────────┐
│ Master Database │
│ (MongoDB Cluster) │
│ ┌──────────────────────────────┐ │
│ │ organizations collection │ │
│ │ admin_users collection │ │
│ │ org_* dynamic collections │ │
│ └──────────────────────────────┘ │
└─────────────────────────────────────┘

text

## Component Details

### 1. FastAPI Application Layer
- **Framework**: FastAPI with async/await support
- **Authentication**: JWT-based with HTTP Bearer tokens
- **Validation**: Pydantic models for request/response validation
- **Middleware**: CORS, Logging, Error Handling
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### 2. Database Layer
- **Primary Database**: MongoDB (document-oriented)
- **Master Database**: Contains metadata and admin credentials
- **Dynamic Collections**: Created per organization with pattern `org_<name>`
- **Indexes**: Optimized for frequent queries

### 3. Service Layer
- **OrganizationService**: Business logic for organization management
- **AdminService**: Authentication and admin management
- **ValidationService**: Input validation and sanitization

### 4. Data Flow

#### Organization Creation:
1. Client sends POST `/org/create` with organization details
2. Service validates input and checks for duplicates
3. Creates admin user record with hashed password
4. Creates organization metadata record
5. Creates dynamic collection for the organization
6. Returns success response with organization ID

#### Admin Authentication:
1. Client sends POST `/admin/login` with credentials
2. Service verifies email and password hash
3. Generates JWT token with admin and organization info
4. Returns token for subsequent authenticated requests

## Scalability Considerations

### Horizontal Scaling
- Stateless application servers allow easy scaling
- MongoDB sharding for database scalability
- Load balancer distributes traffic across instances

### Multi-Tenancy
- Each organization gets isolated data collection
- No data mixing between organizations
- Collection naming convention prevents conflicts

### Security
- Password hashing with bcrypt
- JWT tokens for stateless authentication
- Input validation and sanitization
- HTTPS enforcement in production

## Deployment Options

### Option 1: Docker Compose (Development)
docker-compose up -d

text

### Option 2: Kubernetes (Production)
- Deployment with multiple replicas
- ConfigMaps for environment variables
- Secrets for sensitive data
- Horizontal Pod Autoscaler

### Option 3: Serverless
- AWS Lambda with API Gateway
- MongoDB Atlas for managed database
- Reduced operational overhead

## Monitoring & Observability

### Logging
- Structured JSON logs
- Request/response logging
- Error tracking
- Performance metrics

### Metrics
- Request rate and latency
- Database query performance
- Memory and CPU usage
- Error rates

### Alerting
- Service downtime
- High error rates
- Performance degradation
- Security incidents