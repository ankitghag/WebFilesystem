Project Overview :
WebFilesystem is a FastAPI-based backend API for managing user files and folders in a cloud-backed filesystem. It solves the problem of securely storing, organizing, and managing files through REST APIs, using PostgreSQL for metadata, Redis for background processing, and Cloudflare R2/S3-compatible storage for files.Authentication is handled with JWT access tokens and refresh-token cookies. 

Features
- User registration and secure sign-in
- JWT-based access tokens with refresh-token support
- Create and manage folders
- Upload and retrieve files through S3-compatible storage
- Move files and folders within the filesystem
- Delete files, empty folders, or folders recursively
- File and folder permission management
- User group creation for access management
- PostgreSQL-based filesystem metadata storage
- Redis-based queueing for background file-processing tasks
- Interactive API documentation through FastAPI Swagger UI (/docs)

Tech Stack
Backend: Python 3.11, FastAPI
Database: PostgreSQL, SQLAlchemy (async), asyncpg
Cache & Queue: Redis
Object Storage: Cloudflare R2 (S3-compatible)
Authentication: JWT, bcrypt
Validation: Pydantic
Containerization: Docker
Server: Uvicorn

Prerequisites
Before running the project, make sure you have:
Python 3.11+
PostgreSQL
Redis
Cloudflare R2 or any S3-compatible storage
Git
Optional: Docker, if you want to run the application in a container.
