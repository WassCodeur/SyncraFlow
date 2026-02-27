from faker import Faker
from uuid import uuid4
from pathlib import Path
from json import dump, load
from passlib.hash import pbkdf2_sha256
from random import choice
from datetime import datetime, timezone

fake = Faker()

DATA_DIR = Path("app/database/")

MOCK_USERS = DATA_DIR / "mock_users.json"

WORFLOWS_DATA = DATA_DIR / "mock_workflows.json"

STEPS_DATA = DATA_DIR / "mock_steps.json"

# TODO: Implement a real database and remove this mock data generation and stockage functions


def generate_fake_users(number):
    users = load_data()
    for _ in range(number):
        user = {
            "id": str(uuid4()),
            "name": fake.name(),
            "username": fake.user_name(),
            "email": fake.email(),
            "password_hash": pbkdf2_sha256.hash("Pass1234"),
            "is_active": choice([True, False]),
            "role": choice(["SUPER_ADMIN", "ADMIN", "DEVELOPER", "USER"]),
            "tier": choice(["free", "pro", "entreprise"]),
            "created_at": str(datetime.now(timezone.utc))
        }
        users.append(user)

    save_data(users, MOCK_USERS)


def save_data(data, file=MOCK_USERS):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(file, "w") as f:
        dump(data, f, indent=2)


def load_data(file=MOCK_USERS):
    if file.exists():
        with open(file, "r") as f:
            return load(f)
    else:
        return []
