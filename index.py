from flask import Flask, render_template, request
import sqlite3
import query_courses

app = Flask(__name__)

DB_NAME = "Atlas_Courseguide_W23_All_Subjects_UG.db"
COURSE_TABLE = "W23_All_Atlas_Data_test"
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = query_courses.create_connection()
    departments = query_courses.get_departments(conn)
    if request.method == 'POST':
        search = request.form.get('search')
        sort_by = request.form.get('sort_by')
        sort_order = request.form.get('sort_order')
        limit = request.form.get('limit')
        category = request.form.get('category')
        course_level = request.form.get('course_level')
        exclude_na = request.form.get('exclude_na')
        grade_range = request.form.get("grade_range")
        gpa_range = request.form.get("gpa_range")

        
        print(gpa_range)
        # Call the query_courses function and pass in the form data
        courses = query_courses.query_courses(conn=conn, sort_by=sort_by, ascending=sort_order, limit=limit, filter_criteria=search, category=category, course_level=course_level, exclude_na=exclude_na)
        print(courses, "\n")
        print(len(courses), " courses")
        print(len(courses[0])," elements")
        # Close the database connection
        query_courses.close_connection(conn)

        return render_template('index.html', courses=courses, departments=departments)
    
    else:
        # Connect to the database
        conn = query_courses.create_connection()

        # Call the query_courses function without form data to get all courses
        courses = query_courses.query_courses(conn)
        print(courses)
        print(len(courses), " courses")
        print(len(courses[0])," elements")
        # Close the database connection
        query_courses.close_connection(conn)

        return render_template('index.html', courses=courses, departments = departments)

if __name__ == '__main__':
    app.run()