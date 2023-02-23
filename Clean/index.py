from flask import Flask, render_template, request
import sqlite3
import query_courses

app = Flask(__name__)

NAMES_TO_TABLES = {
    "F22": ("F22_All_Atlas_Data","Atlas_F22_All_Subjects_UG.db"),
    "W23": ("W23_All_Atlas_Data","Atlas_W23_All_Subjects_UG.db"),
    "F22_GR": ("F22_All_Atlas_GR_Data","Atlas_F22_All_Subjects_GR.db"),
    "W23_GR": ("W23_All_Atlas_Data_GR","Atlas_W23_All_Subjects_GR.db"),
    "F22_GR_O": ("F22_Online_Atlas_Data_GR","Atlas_F22_All_Subjects_GR.db"),
    "W23_GR_O": ("W23_Online_Atlas_Data_GR","Atlas_W23_All_Subjects_GR.db"),
}

DB_NAME = "Atlas_W23_All_Subjects_GR.db"
COURSE_TABLE = "W23_All_Atlas_Data_GR"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        sort_by = request.form.get('sort_by')
        sort_order = request.form.get('sort_order')
        limit = request.form.get('limit')
        category = request.form.get('category')
        course_level = request.form.get('course_level')
        exclude_na = request.form.get('exclude_na')
        min_grade = request.form.get('grade-letter')
        min_percent = request.form.get('grade-range')
        term_code = request.form.get('term_name')
        course_table, db_name = NAMES_TO_TABLES[term_code]
        print("creating conn to ", db_name)
        conn = query_courses.create_connection(database_name=db_name)
        print("getting deparments from ", course_table)
        departments = query_courses.get_departments(conn, course_table=course_table)
        print(course_table, db_name)

        
        # Call the query_courses function and pass in the form data
        courses, percent_results = query_courses.query_courses(conn=conn, sort_by=sort_by, ascending=sort_order, limit=limit, filter_criteria=search, category=category, course_level=course_level, exclude_na=exclude_na, min_grade=min_grade, min_percent=min_percent, course_table=course_table, database_name=db_name)
        
        # Append each course's percent results to the course object
        for i in range(len(courses)):
            # Add the percent results to the end of the tuple
            courses[i] = list(courses[i])
            courses[i].append(percent_results[i])
            if courses[i][26] == None or courses[i][26] == "" :
                courses[i][26] = 0.0 

        # Close the database connection
        query_courses.close_connection(conn)

        return render_template('index.html', courses=courses, departments=departments, min_grade=min_grade, min_percent=min_percent)
    
    else:
        # Connect to the database
        conn = query_courses.create_connection()

        # Call the query_courses function without form data to get all courses
        courses, percent_results = query_courses.query_courses(conn)
        # Close the database connection
        course_table, db_name = NAMES_TO_TABLES["W23_GR"]
        departments = query_courses.get_departments(conn, course_table=course_table)
        
        query_courses.close_connection(conn)
        for i in range(len(courses)):
            # Add the percent results to the end of the tuple
            courses[i] = list(courses[i])
            courses[i].append(percent_results[i])

        return render_template('index.html', courses=courses, departments = departments, min_grade=0, min_percent=0)

if __name__ == '__main__':
    app.run()