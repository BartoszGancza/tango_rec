import os

from fastapi.middleware.cors import CORSMiddleware

DB_NAME = os.getenv("POSTGRES_NAME")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST", "*").split(",")

if all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
    POSTGRESQL_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
else:
    POSTGRESQL_DATABASE_URL = None

MIDDLEWARE = (
    (
        CORSMiddleware,
        {
            "allow_origins": CORS_ORIGIN_WHITELIST,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        },
    ),
)
