from db.db_setup import create_tables, seed_data
from db.config import get_config
from db.views import create_views
from db.sql_table import SQLTable

DB_NAME = "pz_10"
DB_TYPE = "postgres"

config = get_config(DB_NAME, DB_TYPE)

create_tables(config, DB_TYPE)
seed_data(config, DB_TYPE)

table = SQLTable(config, "students", db_type=DB_TYPE)
create_views(table.connection)