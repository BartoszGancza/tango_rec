import argparse
import datetime
import hashlib
import random
import uuid

from dateutil import tz
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import CalendarEventModel, ConferenceRoomModel, UserModel


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    sha = hashlib.sha256()
    sha.update(password_bytes)

    return sha.hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("--username", type=str, default=None)
parser.add_argument("--password", type=str, default=None)
parser.add_argument("--email", type=str, default=None)
parser.add_argument("--timezone", type=str, default=None)
parser.add_argument("--company_id", type=uuid.UUID, default=None)
parser.add_argument("--count", type=int, default=1)
parser.add_argument("--generate-users", action="store_true")
parser.add_argument("--generate-rooms", action="store_true")
parser.add_argument("--generate-events", action="store_true")

args = parser.parse_args()

engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/postgres")
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

fake = Faker()
db = SessionLocal()

if args.generate_users:
    if args.count > 1:
        company_ids = [uuid.uuid4() for _ in range(4)]
        users = []
        for _ in range(args.count):
            username = fake.user_name()
            password = fake.password()
            users.append(
                UserModel(
                    username=username,
                    email=fake.email(),
                    password=hash_password(password),
                    timezone=fake.timezone(),
                    company_id=company_ids[random.randint(0, 3)],
                )
            )
            print(f"Username: {username}, Password: {password}")
        db.bulk_save_objects(users)
    else:
        user = UserModel(
            username=args.username,
            email=args.email,
            password=hash_password(args.password),
            timezone=args.timezone,
            company_id=args.company_id,
        )
        db.add(user)
elif args.generate_rooms:
    managers = db.query(UserModel).all()

    if not managers:
        print("No potential managers found.")
        exit()

    conference_rooms = [
        ConferenceRoomModel(
            name=fake.word(),
            address=fake.address(),
            manager_id=random.choice(managers).uuid,
        )
        for _ in range(args.count)
    ]
    db.bulk_save_objects(conference_rooms)
elif args.generate_events:
    owners = db.query(UserModel).all()
    locations = db.query(ConferenceRoomModel).all()

    if not owners:
        print("No potential owners found.")
        exit()

    for _ in range(args.count):
        owner = random.choice(owners)
        location = random.choice(locations) if locations else None
        start_time = fake.date_time(tzinfo=tz.gettz(owner.timezone))
        event = CalendarEventModel(
            owner_id=owner.uuid,
            location_id=location.uuid,
            start_time=start_time,
            end_time=start_time
            + datetime.timedelta(
                hours=random.randint(1, 8),
            ),
            name=fake.sentence(nb_words=3),
            agenda=fake.text(max_nb_chars=200),
            company_id=owner.company_id,
        )
        db.add(event)
        event.attendees = random.choices(
            owners, k=random.randint(1, len(owners))
        )

db.commit()
db.close()
