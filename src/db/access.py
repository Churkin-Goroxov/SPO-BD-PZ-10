def create_roles_and_users(connection, db_type: str):
    cursor = connection.cursor()

    if db_type == "postgres":
        #  ROLES 
        cursor.execute("CREATE ROLE admins;")
        cursor.execute("CREATE ROLE observers;")
        cursor.execute("CREATE ROLE operators;")

        #  USERS 
        cursor.execute("CREATE USER admin_user WITH PASSWORD '1234';")
        cursor.execute("CREATE USER observer_user WITH PASSWORD '1234';")
        cursor.execute("CREATE USER operator_user WITH PASSWORD '1234';")

        #  ASSIGN ROLES 
        cursor.execute("GRANT admins TO admin_user;")
        cursor.execute("GRANT observers TO observer_user;")
        cursor.execute("GRANT operators TO operator_user;")

        #  ADMINS: всё можно 
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admins;")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admins;")

        #  OBSERVERS: только 1 VIEW 
        cursor.execute("GRANT SELECT ON vw_student_grades TO observers;")

        #  OPERATORS 
        cursor.execute("GRANT SELECT ON vw_student_groups TO operators;")
        cursor.execute("GRANT SELECT ON vw_subject_teachers TO operators;")
        cursor.execute("GRANT SELECT ON vw_student_grades TO operators;")

        cursor.execute("GRANT SELECT, INSERT, UPDATE ON grades TO operators;")

    else:
        #  MYSQL 
        cursor.execute("CREATE USER 'admin_user'@'localhost' IDENTIFIED BY '1234';")
        cursor.execute("CREATE USER 'observer_user'@'localhost' IDENTIFIED BY '1234';")
        cursor.execute("CREATE USER 'operator_user'@'localhost' IDENTIFIED BY '1234';")

        # ADMINS
        cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'admin_user'@'localhost';")

        # OBSERVERS
        cursor.execute("GRANT SELECT ON vw_student_grades TO 'observer_user'@'localhost';")

        # OPERATORS
        cursor.execute("GRANT SELECT ON vw_student_groups TO 'operator_user'@'localhost';")
        cursor.execute("GRANT SELECT ON vw_subject_teachers TO 'operator_user'@'localhost';")
        cursor.execute("GRANT SELECT ON vw_student_grades TO 'operator_user'@'localhost';")
        cursor.execute("GRANT SELECT, INSERT, UPDATE ON grades TO 'operator_user'@'localhost';")

    connection.commit()
    cursor.close()