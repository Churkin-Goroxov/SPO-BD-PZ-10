from db.db_setup import create_tables, seed_data
from db.config import get_config

DB_NAME = "pz_10"
DB_TYPE = "postgres"

config = get_config(DB_NAME, DB_TYPE)

create_tables(config, DB_TYPE)
seed_data(config, DB_TYPE)
