import requests
from bs4 import BeautifulSoup
import requests

def scrape_course_info(course_code):
    # url = f"https://atlas.ai.umich.edu/course/{course_code}"
    url = 'https://atlas.ai.umich.edu/accounts/login/?next=%2F'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the information you want from the page
    # ...
    course_info = soup
    return course_info

def primary_testing():
    session = requests.Session()

    # First, send a request to the website to get the login page
    login_page = session.get('https://weblogin.umich.edu/?cosign-shibboleth.umich.edu&https://shibboleth.umich.edu/idp/Authn/RemoteUser?conversation=e5s1')

    login_url = 'https://weblogin.umich.edu/?cosign-shibboleth.umich.edu&https://shibboleth.umich.edu/idp/Authn/RemoteUser?conversation=e5s1'
    r = session.get(login_url)
    ck = session.cookies.get_dict()
    print(ck)

    # Extract the necessary information from the login page
    # such as the action URL and any hidden form fields
    # (this part will vary depending on the website you are trying to authenticate to)
    # print(login_page.content)

    # Next, send a POST request to the authentication page with the username and password
    username = 'ctkrug'
    password = 'password'
    ck['login'] = username
    ck['password'] = password

    # Sent Post request

    login_response = requests.post(login_url, cookies=ck)
    print(login_response.content)

    # Finally, send requests to the protected pages using the same session
    protected_page = session.get('https://atlas.ai.umich.edu/course/AAS%20103')

    # You can now access the content of the protected page
    # print(protected_page.content)


    # Example usage
    course_codes = ['AAS%20103', 'AAS%20104']
    for course_code in course_codes:
        course_info = scrape_course_info(course_code)
        # print(course_info)
        # Do something with the course info
        # ...
primary_testing()