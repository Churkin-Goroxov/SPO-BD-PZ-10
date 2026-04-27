def create_views(connection):
    cursor = connection.cursor()

    # 1. Студенты + группы
    cursor.execute("""
    CREATE OR REPLACE VIEW vw_student_groups AS
    SELECT s.id, s.name, g.name AS group_name
    FROM students s
    JOIN groups g ON s.group_id = g.id;
    """)

    # 2. Дисциплины + преподаватели
    cursor.execute("""
    CREATE OR REPLACE VIEW vw_subject_teachers AS
    SELECT sub.name AS subject, t.name AS teacher
    FROM subjects sub
    JOIN teachers t ON sub.teacher_id = t.id;
    """)

    # 3. Оценки студентов
    cursor.execute("""
    CREATE OR REPLACE VIEW vw_student_grades AS
    SELECT s.name AS student, sub.name AS subject, g.grade, g.date
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN subjects sub ON g.subject_id = sub.id;
    """)

    connection.commit()
    cursor.close()