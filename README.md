# Disaster Missing Persons

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg)](https://fastapi.tiangolo.com/)

A lightweight, fast, and reliable missing person reporting system designed for disaster scenarios. Built with Python FastAPI and MongoDB, optimized for low-bandwidth environments.

## Features

- **Role-Based Access Control**: Admins, Rescuers, and Public Users
- **Missing Person Reports**: Created exclusively by authorized rescuers
- **Tip Submission**: Anyone with an account can submit tips about missing persons
- **Image Compression**: Automatic photo compression for bandwidth efficiency
- **Mobile-First Design**: Works on any device, optimized for phones
- **Auto-Expiring Reports**: Reports automatically expire after 30 days
- **Urgent Flagging**: Critical cases highlighted for immediate attention
- **Real-time Statistics**: Live dashboard of active cases and tips
- **Report Status Tracking**: Active, Found, Closed - managed by rescuer/admin only

## Quick Start

### Prerequisites

- Python 3.10+
- MongoDB 5.0+ (local or [MongoDB Atlas](https://www.mongodb.com/atlas)) — see [docs/MONGODB_GUIDE.md](docs/MONGODB_GUIDE.md) for install, Docker, Atlas, and troubleshooting

---

## Setup (Windows)

```powershell
# 1. Clone the repository
git clone https://github.com/NurAbir/Disaster-Missing-Persons.git
cd Disaster-Missing-Persons

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Windows)
venv\Scripts\Activate.ps1

# 4. Install
pip install -e .

# 5. Configure
copy .env.example .env
notepad .env   # Edit SECRET_KEY and default admin password

# 6. Make sure MongoDB is running (install from mongodb.com if needed)

# 7. Run
python -m disaster_missing_persons

# 8. Open browser → http://localhost:8000
```

---

## Setup (Linux / macOS)

```bash
# 1. Clone the repository
git clone https://github.com/NurAbir/Disaster-Missing-Persons.git
cd Disaster-Missing-Persons

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate
source venv/bin/activate

# 4. Install
pip install -e .

# 5. Configure
cp .env.example .env
nano .env   # Edit SECRET_KEY and default admin password

# 6. Make sure MongoDB is running

# 7. Run
python -m disaster_missing_persons

# 8. Open browser → http://localhost:8000
```

---

## Default Admin Account

On first run, a default admin account is created:

- **Email**: `admin@disaster-response.org`
- **Password**: `admin123` (change immediately in production)

---

## User Roles & Permissions

| Role | Description | Can Create Reports | Can View Tips | Can Change Status | Can Create Rescuers |
|------|-------------|-------------------|---------------|-------------------|---------------------|
| **Admin** | System administrator | Yes | All | Any report | Yes |
| **Rescuer** | Disaster response worker | Yes | Own reports only | Own reports only | No |
| **User** | General public | No | No | No | No |

### Key Rules

- **Only rescuers** can create missing person reports
- **Only the rescuer who created a report** (or an admin) can view tips on that report
- **Only the rescuer who created a report** (or an admin) can change that report's status
- **Anyone** can view active reports without logging in
- **Any logged-in user** can submit tips on active reports

---

## Report Status Flow

```
ACTIVE --> FOUND --> CLOSED
   ^                    |
   |____________________|
```

| Status | Meaning |
|--------|---------|
| **Active** | Person is still missing, accepting tips |
| **Found** | Person has been located safely |
| **Closed** | Case is resolved or no longer active |

---

## API Documentation

Once running, interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### Endpoint Reference

| Method | Endpoint | Auth Required | Description |
|--------|----------|----------------|--------------|
| POST | `/api/auth/register` | No | Register a new public user account |
| POST | `/api/auth/login` | No | Log in and receive a JWT access token |
| POST | `/api/admin/create-rescuer` | Admin | Create a rescuer account |
| GET | `/api/admin/rescuers` | Admin | List all rescuer accounts |
| GET | `/api/admin/stats` | Admin | System-wide statistics |
| GET | `/api/reports/stats` | No | Public dashboard statistics |
| GET | `/api/reports/` | No | List reports (supports search, urgent-only, and status filters) |
| POST | `/api/reports/` | Rescuer | Create a missing person report |
| GET | `/api/reports/{report_id}` | No | Get full details of a report |
| PATCH | `/api/reports/{report_id}/status` | Rescuer/Admin | Update a report's status |
| POST | `/api/reports/{report_id}/tips` | Logged-in user | Submit a tip on a report |
| GET | `/api/reports/{report_id}/tips` | Owning rescuer/Admin | View tips submitted on a report |

---

## Project Structure

```
Disaster Missing Persons/
├── src/disaster_missing_persons/
│   ├── api/
│   │   ├── dependencies.py      # Auth dependencies
│   │   └── routes/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── admin.py         # Admin endpoints
│   │       └── reports.py       # Report & tip endpoints
│   ├── core/
│   │   ├── config.py            # Application settings
│   │   ├── constants.py         # Enums & constants
│   │   └── exceptions.py        # Custom exceptions
│   ├── models/
│   │   ├── user.py              # User models
│   │   ├── report.py            # Report models
│   │   └── tip.py               # Tip models
│   ├── services/
│   │   ├── database.py          # MongoDB connection
│   │   └── auth_service.py      # Auth utilities
│   ├── utils/
│   │   ├── image.py             # Image compression
│   │   ├── datetime.py          # Date utilities
│   │   └── serialization.py     # Data serialization
│   ├── static/                  # CSS & JS
│   ├── templates/               # HTML templates
│   ├── main.py                  # FastAPI app
│   └── __main__.py              # CLI entry point
├── tests/                       # Test suite
├── docs/
│   ├── USERMANUAL.md            # User manual
│   └── MONGODB_GUIDE.md         # MongoDB setup, indexes, backup & troubleshooting
├── .github/
│   ├── workflows/ci.yml         # CI: lint, type-check, tests
│   ├── ISSUE_TEMPLATE/          # Bug report / feature request templates
│   └── PULL_REQUEST_TEMPLATE.md
├── pyproject.toml               # Project config
├── .env.example                 # Environment template
├── .gitignore
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
├── CHANGELOG.md                 # Version history
└── README.md                    # This file
```

---

## Configuration

All configuration is done via environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URL` | `mongodb://localhost:27017` | MongoDB connection string |
| `SECRET_KEY` | `change-me` | JWT signing key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token expiry (24 hours) |
| `IMAGE_QUALITY` | `60` | JPEG compression quality |
| `REPORT_AUTO_EXPIRE_DAYS` | `30` | Report auto-expiry |
| `DEFAULT_ADMIN_EMAIL` | `admin@disaster-response.org` | Default admin email |
| `DEFAULT_ADMIN_PASSWORD` | `admin123` | Default admin password |

---

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/
ruff check src/ tests/

# Type checking
mypy src/
```

---

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 8000
CMD ["python", "-m", "disaster_missing_persons"]
```

For local testing with a bundled MongoDB, create a `docker-compose.yml`:

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      MONGODB_URL: mongodb://mongo:27017
    env_file: .env
    depends_on:
      - mongo
  mongo:
    image: mongo:7
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

### Production Checklist

- [ ] Change `SECRET_KEY` to a secure random string (32+ chars)
- [ ] Change default admin password
- [ ] Use MongoDB Atlas or secured MongoDB instance
- [ ] Enable HTTPS / reverse proxy (nginx, Caddy)
- [ ] Set `DEBUG=false`
- [ ] Configure proper logging
- [ ] Set up firewall rules

---

## Troubleshooting

### `email-validator not installed`
```bash
pip install email-validator
```

### `bcrypt password too long`
This is fixed in the latest version. If you see this, update to the latest ZIP or run:
```bash
pip install --upgrade passlib bcrypt
```

### MongoDB connection refused
- Make sure MongoDB is running: `mongod` (or `sudo systemctl start mongod` on Linux)
- Check your `MONGODB_URL` in `.env`
- See [docs/MONGODB_GUIDE.md](docs/MONGODB_GUIDE.md) for a full setup and troubleshooting guide

### Port already in use
Change the port in `.env`: `PORT=8001`

### 422 Validation Error when creating report
Check that all required fields are filled:
- Full Name
- Date & Time (Last Seen)
- Address/Location
- Contact Phone

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on setting up a dev environment, coding style, and submitting pull requests.

See [CHANGELOG.md](CHANGELOG.md) for release history.

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Built for disaster response teams worldwide. Stay safe.
