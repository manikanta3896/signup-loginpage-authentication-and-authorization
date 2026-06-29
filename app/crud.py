from sqlalchemy.orm import Session

try:
    from . import models, schemas
    from .auth import hash_password
except ImportError:  # pragma: no cover - supports direct execution
    from app import models, schemas
    from app.auth import hash_password


# Create User (Signup)

def create_user(db: Session, user: schemas.UserSignup):

    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Get User By Username

def get_user_by_username(
    db: Session,
    username: str
):
    username = username.strip()

    print("Searching:", repr(username))

    all_users = db.query(models.User).all()
    print("Users in DB:", [(u.id, repr(u.username)) for u in all_users])

    user = (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )

    print("Matched user:", user)

    return user

# Get User By Email

def get_user_by_email(
    db: Session,
    email: str
):

    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


# Get User By Phone

def get_user_by_phone(
    db: Session,
    phone: str
):

    return (
        db.query(models.User)
        .filter(models.User.phone == phone)
        .first()
    )


# Create Password

def create_password(
    db: Session,
    username: str,
    password: str
):

    user = get_user_by_username(
        db,
        username
    )

    if not user:
        return None

    user.hashed_password = hash_password(password)

    db.commit()
    db.refresh(user)

    return user


# Login User

def login_user(
    db: Session,
    username: str
):

    return get_user_by_username(
        db,
        username
    )