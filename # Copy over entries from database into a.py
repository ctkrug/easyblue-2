# Copy over entries from database into a new database if theay re in a a dictionarys
import categories

def create_new_db(DB_NAME, COURSE_TABLE, conn, satisfactory_courses, new_table_name):
    # If a course name in the dictionary is in the database, copy it over to a new database
    cursor = conn.cursor()
    query = f"SELECT name from {COURSE_TABLE}"
    cursor.execute(query)
    courses = cursor.fetchall()
    courses_names = [course[0] for course in courses]
    for course in satisfactory_courses:
        if course in courses_names:
            query = f"INSERT INTO {new_table_name} SELECT * FROM {COURSE_TABLE} WHERE name = '{course}'"
            cursor.execute(query)
    return

def main():
    DB_NAME = "Atlas_Courseguide_W23_All_Subjects_UG.db"
    COURSE_TABLE = "W23_All_Courses"
    new_table_name = "ds_adv_tech"
    satisfactory_courses = categories.categories["ds_adv_tech"]
    