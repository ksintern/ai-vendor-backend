from app.core.security import hash_password


hashed_password = hash_password("admin123")

print(hashed_password)