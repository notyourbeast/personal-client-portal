# Quick MongoDB Setup Guide

## Step 1: Get Your MongoDB Connection String

### For MongoDB Atlas (Cloud - Recommended):
1. Sign up at https://www.mongodb.com/cloud/atlas (free tier available)
2. Create a cluster (free M0 tier works fine)
3. Click "Connect" → "Connect your application"
4. Copy the connection string (looks like):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### For Local MongoDB:
If you have MongoDB installed locally:
```
mongodb://localhost:27017
```

## Step 2: Update .env File

Edit `backend/.env` and replace the placeholders:

```env
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGO_DB=clienthub
JWT_SECRET_KEY=generate-a-random-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Generate a secure JWT secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 3: Whitelist Your IP (MongoDB Atlas Only)

1. In MongoDB Atlas dashboard, go to "Network Access"
2. Click "Add IP Address"
3. For development, add `0.0.0.0/0` (allows all IPs)
   - ⚠️ Only use this for development!
   - For production, add your specific server IP

## Step 4: Test Connection

```bash
cd backend
python test_mongo_connection.py
```

You should see: ✅ MongoDB connection successful!

## Step 5: Start the Server

```bash
uvicorn app.main:app --reload
```

## Troubleshooting

**Connection timeout:**
- Check your internet connection
- Verify MongoDB Atlas cluster is running
- Check IP whitelist in MongoDB Atlas

**Authentication failed:**
- Verify username and password in connection string
- Make sure special characters in password are URL-encoded

**Database not found:**
- This is normal! MongoDB creates databases automatically when you first write data

## Need Help?

Check the full README.md for more details.

