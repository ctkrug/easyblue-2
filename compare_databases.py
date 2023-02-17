# Compare the contents of two databases
import sqlite3
# Get ditionary of clases for F22 classses[department] = {coursenum1, coursenum2, ...}
def get_classes(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"SELECT DISTINCT department, course_number FROM {table_name}"
    cursor.execute(query)
    courses = cursor.fetchall()
    classes = {}
    for course in courses:
        if course[0] not in classes:
            classes[course[0]] = set()
        classes[course[0]].add(course[1])
    return classes

DB_F22 = "Atlas_Courseguide_F22_All_Subjects_UG.db"
DB_W23 = "Atlas_Courseguide_W23_All_Subjects_UG.db"

F22_Table = "F22_All_Courses_UG"
W23_Table = "W23_All_Courses"

# Get F22 classes
F22_Classes = get_classes(DB_F22, F22_Table)
# Get W23 classes
W23_Classes = get_classes(DB_W23, W23_Table)

# Compare the two dictionaries
for department in F22_Classes:
    print(department)
    if department not in W23_Classes:
        print(f"{department} is not in W23")
    else:
        for course in F22_Classes[department]:
            if course not in W23_Classes[department]:
                print(f"{department} {course} is not in W23")
