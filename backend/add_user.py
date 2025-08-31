from database import SessionLocal, User, init_db
from auth_utils import hash_password

# Initialize DB (creates tables if not exist)
init_db()

# Create a new session
db = SessionLocal()

# Add demo user
demo_email = "demo@bank.com"
demo_password = "demo123"

# Check if user already exists
existing_user = db.query(User).filter(User.email == demo_email).first()
if existing_user:
    print("User already exists!")
else:
    user = User(email=demo_email, hashed_password=hash_password(demo_password))
    db.add(user)
    db.commit()
    print(f"Demo user created: {demo_email}")

db.close()
