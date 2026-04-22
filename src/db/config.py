# КОНФИГИ
def get_config(db_name: str, db_type: str):
    if db_type == "postgres":
        return {
            "host": "127.0.0.1",
            "port": 5432,
            "user": "user",
            "password": "1234",
            "dbname": db_name
        }

    elif db_type == "mysql":
        return {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "user",
            "password": "1234",
            "database": db_name
        }

    else:
        raise ValueError("Unsupported db_type")
