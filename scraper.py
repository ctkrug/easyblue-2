import requests

# Define your login credentials
username = "ctkrug"
password = "Mummy_0dd-ball!"

# Define the URL for the login page
login_url = 'https://weblogin.umich.edu/?cosign-shibboleth.umich.edu&https://shibboleth.umich.edu/idp/Authn/RemoteUser?conversation=e1s1'

# Start a session to persist the login across multiple requests
session = requests.Session()

# Make a GET request to the login page to get the CSRF token
response = session.get(login_url)

# Extract the CSRF token from the response
# csrf_token = response.text.split('<input type="hidden" name="_csrf" value="')[1].split('"')[0]

# Define the payload to be sent with the POST request
payload = {
    # '_csrf': csrf_token,
    'login': username,
    'password': password,
}

# Make a POST request to the login page with the payload
response = session.post(login_url, data=payload)
print(response.content)
# Check the response status code to ensure the login was successful
if response.status_code == 200:
    print('Login successful!')
else:
    print('Login failed!')
