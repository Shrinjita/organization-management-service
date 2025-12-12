from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="organization-management-service",
    version="1.0.0",
    author="Organization Management Service Team",
    author_email="team@example.com",
    description="Multi-tenant backend service with dynamic MongoDB collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/organization-management-service",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Backend Services",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pymongo==4.5.0",
        "python-dotenv==1.0.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "httpx==0.25.2",
            "black==23.11.0",
            "flake8==6.1.0",
            "mypy==1.7.0",
        ],
        "test": [
            "pytest==7.4.3",
            "httpx==0.25.2",
            "pytest-asyncio==0.21.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "org-service=main:main",
        ],
    },
)