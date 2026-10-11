# Project Overview :

WebFilesystem is a FastAPI-based backend API for managing user files and folders in a cloud-backed filesystem. It solves the problem of securely storing, organizing, and managing files through REST APIs, using PostgreSQL for metadata, Redis for background processing, and Cloudflare R2/S3-compatible storage for files.Authentication is handled with JWT access tokens and refresh-token cookies.

## Features

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
- Interactive API documentation through FastAPI Swagger UI (`/docs`)

## Tech Stack

- Backend: Python 3.11, FastAPI
- Database: PostgreSQL, SQLAlchemy (async), asyncpg
- Cache & Queue: Redis
- Object Storage: Cloudflare R2 (S3-compatible)
- Authentication: JWT, bcrypt
- Validation: Pydantic
- Containerization: Docker
- Server: Uvicorn

## Prerequisites

Before running the project, make sure you have:

- Python 3.11+
- PostgreSQL
- Redis
- Cloudflare R2 or any S3-compatible storage
- Git
- Optional: Docker, if you want to run the application in a container.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd webfilesystem
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example configuration file:

Windows:

```powershell
Copy-Item .env_demo .env
```

macOS/Linux:

```bash
cp .env_demo .env
```

### 5. Set up the database

Create a PostgreSQL database and configure `USERDATABASE_URL` in `.env`.

Create the `filesys` schema and required tables using the SQLAlchemy models defined in:

`app/models/app_model.py`

Database migrations and initialization scripts are not included.

### 6. Start the application

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`, with interactive documentation at `http://127.0.0.1:8000/docs`.

### 7.Run the Background Worker

The application uses a Redis-based background worker to process file-upload tasks.

After starting the API, open a separate terminal, activate the virtual environment, and run:

```bash
python -m app.worker.file_worker
```

Keep this worker running while using file-upload functionality. It reads upload tasks from the Redis queue and updates the file-processing status.

## With Docker

Build the Docker image:

```bash
docker build -t webfilesystem-app .
```

Run the container using your `.env` file:

```bash
docker run --env-file .env -p 8000:8000 webfilesystem-app
```

### Run the Background Worker

```bash
docker run --env-file .env webfilesystem-app python -m app.worker.file_worker
```

The API will be available at:

`http://localhost:8000`

Interactive API documentation:

`http://localhost:8000/docs`

## Authentication

Protected endpoints require a JWT access token. First, create an account using the sign-up endpoint, then sign in to receive an access token.

Include the token in requests using the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

The API also sets a refresh token as an HTTP-only cookie during sign-in. When the access token expires, call the refresh endpoint to obtain a new access token.

## Database Setup

The application uses PostgreSQL for users, filesystem metadata, groups, and refresh tokens.

1. Create a PostgreSQL database.

2. Add the connection URL to `.env`:

```env
USERDATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DATABASE
```

3. Create the `filesys` schema and tables based on the models in `app/models/app_model.py`.

Migration scripts are not included, so the schema must be created manually.


AWS SETUP:

## AWS Deployment Setup

### 1. Launch an EC2 Instance

* **Name:** `WEBFS`
* **Operating system:** Ubuntu 64-bit (x86)
* **Instance type:** `t3.micro`
* **Key pair:** Select an existing key pair or create a new one. If creating a new key pair, select **RSA** as the key pair type and `.pem` as the file format.
* **Security group:** Create a new security group or select an existing one. It should allow SSH, HTTP, and HTTPS traffic.
* **File system:** None

Connect to the instance. A terminal will open.

### 2. Install Docker

Run the following commands:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
newgrp docker
```

### 3. Clone the Repository

```bash
git clone https://github.com/ankitghag/WebFilesystem.git
```

### 4. Create an ElastiCache Cache

* **Engine:** Valkey (recommended)
* **Deployment option:** Serverless
* **Creation method:** New cache

Modify or configure the security group to use the same security group as the EC2 instance.

Copy the cache endpoint and replace the Redis URL in the `.env` file with the endpoint, using the `rediss://` scheme for TLS.

### 5. Configure the Security Group

Add the following inbound rules to the security group attached to both EC2 and ElastiCache:

* **Type:** Custom TCP
* **Ports:** `6379` and `6380`
* **Source:** The security group ID assigned to the EC2 instance and ElastiCache.


### Connect ec2 to elastic cache
sudo apt install -y redis-tools
redis-cli -c -h redis_endpoint -p 6379 --tls