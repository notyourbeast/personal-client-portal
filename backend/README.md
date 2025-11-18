# Freelance ClientHub - Backend Setup

## MongoDB Setup

### Option 1: MongoDB Atlas (Cloud - Recommended)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account and cluster
3. Get your connection string:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
4. Update `.env` file:
   ```env
   MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   MONGO_DB=clienthub
   ```
   Replace `<username>` and `<password>` with your MongoDB Atlas credentials.

5. **Important:** Whitelist your IP address:
   - Go to "Network Access" in MongoDB Atlas
   - Click "Add IP Address"
   - Add `0.0.0.0/0` for development (allows all IPs) or your specific IP

### Option 2: Local MongoDB

1. Install MongoDB locally:
   ```bash
   # macOS
   brew install mongodb-community
   
   # Start MongoDB
   brew services start mongodb-community
   ```

2. Update `.env` file:
   ```env
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=clienthub
   ```

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGO_DB=clienthub
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Important:** Generate a secure JWT secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Installation

1. Install dependencies:
   ```bash
   cd backend
   pip install -e .
   # or
   pip install fastapi uvicorn motor pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv
   ```

2. Test MongoDB connection:
   ```bash
   python test_mongo_connection.py
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

