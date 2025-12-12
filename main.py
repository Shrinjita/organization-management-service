from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.logging_middleware import LoggingMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/app.log')
    ]
)

logger = logging.getLogger(__name__)

# Import routers
from src.routes import auth_router, organization_router
from src.db.mongo import mongo_manager
from src.models.organization import OrganizationModel
from src.models.admin_user import AdminUserModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting Organization Management Service...")
    
    try:
        # Initialize database connections
        mongo_manager.get_client()
        
        # Create indexes
        OrganizationModel.create_indexes()
        AdminUserModel.create_indexes()
        
        logger.info("✅ Database initialized and indexes created")
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection error: {str(e)}")
        # DO NOT RAISE - let service start in degraded mode
        # This allows health endpoint to show "disconnected" status
    
    yield
    
    # Shutdown
    logger.info("Shutting down Organization Management Service...")
    mongo_manager.close_connection()
    logger.info("✅ Clean shutdown completed")

# Create FastAPI app
app = FastAPI(
    title="Organization Management Service",
    description="Multi-tenant backend service with dynamic MongoDB collections",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(auth_router)
app.include_router(organization_router)

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Organization Management Service is running",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity test"""
    try:
        # Test database connection
        client = mongo_manager.get_client()
        client.admin.command('ping')
        
        return {
            "status": "healthy",
            "database": "connected",
            "service": "Organization Management Service"
        }
    except Exception as e:
        logger.warning(f"⚠️ Health check: Database disconnected: {str(e)}")
        return JSONResponse(
            status_code=200,  # Still return 200, but show disconnected
            content={
                "status": "degraded",
                "database": "disconnected",
                "service": "Organization Management Service",
                "error": str(e)
            }
        )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )