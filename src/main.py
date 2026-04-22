from db.config import db_config_pg
from db.db_setup import create_tables

create_tables(db_config_pg, "postgres")