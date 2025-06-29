from app.api.repositories import user_repository
import bcrypt

# New user registration
def register_user(username, email, password, first_name=None, last_name=None, profile_pic=None):
    existing_user = user_repository.get_user_by_email(email)
    if existing_user:
        return None, "Email already registered"
    
    # hashing password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    # creating user
    user = user_repository.create_user(
        username=username,
        email=email,
        password_hash=hashed_password,
        first_name=first_name,
        last_name=last_name,
        profile_pic=profile_pic
    )

    if user:
        return user, None
    else:
        return None, "Failed to create user "
    
# Login
def authenticate_user(email, password):
    user = user_repository.get_user_by_email(email)
    print("email from login:", email)
    print("found user:", user)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        return user
    return None

# Getting user profile by ID
def get_user(user_id):
    return user_repository.get_user_by_id(user_id)

# Updating user
def update_user(user_id, username=None, email=None, first_name=None, last_name=None, profile_pic=None):
    return user_repository.update_user(
        user_id=user_id,
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        profile_pic=profile_pic
    )

# Deleting user
def delete_user(user_id):
    return user_repository.delete_user(user_id)
