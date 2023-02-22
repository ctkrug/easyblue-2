# Author: Charles Krug
# Data Querying -- UM Atlas Course Data
# Date: 2/14/2023

import sqlite3
import argparse
import categories

# Global Variables
DB_NAME = "Atlas_W23_All_Subjects_GR.db"
COURSE_TABLE = "W23_All_Atlas_Data_GR"
GRADE_LIST = ["a_plus", "a", "a_minus", "b_plus", "b", "b_minus", "c_plus", "c", "c_minus", "d_plus", "d", "d_minus", "e"]

def create_connection(database_name=DB_NAME):
    conn = sqlite3.connect(database_name)
    return conn

def close_connection(conn):
    conn.close()
    return

def get_departments(conn, course_table=COURSE_TABLE):
    cursor = conn.cursor()
    query = "SELECT DISTINCT course_code FROM {}".format(course_table)
    cursor.execute(query)
    departments = cursor.fetchall()
    departments = [department[0] for department in departments]
    return departments

def create_percent_grade_query(conn, min_grade, min_percent, query, course_table=COURSE_TABLE):
    min_percent = float(min_percent)/100
    query += " WHERE "
    grade_query = ""

    # Add each value of the grade distribution to the query until the min_grade is reached
    count = 0
    for grade in GRADE_LIST:
        grade_query += "{} + ".format(grade)
        if grade == min_grade:
            break

    orig_grade_query = grade_query[:-3]
    just_grade_query = "SELECT {} 0 FROM {} WHERE {} 0 >= {}".format(grade_query, course_table, grade_query, min_percent)

    cursor = conn.cursor()
    cursor.execute(just_grade_query)

    grade_query += "0 >= {}".format(min_percent)
    query += grade_query
    # Get the sum of the grade distribution for each course

    return query, orig_grade_query

def query_courses(conn, sort_by="median_grade", ascending=None, limit=None, filter_criteria=None, category=None, course_level=None, exclude_na="False", min_grade=0, min_percent=0, course_table=COURSE_TABLE, database_name=DB_NAME):
    """
    Queries the database for courses, sorted by the given column, in the given order.
    If limit is specified, only the first limit results are returned.
    If filter_criteria is specified, only the results that match the criteria are returned.
    If category is specified, only the courses belonging to that category are returned.
    If course_level is specified, only the courses in that level range are returned.
    """
    int_min_grade = int(min_grade)
    min_percent = int(min_percent)
    min_grade = GRADE_LIST[max(0,12-int(min_grade))]
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
        sort_by = "gpa"
        # Check for None values
        if order is None:
            order = "DESC"
        second_priority = "weighted_gpa"
        second_priority_order = "DESC"
        third_priority = "workload"
        third_priority_order = "ASC"

    # Workload Sort
    elif sort_by == "workload":
        # Check for None values
        if order is None:
            order = "ASC"
        second_priority = "median_grade"
        second_priority_order = "DESC"
        third_priority = "weighted_gpa"
        third_priority_order = "DESC"

    # Weighted GPA Sort
    elif sort_by == "weighted_gpa":
        # Check for None values
        if order is None:
            order = "DESC"
        second_priority = "workload"
        second_priority_order = "ASC"
        third_priority = "median_grade"
        third_priority_order = "DESC"

    select = f"SELECT * FROM {course_table}"

    query, grade_query = create_percent_grade_query(conn, min_grade, min_percent, "", course_table=course_table)

    if min_percent == 0 and int_min_grade == 0:
        query = " WHERE course_name != 'N/A'"

    if course_level is not None:
        query += f" AND course_number >= {course_level}"

    if category:
        query += f" AND course_code='{category}'"  
    
    if filter_criteria:
            query += f" AND {filter_criteria}"
            
    # check if the word 'False' is in the string exclude_na (there's extra whitespace)
    if 'False' not in exclude_na:
            query += " AND {} != 'N/A' AND {} != 'null' AND {} != 'N/A' AND {} != 'null' AND {} != 'N/A' AND {} != 'null'".format(orig_sort_by, orig_sort_by, second_priority, second_priority, third_priority, third_priority)
    
    if second_priority == "median_grade":
        second_priority = "weighted_gpa"
    
    query += " ORDER BY {} {} ".format(sort_by, order)
    query += ", {} {}".format(second_priority, second_priority_order)
    query += ", {} {}".format(third_priority, third_priority_order)

    if limit:
        query += " LIMIT {}".format(limit)

    grade_query = "SELECT {} FROM {} WHERE {} >= {}".format(grade_query, course_table, grade_query, float(min_percent)/100)
    cursor.execute(grade_query)
    percent_results = cursor.fetchall()
    query = select + query
    print(query)
    cursor.execute(query)
    query_results = cursor.fetchall()

    return query_results, percent_results

def update_name_column(conn, course_table=COURSE_TABLE):
    """ 
    Adds a new column to the classes table called name, which is the name of the course.
    It combines the department and number columns.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE {} SET name = department || ' ' ||  course_number".format(course_table))
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

    results = query_courses(conn, sort_by, ascending, limit, filter_criteria, category, course_level, exclude_na, min_grade, min_percent)
    print(results)
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

    GRADE_LIST = ["a_plus", "a", "a_minus", "b_plus", "b", "b_minus", "c_plus", "c", "c_minus", "d_plus", "d", "d_minus", "e"]
    main()