import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", 5432)
    password = os.environ.get("POSTGRES_PASSWORD", "netF6SJJELUm6d9")
    user = os.environ.get("POSTGRES_USER", "ok-scoring-py-user")
    db_name = os.environ.get("POSTGRES_DB", "ok-scoring")
    uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return uri


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
