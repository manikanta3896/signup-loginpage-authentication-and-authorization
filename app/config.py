from datetime import timedelta

# Secret key used to sign JWT tokens
SECRET_KEY = "your_super_secret_key_change_this_in_production"

# Algorithm used to sign the token
ALGORITHM = "HS256"

# Token expiry time
ACCESS_TOKEN_EXPIRE_MINUTES = 30