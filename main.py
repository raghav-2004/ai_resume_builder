from fastapi import FastAPI, Form, Request, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

app = FastAPI()

# Static and Template Directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Homepage - Resume Form
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Pydantic Model for JSON data validation
class ResumeData(BaseModel):
    name: str
    email: str
    phone: str
    skills: str
    experience: int
    education: str
    projects: str

# Handle Form Submission (HTML Form)
@app.post("/generate-resume", response_class=RedirectResponse)
async def generate_resume_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    skills: str = Form(...),
    experience: int = Form(...),
    education: str = Form(...),
    projects: str = Form(...)
):
    # Store data temporarily in a dictionary
    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills.split(","),
        "experience": experience,
        "education": education,
        "projects": projects.split(",")
    }
    
    # Redirect to resume preview (you can modify this)
    return RedirectResponse(url="/resume-preview", status_code=303)

# Handle JSON POST requests (Swagger)
@app.post("/generate-resume-json", response_class=JSONResponse)
async def generate_resume_json(resume: ResumeData):
    resume_data = {
        "name": resume.name,
        "email": resume.email,
        "phone": resume.phone,
        "skills": resume.skills.split(","),
        "experience": resume.experience,
        "education": resume.education,
        "projects": resume.projects.split(",")
    }

    return JSONResponse(content={"message": "Resume generated successfully", "data": resume_data})
