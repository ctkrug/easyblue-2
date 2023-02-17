# Author: Charles Krug
# Web Scraping -- UM Atlas and LSA Course Guide
# Date: 2/14/2023

import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import sqlite3
import random
import re 

# Global Variables
TABLE_NAME = "W23_All_Atlas_Data_test"
DB_NAME = "Atlas_Courseguide_W23_All_Subjects_UG.db"

# Funtion to get the information from a single course page
# https://atlas.ai.umich.edu/course/AAS%20115/

def process_grade_history(grade_history):
    """
    Takes in a string that is a list containing dictionaries and returns a list of the percentages for each letter grade
    """
    # Turn string that is a list containing dictionaries into a list of dictionaries
    if grade_history == "null" or grade_history == "" or grade_history == "[]" or grade_history == []:
        return [None, None, None, None, None, None, None, None, None, None, None, None, None]
    grade_history = grade_history.replace("'", '"')
    grade_history = grade_history.replace("None", "null")
    grade_history = json.loads(grade_history)
    grade_list = []
    for grade in grade_history:
        grade_list.append(grade["percent"])
    return grade_list

def scrape_course_info(course_code, number, session, cookies, headers, cursor, conn):
    """
    Scrapes the course information from the course page on Atlas and adds it to the database
    """
    print("Scraping: " + course_code + " " + number)
    url = 'https://atlas.ai.umich.edu/course/' + course_code + '%20' + number + '/'
    response = session.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
        
    # Get Course Name
    try:
        course_name = soup.find("h1", class_="text-med bold").text
    except:
        course_name = ""

    # Get Course Description    
    try:
        course_description = soup.find("div", class_="course-description").text.strip()
    except:
        course_description = ""

    # Get Credits
    try:
        credit = soup.find("p", class_="text-small").text.split(":")[1].strip()
    except:
        credit = ""

    # Get Median Grade    
    try:
        median_grade = soup.find("p", class_="grade-median").text.split(":")[1].strip()
    except:
        median_grade = ""

    # Get Prerequisites
    try:
        advisory_prerequisites = soup.find("h3", string="Advisory Prerequisites:").find_next("p").text
    except:
        advisory_prerequisites = ""

    # Get Enforced Prerequisites
    try:
        enforced_prerequisites = soup.find("h3", string="Enforced Prerequisites:").find_next("p").text
    except:
        enforced_prerequisites = ""

    # Get Evaluations
    try:
        evaluations = soup.find("div", class_="course-eval-section-container-bottom").find_all("evaluation-card")
        evaluations = [evaluation.attrs['title'] + ": " + evaluation.attrs[':value'] for evaluation in evaluations]
    except:
        evaluations = []

    # Get Grade History
    try:
        grade_history = soup.find("grade-distribution")[":grade-data"]
    except:
        grade_history = []

    # Get Student Enrollment
    try:
        student_enrollment = soup.find("student-enrollment").attrs[":enrollment-data"]
    except:
        student_enrollment = []

    # Get Workload
    try:
        workload_element = soup.find("evaluation-card", {"class-prefix": "workload"})
        if workload_element is None:
            workload = "N/A"
        else:
            workload = workload_element[":value"]
    except:
        workload = null

    # Process Grade History
    grade_list = process_grade_history(grade_history)

    # exctact grade percentages for each letter grade
    a_plus = grade_list[0]
    a = grade_list[1]
    a_minus = grade_list[2]
    b_plus = grade_list[3]
    b = grade_list[4]
    b_minus = grade_list[5]
    c_plus = grade_list[6]
    c = grade_list[7]
    c_minus = grade_list[8]
    d_plus = grade_list[9]
    d = grade_list[10]
    d_minus = grade_list[11]
    e = grade_list[12]


    # Create the query to insert into the database
    query = "INSERT INTO {} (course_code, course_name, course_description, credit, median_grade, advisory_prerequisites, enforced_prerequisites, evaluations, grade_history, student_enrollment, workload, a_plus, a, a_minus, b_plus, b, b_minus, c_plus, c, c_minus, d_plus, d, d_minus, e)"
    query = (query + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)").format(TABLE_NAME)
    # Insert into database
    try:
        cursor.execute(query, (course_code, course_name, course_description, credit, median_grade, advisory_prerequisites, enforced_prerequisites, str(evaluations), str(grade_history), str(student_enrollment), workload, a_plus, a, a_minus, b_plus, b, b_minus, c_plus, c, c_minus, d_plus, d, d_minus, e))
        conn.commit()
    except: 
        return
    return

def create_cookies_and_headers():
    """
    Creates the cookies and headers needed to scrape the data
    """
    cookies = {
        'csrftoken': 'TtQaIWGg3jqOqyeTb7J9wKWOuEBSlZl4hty555CJ2Ug7FNOlMPZLyEmfDH1jAph2',
        'sessionid': 'vlt5dhlrceoc0xeo17bhejutujpqkoc9',
        '9339e7aa273defded40dfe7e03283101': '801adb62d81e7c89608d663a3c866f8d',
        '_ga': 'GA1.2.1313871699.1676403329',
        '_gid': 'GA1.2.1349123182.1676403329',
        'saml_session': '2rm2b7nhn8pgns644j5kazb6e6upsp3b',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://atlas.ai.umich.edu/',
        'Connection': 'keep-alive',
        # 'Cookie': 'csrftoken=TtQaIWGg3jqOqyeTb7J9wKWOuEBSlZl4hty555CJ2Ug7FNOlMPZLyEmfDH1jAph2; sessionid=vlt5dhlrceoc0xeo17bhejutujpqkoc9; 9339e7aa273defded40dfe7e03283101=801adb62d81e7c89608d663a3c866f8d; _ga=GA1.2.1313871699.1676403329; _gid=GA1.2.1349123182.1676403329; saml_session=2rm2b7nhn8pgns644j5kazb6e6upsp3b',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    return cookies, headers

def process_subject_list_soup(soup):
    """
    Processes the soup object from LSA Coursguide to get the list of subjects. 
    """
    cookies, headers = create_cookies_and_headers()
    soup_string = str(soup).lstrip()

    soup_string = soup_string.split(':subjects=')[1]
    soup_string = soup_string.split('[')[1]
    soup_string = soup_string.split('], ')[0]
    soup_string = soup_string.split('" :typical-terms')[0]
    soup_string = "[" + soup_string + "]"
    soup_string = soup_string.replace("'s", 's')
    soup_string = soup_string.replace("'", '"')
    soup_string = soup_string.replace("&quot;", '"')
    return soup_string

def create_course_dict(session,cookies,headers):
        
    # Get the login page
    response = session.get('https://atlas.ai.umich.edu/courses/', cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    soup_string = process_subject_list_soup(soup)

    # Save json object to file
    courses = {}
    list_of_dicts = json.loads(soup_string)
    with open('data.json', 'w') as outfile:
        json.dump(list_of_dicts, outfile)

    # Load into dictionary
    for item in list_of_dicts:
        courses[item['code']] = item['description']
    return courses

def scrape_lsa_courseguide_subject(subject, courses, session, cookies, headers, cursor, conn):
    """
    This function scrapes LSA course guide for a given subject and semester.
    It then calls scrape_course_page for each course in the subject. (Atlas)
    """
    # Get the LSA course guide page for the subject + semester
    url = f'https://www.lsa.umich.edu/cg/cg_results.aspx?termArray=w_23_2420&cgtype=ug&department={subject}&allsections=true&show=999'
    response = session.get(url, cookies=cookies, headers=headers)
    
    # Make any whitespace in the soup into a single space
    soup = BeautifulSoup(response.content, 'html.parser')
    soup_string = str(soup)
    soup_string = re.sub(r'\s+', ' ', soup_string)

    course_pattern = re.compile(r"\b({} \d{{3}})\b".format(subject))
    scraped = []

    for match in course_pattern.finditer(soup_string):
        course = match.group(1)
        number = course.split(" ")[1]
        if number not in scraped:
            scrape_course_info(subject, number, session, cookies, headers, cursor, conn)
            scraped.append(number)

def scrape_all_subjects(courses, session, cookies, headers, cursor, conn):
    """
    This function scrapes all subjects in the LSA course guide.
    """
    for subject in courses:
        print(subject)
        scrape_lsa_courseguide_subject(subject, courses, session, cookies, headers, cursor, conn)

def make_table(cursor,conn):
    cursor.execute("""CREATE TABLE {} (
        course_code TEXT, 
        course_name TEXT PRIMARY KEY,
        course_description TEXT,
        credit TEXT,
        median_grade TEXT,
        advisory_prerequisites TEXT,
        enforced_prerequisites TEXT,
        evaluations TEXT,
        grade_history TEXT,
        student_enrollment TEXT,
        workload TEXT,
        a_plus TEXT,
        a TEXT,
        a_minus TEXT,
        b_plus TEXT,
        b TEXT,
        b_minus TEXT,
        c_plus TEXT,
        c TEXT,
        c_minus TEXT,
        d_plus TEXT,
        d TEXT,
        d_minus TEXT,
        e TEXT
        )""".format(TABLE_NAME))

def main():
    # Create a session
    session = requests.Session()
    cookies, headers = create_cookies_and_headers()
    courses = create_course_dict(session, cookies,headers)

    # Connect to SQL database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Creat the course table based on:     query = "INSERT INTO {} (course_code, course_name, course_description, credit, median_grade, advisory_prerequisites, enforced_prerequisites, evaluations, grade_history, student_enrollment, workload, a_plus, a, a_minus, b_plus, b, b_minus, c_plus, c, c_minus, d_plus, d, d_minus, e)"
    make_table(cursor, conn)
    

    # Scrape all subjects
    scrape_all_subjects(courses, session, cookies, headers, cursor, conn)
    # scrape_lsa_courseguide_subject('EECS',courses, session, cookies, headers, cursor, conn)
    # scrape_course_info('EECS', '409', session, cookies, headers, cursor, conn)
    
    conn.commit()


if __name__ == "__main__":
    main()