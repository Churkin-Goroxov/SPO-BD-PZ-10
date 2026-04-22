from sql_table import SQLTable

def create_tables(db_config, db_type):
    # GROUPS
    groups = SQLTable(db_config, "groups", db_type=db_type)
    groups.create_table([
        {"name": "id", "type": "INT", "auto_increment": True},
        {"name": "name", "type": "VARCHAR(100)", "nullable": False}
    ])

    # STUDENTS
    students = SQLTable(db_config, "students", db_type=db_type)
    students.create_table([
        {"name": "id", "type": "INT", "auto_increment": True},
        {"name": "name", "type": "VARCHAR(100)", "nullable": False},
        {"name": "group_id", "type": "INT"}
    ])

    # TEACHERS
    teachers = SQLTable(db_config, "teachers", db_type=db_type)
    teachers.create_table([
        {"name": "id", "type": "INT", "auto_increment": True},
        {"name": "name", "type": "VARCHAR(100)", "nullable": False}
    ])

    # SUBJECTS
    subjects = SQLTable(db_config, "subjects", db_type=db_type)
    subjects.create_table([
        {"name": "id", "type": "INT", "auto_increment": True},
        {"name": "name", "type": "VARCHAR(100)", "nullable": False},
        {"name": "teacher_id", "type": "INT"}
    ])

    # GRADES
    grades = SQLTable(db_config, "grades", db_type=db_type)
    grades.create_table([
        {"name": "id", "type": "INT", "auto_increment": True},
        {"name": "student_id", "type": "INT"},
        {"name": "subject_id", "type": "INT"},
        {"name": "grade", "type": "INT"},
        {"name": "date", "type": "DATE"}
    ])