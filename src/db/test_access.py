import psycopg2


def test(user, password, query):
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            user=user,
            password=password,
            dbname="pz_10"
        )
        cur = conn.cursor()
        cur.execute(query)
        print(f"[OK] {user}: {query}")
        conn.close()
    except Exception as e:
        print(f"[FAIL] {user}: {e}")


# observer
test("observer_user", "1234", "SELECT * FROM vw_student_grades;")
test("observer_user", "1234", "SELECT * FROM students;")  # должен упасть

# operator
test("operator_user", "1234", "SELECT * FROM vw_student_groups;")
test("operator_user", "1234", "UPDATE grades SET grade = 5 WHERE id = 1;")
test("operator_user", "1234", "DELETE FROM students;")  # должен упасть

# admin
test("admin_user", "1234", "DELETE FROM students;")