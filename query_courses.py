# Author: Charles Krug
# Data Querying -- UM Atlas Course Data
# Date: 2/14/2023

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

def get_departments(conn):
    cursor = conn.cursor()
    query = "SELECT DISTINCT course_code FROM {}".format(COURSE_TABLE)
    cursor.execute(query)
    departments = cursor.fetchall()
    departments = [department[0] for department in departments]
    return departments

def query_courses(conn, sort_by="median_grade", ascending=None, limit=None, filter_criteria=None, category=None, course_level=None, exclude_na="False"):
    """
    Queries the database for courses, sorted by the given column, in the given order.
    If limit is specified, only the first limit results are returned.
    If filter_criteria is specified, only the results that match the criteria are returned.
    If category is specified, only the courses belonging to that category are returned.
    If course_level is specified, only the courses in that level range are returned.
    """
    cursor = conn.cursor()
    order = "ASC" if ascending == "ASC" else "DESC" if ascending == "DESC" else "DESC"
    limit = 100 if limit is None else limit
    orig_sort_by = sort_by
    where = False
    try:
        course_level = int(course_level)
    except: 
        course_level = None

    # Median Grade Sort
    if sort_by == "median_grade":
        sort_by = "weighted_gpa"
        # Check for None values
        if order is None:
            order = "DESC"
        second_priority = "workload"
        second_priority_order = "ASC"

    # Workload Sort
    elif sort_by == "workload":
        # Check for None values
        if order is None:
            order = "ASC"
        second_priority = "median_grade"
        second_priority_order = "DESC"

    query = f"SELECT * FROM {COURSE_TABLE}"
    
    if course_level is not None:
        query += f" WHERE course_number >= {course_level}"
        where = True
        if category or filter_criteria:
            query += " AND "
    elif category or filter_criteria:
        query += " WHERE "
        where = True
    if category:
        query += f" course_code='{category}'"  
        if filter_criteria:
            query += f" AND {filter_criteria}"
    elif filter_criteria:
        query += " WHERE " + filter_criteria
        where = True
    # check if the word 'False' is in the string exclude_na (there's extra whitespace)
    if 'False' not in exclude_na:
        print('excluded na', exclude_na)
        print(type(exclude_na))
        if where:
            query += " AND {} != 'N/A' AND {} != 'null' AND {} != 'N/A' AND {} != 'null'".format(orig_sort_by, orig_sort_by, second_priority, second_priority)
        else:
            query += " WHERE {} != 'N/A' AND {} != 'null' AND {} != 'N/A' AND {} != 'null'".format(orig_sort_by, orig_sort_by, second_priority, second_priority)
    if second_priority == "median_grade":
        second_priority = "weighted_gpa"
    query += " ORDER BY {} {}".format(sort_by, order)
    query += ", {} {}".format(second_priority, second_priority_order)
    if limit:
        query += " LIMIT {}".format(limit)
    print(query)
    
    cursor.execute(query)
    return cursor.fetchall()

def update_gpa_column(conn):
    """
    Adds a new column to the classes table called gpa, which is the numeric value of the median grade.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {}".format(COURSE_TABLE))
    classes = cursor.fetchall()
    # Create gpa column
    # cursor.execute("ALTER TABLE {} ADD COLUMN gpa REAL".format(COURSE_TABLE))
    for grade in GRADE_VALUES:
        cursor.execute("UPDATE {} SET gpa = {} WHERE median_grade = '{}'".format(COURSE_TABLE, GRADE_VALUES[grade], grade))
    conn.commit()

def update_name_column(conn):
    """ 
    Adds a new column to the classes table called name, which is the name of the course.
    It combines the department and number columns.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE {} SET name = department || ' ' ||  course_number".format(COURSE_TABLE))
    conn.commit()
    # Create number column

def parse_args():
    parser = argparse.ArgumentParser(description='Query courses from the database.')
    parser.add_argument('-s', '--sort_by', type=str, default='median_grade', help='sort by median_grade or workload')
    parser.add_argument('-a', '--ascending', action='store_true', help='sort in ascending order')
    parser.add_argument('-l', '--limit', type=int, help='limit the number of results')
    parser.add_argument('-f', '--filter_criteria', type=str, help='filter criteria in SQL syntax')
    parser.add_argument('-c', '--category', type=str, help='category of courses to display', choices=categories.categories.keys())
    return parser.parse_args()

def main():
    args = parse_args()
    sort_by = args.sort_by
    ascending = args.ascending
    limit = args.limit
    filter_criteria = args.filter_criteria
    category = args.category
    # Connect to the database
    conn = sqlite3.connect(DB_NAME)
    update_gpa_column(conn)
    # update_name_column(conn)
    # results = query_courses(conn, sort_by, ascending, limit, filter_criteria, category)
    # for result in results:
    #   print(result)
    conn.close()

if __name__ == '__main__':
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