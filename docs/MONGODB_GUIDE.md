# MongoDB Guide

This guide covers installing, configuring, and operating the MongoDB database used by Disaster Missing Persons.

## 1. Choosing a Setup

| Option | Best for |
|--------|----------|
| Local MongoDB | Development, offline/low-bandwidth field deployments |
| Docker | Quick local testing without installing MongoDB directly |
| MongoDB Atlas | Production, managed hosting, automatic backups |

---

## 2. Local Installation

### Windows
1. Download the MongoDB Community Server installer from [mongodb.com](https://www.mongodb.com/try/download/community).
2. Run the installer and select **"Install as a Service"** so MongoDB starts automatically.
3. Verify it's running:
   ```powershell
   mongosh
   ```

### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

Check it's running:
```bash
sudo systemctl status mongod
mongosh
```

---

## 3. Docker (Quick Local Testing)

```bash
docker run -d --name disaster-mongo -p 27017:27017 -v mongo_data:/data/db mongo:7
```

Or with the `docker-compose.yml` from the README's Deployment section — MongoDB will start alongside the app automatically with `docker compose up`.

To connect a shell into the container:
```bash
docker exec -it disaster-mongo mongosh
```

---

## 4. MongoDB Atlas (Production / Managed Hosting)

1. Create a free account and cluster at [mongodb.com/atlas](https://www.mongodb.com/atlas).
2. Under **Database Access**, create a user with a strong password.
3. Under **Network Access**, add your server's IP (or `0.0.0.0/0` only for quick testing — restrict it for production).
4. Click **Connect → Drivers** and copy your connection string, which looks like:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/disaster_missing_persons?retryWrites=true&w=majority
   ```
5. Put that string in your `.env` file as `MONGODB_URL`.

---

## 5. Configuring the App

In `.env` (copied from `.env.example`):

```bash
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=disaster_missing_persons
```

For Atlas, replace `MONGODB_URL` with your `mongodb+srv://...` connection string. `DATABASE_NAME` can stay as-is — MongoDB creates the database automatically on first write.

---

## 6. Collections & Indexes

On startup, `init_database()` (in `src/disaster_missing_persons/services/database.py`) automatically creates these collections and indexes — no manual setup required:

| Collection | Index | Purpose |
|------------|-------|---------|
| `users` | `email` (unique) | Prevent duplicate accounts, fast login lookup |
| `users` | `username` (unique) | Prevent duplicate usernames |
| `reports` | `status` | Fast filtering by Active/Found/Closed |
| `reports` | `created_at` | Sorting/expiry queries |
| `reports` | `rescuer_id` | Fast lookup of a rescuer's own reports |
| `reports` | `last_seen_location` (2dsphere) | Geospatial queries on last-seen coordinates |
| `tips` | `report_id` | Fast lookup of tips for a given report |
| `tips` | `created_at` | Sorting tips chronologically |

A default admin account is also created automatically on first run using `DEFAULT_ADMIN_EMAIL` / `DEFAULT_ADMIN_PASSWORD` from `.env`, if no admin account exists yet.

---

## 7. Useful `mongosh` Commands

Connect and switch to the app's database:
```bash
mongosh
use disaster_missing_persons
```

Inspect data:
```javascript
db.users.find().pretty()
db.reports.find({ status: "active" }).pretty()
db.tips.find({ report_id: "<report-id>" }).pretty()
```

Count documents:
```javascript
db.reports.countDocuments({ status: "active" })
```

Verify indexes were created:
```javascript
db.users.getIndexes()
db.reports.getIndexes()
```

Manually promote a user to admin (useful if you're locked out):
```javascript
db.users.updateOne({ email: "you@example.com" }, { $set: { role: "admin" } })
```

Reset the default admin (deletes it so the app recreates it on next startup):
```javascript
db.users.deleteOne({ role: "admin" })
```

---

## 8. Backup & Restore

Back up the database:
```bash
mongodump --uri="mongodb://localhost:27017" --db=disaster_missing_persons --out=./backup
```

Restore from a backup:
```bash
mongorestore --uri="mongodb://localhost:27017" --db=disaster_missing_persons ./backup/disaster_missing_persons
```

For Atlas, use the same commands with your `mongodb+srv://...` URI, or use Atlas's built-in automated backup/snapshot feature (available on paid tiers).

---

## 9. Troubleshooting

### `MongoDB connection refused`
- Confirm MongoDB is actually running: `sudo systemctl status mongod` (Linux) or check the Services app (Windows).
- Confirm `MONGODB_URL` in `.env` matches where MongoDB is listening (default port `27017`).

### `Authentication failed` (Atlas)
- Double-check the username/password in the connection string — special characters in the password must be URL-encoded (e.g. `@` → `%40`).
- Confirm the database user has read/write permissions on the target database.

### `Could not connect to any servers in your MongoDB Atlas cluster`
- Your current IP isn't whitelisted — add it under **Network Access** in Atlas.

### Duplicate key errors on `email` or `username`
- Expected behavior — the unique indexes are working as intended to prevent duplicate accounts.

### Slow geospatial queries on `last_seen_location`
- Confirm the `2dsphere` index exists: `db.reports.getIndexes()`. If missing, restart the app so `init_database()` recreates it, or create it manually:
  ```javascript
  db.reports.createIndex({ last_seen_location: "2dsphere" })
  ```
