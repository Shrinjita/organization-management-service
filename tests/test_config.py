import os
os.environ["TEST_MODE"] = "true"
os.environ["DEBUG"] = "true"
os.environ["MONGODB_URI"] = "mongodb://localhost:27017"
os.environ["MASTER_DB_NAME"] = "test_organization_master"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"