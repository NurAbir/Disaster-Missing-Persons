"""Main FastAPI application."""

import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from disaster_missing_persons.core.config import get_settings
from disaster_missing_persons.services.database import init_database
from disaster_missing_persons.api.routes import auth_router, admin_router, reports_router

settings = get_settings()

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title=settings.APP_NAME,
    description="Lightweight missing person reporting system for disaster scenarios",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS - allow all for disaster scenario flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates - use absolute paths
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Include API routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(reports_router)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize database on startup."""
    await init_database()


# ============== HTML Pages ==============
@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Homepage."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) -> HTMLResponse:
    """Login page."""
    return templates.TemplateResponse(request, "login.html")


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request) -> HTMLResponse:
    """Registration page."""
    return templates.TemplateResponse(request, "register.html")


@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request) -> HTMLResponse:
    """Reports listing page."""
    return templates.TemplateResponse(request, "reports.html")


@app.get("/reports/{report_id}", response_class=HTMLResponse)
async def report_detail_page(request: Request, report_id: str) -> HTMLResponse:
    """Report detail page."""
    return templates.TemplateResponse(request, "report_detail.html", {"report_id": report_id})


@app.get("/create-report", response_class=HTMLResponse)
async def create_report_page(request: Request) -> HTMLResponse:
    """Create report page (rescuer only)."""
    return templates.TemplateResponse(request, "create_report.html")


@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request) -> HTMLResponse:
    """Admin dashboard page."""
    return templates.TemplateResponse(request, "admin.html")
