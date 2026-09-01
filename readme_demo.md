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


Installation
1. Clone the repository
git clone <your-repository-url>
cd webfilesystem
2. Create and activate a virtual environment
python -m venv .venv
Windows PowerShell:
.venv\Scripts\Activate.ps1
macOS/Linux:
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables
Copy the example configuration file:
Windows:
Copy-Item .env_demo .env
macOS/Linux:
cp .env_demo .env
Update .env with your PostgreSQL, Redis, and S3-compatible storage credentials:
API_V1_STR=/api/v1
SECRET_KEY=replace-with-a-secure-random-value
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=10080
ALGORITHM=HS256
JWT_AUDIENCE=*
JWT_ISSUER=http://localhost:8000

USERDATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DATABASE
redis_url=redis://HOST:6379/0

aws_access_key_id=YOUR_ACCESS_KEY
aws_secret_key=YOUR_SECRET_KEY
s3api=https://YOUR-S3-COMPATIBLE-ENDPOINT
5. Set up the database
Create the PostgreSQL database and the filesys schema with the required tables (users, fs_node, groups, user_groups, and refresh_tokens).
The repository currently does not include migrations or a database initialization script, so this schema must be created before starting the application.

6. Start the application
python main.py
The API will be available at http://127.0.0.1:8000, with interactive documentation at http://127.0.0.1:8000/docs.