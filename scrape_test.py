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
TABLE_NAME = "F22_All_Courses_UG"
DB_NAME = "Atlas_Courseguide_F22_All_Subjects_UG.db"

# Funtion to get the information from a single course page
# https://atlas.ai.umich.edu/course/AAS%20115/
def scrape_course_info(course_code, number, session, cookies, headers, cursor, conn):
    
    url = 'https://atlas.ai.umich.edu/course/' + course_code + '%20' + number + '/'
    response = session.get(url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    median_grade_element = soup.find("grade-distribution")
    
    # Get Median Grade
    if median_grade_element is None:
        median_grade = "N/A"
    else:
        median_grade = median_grade_element["median-grade"]
    
    # Get Workload
    workload_element = soup.find("evaluation-card", {"class-prefix": "workload"})
    if workload_element is None:
        workload = "N/A"
    else:
        workload = workload_element[":value"]

    # Insert into database
    query = "INSERT INTO {} (department, course_number, median_grade, workload) VALUES (?, ?, ?, ?)".format(TABLE_NAME)
    cursor.execute(query, (course_code, number, median_grade, workload))
    conn.commit()

    return

def create_cookies_and_headers():
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
    cookies, headers = create_cookies_and_headers()
    soup_string = str(soup).lstrip()
    # print(soup_string)
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
    url = f'https://www.lsa.umich.edu/cg/cg_results.aspx?termArray=f_22_2420&cgtype=ug&department={subject}&allsections=true&show=999'
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

def main():
    # Create a session
    session = requests.Session()
    cookies, headers = create_cookies_and_headers()
    courses = create_course_dict(session, cookies,headers)

    # Connect to SQL database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Creat the course table
    cursor.execute("""CREATE TABLE {} (
                department text,
                course_number text,
                median_grade text,
                workload real
            )""".format(TABLE_NAME))
    # Scrape all subjects
    scrape_all_subjects(courses, session, cookies, headers, cursor, conn)
    # scrape_lsa_courseguide_subject('EECS',courses, session, cookies, headers, cursor, conn)

    conn.commit()


if __name__ == "__main__":
    main()