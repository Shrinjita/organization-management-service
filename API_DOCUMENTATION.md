# Organization Management Service API Documentation

The Organization Management Service is a RESTful API built with FastAPI for managing organizational data with MongoDB as the database.

## 🌐 Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://your-render-url.onrender.com`

## 🏥 Health Check
**GET `/health`**
Check service and database connectivity.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "service": "Organization Management Service"
}
```

## 🏢 Organizations Endpoints

### 📋 List Organizations
**GET `/organizations`**
Retrieve all organizations with optional pagination.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Response (200 OK):**
```json
[
  {
    "_id": "string",
    "name": "string",
    "description": "string",
    "industry": "string",
    "founded_year": 2023,
    "employee_count": 50,
    "location": "string",
    "website": "string",
    "created_at": "2023-12-13T10:30:00Z",
    "updated_at": "2023-12-13T10:30:00Z"
  }
]
```

### ➕ Create Organization
**POST `/organizations`**
Create a new organization.

**Request Body:**
```json
{
  "name": "Acme Corp",
  "description": "A technology company",
  "industry": "Technology",
  "founded_year": 2020,
  "employee_count": 150,
  "location": "San Francisco, CA",
  "website": "https://acme.example.com"
}
```

**Response (201 Created):**
```json
{
  "message": "Organization created successfully",
  "organization_id": "507f1f77bcf86cd799439011"
}
```

### 🔍 Get Organization by ID
**GET `/organizations/{organization_id}`**
Retrieve a specific organization.

**Response (200 OK):**
```json
{
  "_id": "string",
  "name": "string",
  "description": "string",
  "industry": "string",
  "founded_year": 2023,
  "employee_count": 50,
  "location": "string",
  "website": "string",
  "created_at": "2023-12-13T10:30:00Z",
  "updated_at": "2023-12-13T10:30:00Z"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Organization not found"
}
```

### ✏️ Update Organization
**PUT `/organizations/{organization_id}`**
Update an existing organization.

**Request Body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "industry": "Updated Industry",
  "employee_count": 200
}
```

**Response (200 OK):**
```json
{
  "message": "Organization updated successfully"
}
```

### 🗑️ Delete Organization
**DELETE `/organizations/{organization_id}`**
Delete an organization.

**Response (200 OK):**
```json
{
  "message": "Organization deleted successfully"
}
```

## 🔍 Search & Filter
**GET `/organizations/search`**
Search organizations with various filters.

**Query Parameters:**
- `name` (optional): Partial name match
- `industry` (optional): Exact industry match
- `min_employees` (optional): Minimum employee count
- `max_employees` (optional): Maximum employee count
- `location` (optional): Partial location match

## 📊 Statistics
**GET `/organizations/stats`**
Get organization statistics.

**Response:**
```json
{
  "total_organizations": 150,
  "industries": ["Technology", "Healthcare", "Finance"],
  "average_employee_count": 85.5,
  "latest_organization": "2023-12-13T10:30:00Z"
}
```

## 🧪 Testing
**GET `/test/health`**
Test endpoint for health checks.

**Response:**
```json
{
  "status": "test_healthy",
  "timestamp": "2023-12-13T10:30:00Z"
}
```

## 📚 API Documentation
- **Interactive API Docs**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc` (ReDoc)
- **OpenAPI Schema**: `/openapi.json`

## 🔒 Authentication & Authorization
*Note: Currently uses basic API key authentication. Future versions will implement JWT.*

## 🚨 Error Responses
All endpoints may return:

**400 Bad Request:**
```json
{
  "detail": "Validation error description"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error occurred"
}
```

## 📈 Rate Limiting
- Free tier: 100 requests/hour per IP
- Production: 1000 requests/hour per API key

## 🗂️ Data Models

### Organization
```typescript
{
  _id: ObjectId;
  name: string;
  description: string;
  industry: string;
  founded_year: number;
  employee_count: number;
  location: string;
  website: string;
  created_at: ISO8601;
  updated_at: ISO8601;
}
```

### API Health
```typescript
{
  status: "healthy" | "unhealthy";
  database: "connected" | "disconnected";
  service: string;
  timestamp: ISO8601;
}
```

