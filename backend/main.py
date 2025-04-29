# main.py
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from auth import register_user, login_user, get_current_user
from generator import generate_website
from scraper import scrape_businesses_without_websites
from emailer import send_demo_email
from crm import (
    create_project,
    get_projects,
    update_project_status
)

app = FastAPI(title="WebPulse AI Admin API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to WebPulse AI API"}

# -------------------------
# AUTH ROUTES
# -------------------------

@app.post("/auth/register")
async def register(request: Request):
    data = await request.json()
    return await register_user(data)

@app.post("/auth/login")
async def login(request: Request):
    data = await request.json()
    return await login_user(data)

# -------------------------
# PROJECT / CRM ROUTES
# -------------------------

@app.post("/projects")
def create(data: dict, user=Depends(get_current_user)):
    return create_project(data, user)

@app.get("/projects")
def list_projects(user=Depends(get_current_user)):
    return get_projects(user)

@app.put("/projects/{project_id}")
def update_project(project_id: str, status: str, user=Depends(get_current_user)):
    return update_project_status(project_id, status, user)

# -------------------------
# WEBSITE GENERATION ROUTE
# -------------------------

@app.post("/generate")
def generate(data: dict, user=Depends(get_current_user)):
    return generate_website(data)

# -------------------------
# SCRAPER ROUTE
# -------------------------

@app.get("/scrape")
def scrape(category: str = "all", location: str = "South Africa"):
    return scrape_businesses_without_websites(category, location)

# -------------------------
# EMAIL ROUTE
# -------------------------

@app.post("/email")
def email(data: dict, user=Depends(get_current_user)):
    return send_demo_email(data)

# -------------------------
# Error Handling
# -------------------------

@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
