
import sqlite3
import argparse
import categories

# Global Variables
DB_NAME = "Atlas_Courseguide_W23_All_Subjects_UG.db"
COURSE_TABLE = "W23_All_Atlas_Data_test"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def close_connection(conn):
    conn.close()
    return

def create_weighted_gpa_column(conn):
    cursor = conn.cursor()
    query = "ALTER TABLE {} ADD COLUMN weighted_gpa REAL".format(COURSE_TABLE)
    print(query)
    cursor.execute(query)
    conn.commit()
    return

def update_weighted_gpa_column(conn):
    cursor = conn.cursor()
    # Weighted GPA is the expected value / weighted sum of gpa given the grade distrubtion (b_plus is 3.3, b is 3.0, etc.)
    query = "UPDATE {} SET weighted_gpa = (4.0 *(a_plus + a) + 3.7 * a_minus + 3.3 * b_plus + 3.0 * b + 2.7 * b_minus + 2.3 * c_plus + 2.0 * c + 1.7 * c_minus + 1.3 * d_plus + 1.0 * d + 0.7 * d_minus + 0.0 * e) / (a_plus + a + a_minus + b_plus + b + b_minus + c_plus + c + c_minus + d_plus + d + d_minus + e)".format(COURSE_TABLE) 
    print(query)
    cursor.execute(query)
    conn.commit()
    return

def create_course_number_column(conn):
    cursor = conn.cursor()
    # The course number is the last 3 digits of the course name
    query = "ALTER TABLE {} ADD COLUMN course_number INTEGER".format(COURSE_TABLE)
    # print(query)
    cursor.execute(query)
    conn.commit()
    return

def update_course_number_column(conn):
    cursor = conn.cursor()
    query = "UPDATE {} SET course_number = (SELECT SUBSTR(course_name, -3, 3))".format(COURSE_TABLE)
    # print(query)
    cursor.execute(query)
    conn.commit()
    return

def main():
    conn = create_connection()
    # create_course_number_column(conn)
    # update_course_number_column(conn)
    close_connection(conn)


    return


if __name__ == "__main__":
    main()