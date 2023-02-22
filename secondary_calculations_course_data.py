
import sqlite3
import argparse
import categories

# Global Variables
DB_NAME = "Atlas_W23_All_Subjects_GR.db"
COURSE_TABLE = "W23_Online_Atlas_Data_GR"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def close_connection(conn):
    conn.close()
    return

def create_weighted_gpa_column(conn):
    cursor = conn.cursor()
    query = "ALTER TABLE {} ADD COLUMN weighted_gpa REAL".format(COURSE_TABLE)
    cursor.execute(query)
    conn.commit()
    return

def update_weighted_gpa_column(conn):
    cursor = conn.cursor()
    # Weighted GPA is the expected value / weighted sum of gpa given the grade distrubtion (b_plus is 3.3, b is 3.0, etc.)
    query = "UPDATE {} SET weighted_gpa = (4.0 *(a_plus + a) + 3.7 * a_minus + 3.3 * b_plus + 3.0 * b + 2.7 * b_minus + 2.3 * c_plus + 2.0 * c + 1.7 * c_minus + 1.3 * d_plus + 1.0 * d + 0.7 * d_minus + 0.0 * e) / (a_plus + a + a_minus + b_plus + b + b_minus + c_plus + c + c_minus + d_plus + d + d_minus + e)".format(COURSE_TABLE) 
    cursor.execute(query)
    conn.commit()
    return

def create_course_number_column(conn):
    cursor = conn.cursor()
    # The course number is the last 3 digits of the course name
    query = "ALTER TABLE {} ADD COLUMN course_number INTEGER".format(COURSE_TABLE)
    cursor.execute(query)
    conn.commit()
    return

def update_course_number_column(conn):
    cursor = conn.cursor()
    query = "UPDATE {} SET course_number = (SELECT SUBSTR(course_name, -3, 3))".format(COURSE_TABLE)
    cursor.execute(query)
    conn.commit()
    return

def change_gpa_and_workload_and_weighted_gpa_to_float(conn):
    cursor = conn.cursor()
    # Create new column called workload_num and convert workload to a float
    query = "UPDATE {} SET workload_num = CAST(workload AS REAL)".format(COURSE_TABLE)
    # query = "UPDATE {} SET workload_num = '1'".format(COURSE_TABLE)
    cursor.execute(query)
    conn.commit()
    return

def create_and_update_gpa_column(conn):
    """
    Adds a new column to the classes table called gpa, which is the numeric value of the median grade.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {}".format(COURSE_TABLE))
    classes = cursor.fetchall()
    # Create gpa column
    cursor.execute("ALTER TABLE {} ADD COLUMN gpa REAL".format(COURSE_TABLE))
    for grade in GRADE_VALUES:
        cursor.execute("UPDATE {} SET gpa = {} WHERE median_grade = '{}'".format(COURSE_TABLE, GRADE_VALUES[grade], grade))
    conn.commit()



def main():
    conn = create_connection()
    create_course_number_column(conn)
    update_course_number_column(conn)

    create_and_update_gpa_column(conn)
    create_weighted_gpa_column(conn)
    update_weighted_gpa_column(conn)
    
    close_connection(conn)

    return


if __name__ == "__main__":
    GRADE_VALUES = {
    "A+": 4.001,
    "A+~A": 4.0001,
    "A": 4.0,
    "A~A-": 3.85,
    "A-": 3.7,
    "A~B+": 3.65,
    "A-~B+": 3.5,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "E": 0.0,
    "F": 0.0,
    "N/A": 0.0,
    }
    main()