1. Project overview
   - What problem it solves.
   - Brief architecture: FastAPI + PostgreSQL + Redis + S3-compatible storage.
2. Features
   - User sign-up and sign-in
   - JWT access/refresh tokens
   - Create folders and upload files
   - Move/delete filesystem nodes
   - Permission changes and groups
   - Presigned/object-storage file retrieval
3. Tech stack
   - Python 3.11
   - FastAPI / Uvicorn
   - SQLAlchemy async + PostgreSQL (asyncpg)
   - Redis
   - Cloudflare R2 or AWS S3
   - Docker
4. Prerequisites
   - Python 3.11+
   - PostgreSQL database with the filesys schema/tables
   - Redis instance
   - Cloudflare R2 or S3 bucket and credentials
5. Installation
git clone <your-repository-url>
cd webfilesystem

python -m venv .venv
Windows:
.venv\Scripts\Activate.ps1
macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
copy .env_demo .env
Then configure .env:
API_V1_STR=/api/v1
SECRET_KEY=replace-with-a-long-random-secret
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
6. Run locally
python main.py
or:
uvicorn app.main:app --reload
Then use:
- API docs: http://127.0.0.1:8000/docs
- Health/test endpoint: http://127.0.0.1:8000/test
7. Docker
docker build -t webfilesystem-app .
docker run --env-file .env -p 8000:8000 webfilesystem-app
8. API overview
   - POST /api/v1/auth/signup
   - POST /api/v1/auth/signin
   - POST /api/v1/auth/refresh
   - POST /api/v1/user/mkdir
   - POST /api/v1/user/mkfile
   - POST /api/v1/user/rmdir
   - POST /api/v1/user/rmdir/r
   - POST /api/v1/user/rmfile
   - POST /api/v1/user/movenode
   - POST /api/v1/user/node/{node_id}/chmod
   - GET /api/v1/user/getfile/{node_id}
9. Authentication
   - Explain Authorization: Bearer <access-token>.
   - Mention the refresh token is stored in an HTTP-only cookie.
   - Include one signup/signin request example.
10. Database setup
    - State that PostgreSQL tables live under the filesys schema.
    - Add database migration/SQL instructions before publishing, since this repository currently has no migration files or database bootstrap script.
11. Security notes
    - Never commit .env, access keys, JWT secrets, or SSH private keys.
    - .env_demo should contain placeholders only; do not publish real credentials or tokens.
12. Limitations / roadmap
    - Add Alembic migrations
    - Add automated tests
    - Add a Docker Compose setup for PostgreSQL and Redis
    - Document bucket name/configuration explicitly
    - Add CI and API examples