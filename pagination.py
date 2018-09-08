##1--------------
students_endpoint = BASE_URL % '/courses/%s/students' % (course_id)  
  
  
# Create a request, adding the REQUEST_HEADERS to it for authentication  
not_done = True  
students = []  
url = students_endpoint  
while not_done:  
  student_request = requests.get(url,headers=REQUEST_HEADERS)  
  students+=student_request.json()  
  if 'next' in student_request.links.keys():  
    url = student.request.links['next']['href']  
  else:  
    not_done = False  
	
#2 another sample

paginated = r.json()
while 'next' in r.links:
    r = get(r.links['next']['url'])
    paginated.extend(r.json())
return paginated

#3

import requests


blueprints = []
num_blueprints = 0

headers = {'Authorization': 'Bearer ' + CANVAS_TOKEN}

url = BASE_URL + 'accounts/sis_account_id:SIS_ID_HERE/courses'
# Per page max value appears to be 100
params = {
    'blueprint': True,
    'per_page': 100
}

response = requests.get(url=url, headers=headers, params=params)
courses = response.json()

num_blueprints = num_blueprints + len(courses)
blueprints = blueprints + courses

while 'next' in response.links:
    # We don't need to include params anymore - the given 'next' URL includes previously included params
    response = requests.get(url=response.links['next']['url'], headers=headers)
    courses = response.json()

    num_blueprints = num_blueprints + len(courses)
    blueprints = blueprints + courses

print('Total blueprints:', num_blueprints)
print('Blueprints:', blueprints)

#4

I start of by declaring a data_set list where each of the JSON objects will reside.

 

data_set = []  
 

I then perform my initial API request and set the per_page limit to the max of 50.

I then save the response body to a variable called raw and use the built-in json() function to make it easier to work with.

uri = 'https://abc.instructure.com/api/v1/courses/12345/quizzes/67890/questions?per_page=50'  
r = request.get(uri, headers=headers)  
raw = r.json()  
 

I then loop through the responses and pull out each individual response and append them to the data_set list.

for question in raw:  
    data_set.append(question)  
 

For the next pages I use a while loop to repeat the above process using the links provided from the link headers of the response. As long as the current url does not equal the last url it will perform another request but using the next url as the uri to bet sent.

while r.links['current']['url'] != r.links['last']['url']:  
    r = requests.get(r.links['next']['url'], headers=headers)  
    raw = r.json()  
    for question in raw:  
        data_set.append(question)  
 
 #5
 
     def _get_paginated(self,
                       url: str,
                       headers: RequestHeaders = None,
                       params: RequestParams = None) -> Iterator[Response]:
        """
        Send an API call to the Canvas server with pagination.
        Returns a generator of response objects.
        """
        response = self._get(url, headers=headers, params=params)
        self._check_response_headers_for_pagination(response)

        yield response.json()

        while 'next' in response.links:
            response = self._get(
                response.links['next']['url'], headers=headers)
            yield response.json()

# The loop stops when they do equal each other as that denotes that all requests have been completed and there are none left, which means you have the entire data set.

#6
# Read last_page and make a get request for each page in the range:

import requests

r_sanfran = requests.get("https://api.angel.co/1/tags/1664/jobs").json()
num_pages = r_sanfran['last_page']

for page in range(2, num_pages + 1):
    r_sanfran = requests.get("https://api.angel.co/1/tags/1664/jobs", params={'page': page}).json()
    print r_sanfran['page']
    # TODO: extract the data

	
## another version
import requests

def get_jobs():
    url = "https://api.angel.co/1/tags/1664/jobs" 
    session = requests.Session()
    first_page = session.get(url).json()
    yield first_page
    num_pages = first_page['last_page']

    for page in range(2, num_pages + 1):
        next_page = session.get(url, params={'page': page}).json()
        yield next_page['page']


for page in get_jobs():
    # TODO: process the page