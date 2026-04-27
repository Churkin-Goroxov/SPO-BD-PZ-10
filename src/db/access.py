def create_roles_and_users(connection, db_type: str, db_name: str = "pz_10"):
    cursor = connection.cursor()

    if db_type == "postgres":
        # --- ROLES ---
        cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admins') THEN
                CREATE ROLE admins;
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'observers') THEN
                CREATE ROLE observers;
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'operators') THEN
                CREATE ROLE operators;
            END IF;
        END
        $$;
        """)

        # --- USERS ---
        cursor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin_user') THEN
                CREATE USER admin_user WITH PASSWORD '1234';
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'observer_user') THEN
                CREATE USER observer_user WITH PASSWORD '1234';
            END IF;
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'operator_user') THEN
                CREATE USER operator_user WITH PASSWORD '1234';
            END IF;
        END
        $$;
        """)

        # --- ASSIGN ROLES ---
        cursor.execute("GRANT admins TO admin_user;")
        cursor.execute("GRANT observers TO observer_user;")
        cursor.execute("GRANT operators TO operator_user;")

        # --- PRIVILEGES ---
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admins;")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admins;")

        cursor.execute("GRANT SELECT ON vw_student_grades TO observers;")

        cursor.execute("GRANT SELECT ON vw_student_groups TO operators;")
        cursor.execute("GRANT SELECT ON vw_subject_teachers TO operators;")
        cursor.execute("GRANT SELECT ON vw_student_grades TO operators;")
        cursor.execute("GRANT SELECT, INSERT, UPDATE ON grades TO operators;")

    else:
        # --- MYSQL ---

        # USERS (без падения при повторном запуске)
        cursor.execute(f"CREATE USER IF NOT EXISTS 'admin_user'@'%' IDENTIFIED BY '1234';")
        cursor.execute(f"CREATE USER IF NOT EXISTS 'observer_user'@'%' IDENTIFIED BY '1234';")
        cursor.execute(f"CREATE USER IF NOT EXISTS 'operator_user'@'%' IDENTIFIED BY '1234';")

        # ADMINS (ограничиваем только БД)
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO 'admin_user'@'%';")

        # OBSERVERS
        cursor.execute(f"GRANT SELECT ON {db_name}.vw_student_grades TO 'observer_user'@'%';")

        # OPERATORS
        cursor.execute(f"GRANT SELECT ON {db_name}.vw_student_groups TO 'operator_user'@'%';")
        cursor.execute(f"GRANT SELECT ON {db_name}.vw_subject_teachers TO 'operator_user'@'%';")
        cursor.execute(f"GRANT SELECT ON {db_name}.vw_student_grades TO 'operator_user'@'%';")
        cursor.execute(f"GRANT SELECT, INSERT, UPDATE ON {db_name}.grades TO 'operator_user'@'%';")


    connection.commit()
    cursor.close()