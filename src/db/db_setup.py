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

def seed_data(db_config, db_type):
    # GROUPS
    groups = SQLTable(db_config, "groups", db_type=db_type)
    groups.insert_many([
        {"name": "A-101"},
        {"name": "B-202"},
    ])

    # STUDENTS
    students = SQLTable(db_config, "students", db_type=db_type)
    students.insert_many([
        {"name": "Ivan", "group_id": 1},
        {"name": "Petr", "group_id": 1},
        {"name": "Anna", "group_id": 2},
    ])

    # TEACHERS
    teachers = SQLTable(db_config, "teachers", db_type=db_type)
    teachers.insert_many([
        {"name": "Dr. Smith"},
        {"name": "Dr. Brown"},
    ])

    # SUBJECTS
    subjects = SQLTable(db_config, "subjects", db_type=db_type)
    subjects.insert_many([
        {"name": "Math", "teacher_id": 1},
        {"name": "Physics", "teacher_id": 2},
    ])

    # GRADES
    grades = SQLTable(db_config, "grades", db_type=db_type)
    grades.insert_many([
        {"student_id": 1, "subject_id": 1, "grade": 5, "date": "2024-01-01"},
        {"student_id": 2, "subject_id": 1, "grade": 4, "date": "2024-01-02"},
        {"student_id": 3, "subject_id": 2, "grade": 5, "date": "2024-01-03"},
    ])
