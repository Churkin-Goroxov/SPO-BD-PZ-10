from db.db_setup import create_tables, seed_data
from db.config import get_config
from db.views import create_views
from db.sql_table import SQLTable
from db.access import create_roles_and_users

DB_NAME = "pz_10"
DB_TYPE = "mysql"

config = get_config(DB_NAME, DB_TYPE)

create_tables(config, DB_TYPE)
seed_data(config, DB_TYPE)

table = SQLTable(config, "students", db_type=DB_TYPE)
create_views(table.connection)

create_roles_and_users(table.connection, DB_TYPE)