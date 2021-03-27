import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", 5432)
    password = os.environ.get("POSTGRES_PASSWORD", "abc123")
    user = os.environ.get("POSTGRES_USER", "user")
    db_name = os.environ.get("POSTGRES_DB", "")
    uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    print('PG URI')
    print(uri)
    return uri


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
