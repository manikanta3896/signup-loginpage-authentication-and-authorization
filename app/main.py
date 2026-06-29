from pathlib import Path

from fastapi import FastAPI, Request, Depends, Form, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .auth import create_access_token, verify_password
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def render(request: Request, template: str):
    return templates.TemplateResponse(request=request, name=template, context={"request": request})


def redirect(url: str):
    return RedirectResponse(url=url, status_code=303)


@app.get("/")
def home():
    return {"message": "Login System is Running Successfully!"}


@app.get("/signup")
def signup_page(request: Request):
    return render(request, "signup.html")


@app.post("/signup")
def signup(
    username: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    if crud.get_user_by_username(db, username):
        return {"message": "Username already exists"}
    if crud.get_user_by_email(db, email):
        return {"message": "Email already exists"}
    if crud.get_user_by_phone(db, phone):
        return {"message": "Phone already exists"}

    crud.create_user(
        db,
        schemas.UserSignup(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
        ),
    )
    return redirect("/create-password")


@app.get("/create-password")
def create_password_page(request: Request):
    return render(request, "create_password.html")


@app.post("/create-password")
def create_password(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if crud.create_password(db, username, password) is None:
        return {"message": "User not found"}
    return redirect("/login")


@app.get("/login")
def login_page(request: Request):
    return render(request, "login.html")


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = crud.login_user(db, username)
    if user is None:
        return {"message": "Invalid Username"}
    if not verify_password(password, user.hashed_password):
        return {"message": "Invalid Password"}

    response = redirect("/dashboard")
    response.set_cookie(
        key="access_token",
        value=create_access_token({"sub": user.username}),
        httponly=True,
    )
    return response


@app.get("/dashboard")
def dashboard(request: Request, access_token: str | None = Cookie(default=None)):
    if access_token is None:
        return redirect("/login")
    return render(request, "dashboard.html")
