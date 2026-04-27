def create_views(connection):
    cursor = connection.cursor()

    is_mysql = connection.__class__.__module__.startswith("mysql")

    def q(name):
        return f"`{name}`" if is_mysql else f'"{name}"'

    cursor.execute(f"""
    CREATE OR REPLACE VIEW vw_student_groups AS
    SELECT s.id, s.name, g.name AS group_name
    FROM {q("students")} s
    JOIN {q("groups")} g ON s.group_id = g.id;
    """)

    cursor.execute(f"""
    CREATE OR REPLACE VIEW vw_subject_teachers AS
    SELECT sub.name AS subject, t.name AS teacher
    FROM {q("subjects")} sub
    JOIN {q("teachers")} t ON sub.teacher_id = t.id;
    """)

    cursor.execute(f"""
    CREATE OR REPLACE VIEW vw_student_grades AS
    SELECT s.name AS student, sub.name AS subject, g.grade, g.{q("date")}
    FROM {q("grades")} g
    JOIN {q("students")} s ON g.student_id = s.id
    JOIN {q("subjects")} sub ON g.subject_id = sub.id;
    """)

    connection.commit()
    cursor.close()