# Author: Charles Krug
# Data Querying -- UM Atlas Course Data
# Date: 2/14/2023

import sqlite3
import argparse
import categories

# Global Variables
DB_NAME = "Atlas_Courseguide_W23_All_Subjects_UG.db"
COURSE_TABLE = "W23_All_Courses"

def query_courses(conn, sort_by="median_grade", ascending=True, limit=None, filter_criteria=None, category=None):
    """
    Queries the database for courses, sorted by the given column, in the given order.
    If limit is specified, only the first limit results are returned.
    If filter_criteria is specified, only the results that match the criteria are returned.
    If category is specified, only the courses belonging to that category are returned.
    """
    cursor = conn.cursor()
    order = "ASC" if ascending else "DESC"
    second_priority = "median_grade" if sort_by != "median_grade" else "workload"
    
    query = f"SELECT name, median_grade, workload FROM {COURSE_TABLE}"
    if category:
        # Get the list of courses belonging to the specified category
        course_list = categories.categories[category]
        # Use the list to build a filter criteria
        course_filter = " OR ".join(["name='{}'".format(course) for course in course_list])
        if filter_criteria:
            query += " WHERE ({}) AND ({})".format(filter_criteria, course_filter)
        else:
            query += " WHERE {}".format(course_filter)
    else:
        if filter_criteria:
            query += " WHERE " + filter_criteria
    query += " ORDER BY {} {}".format(sort_by, order)
    query += ", {} ASC".format(second_priority)
    if limit:
        query += " LIMIT {}".format(limit)
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
    for class_ in classes:
        median_grade = class_[2]
        gpa = GRADE_VALUES.get(median_grade)
        if gpa is not None:
            cursor.execute("UPDATE {} SET gpa = ? WHERE median_grade = ?".format(COURSE_TABLE), (gpa, median_grade))
    conn.commit()

def update_name_column(conn):
    """ 
    Adds a new column to the classes table called name, which is the name of the course.
    It combines the department and number columns.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {}".format(COURSE_TABLE))
    classes = cursor.fetchall()
    # Create number column
    # cursor.execute("ALTER TABLE {} ADD COLUMN name TEXT".format(COURSE_TABLE))
    for class_ in classes:
        number = class_[1]
        department = class_[0]
        name = department + " " + number
        cursor.execute("UPDATE {} SET name = ? WHERE course_number = ?".format(COURSE_TABLE), (name, number))

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
    update_name_column(conn)
    results = query_courses(conn, sort_by, ascending, limit, filter_criteria, category)
    for result in results:
        print(result)

if __name__ == '__main__':
    GRADE_VALUES = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "F": 0.0
}
    main()