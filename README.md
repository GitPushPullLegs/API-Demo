# API Demo

##What is this?
This is a flexible API that generates dynamic SQL queries.

##Queries:
* Group by student_id and count completed assignments ✓
* Group by course_id and average grade ✓
* Group by teacher_id and count assignments created ✓
* Group by school_id and find percentage of students with more than 1 assignment completed ✓

##Explanation
Using a lightweight framework, Flask, I've developed an API that generates new SQL queries from a sqlite database based on the client's request and responds with JSON data.

##Usage:
**Test API**
```python
"""
In the main.py file replace the route string
with the route you'd like to test.
"""

if __name__ == '__main__':
    with api.app.test_client() as client:
        route = '/schools?student_engagement_percentage=True'  # Replace me
        resp = client.get(route)
        data = json.loads(resp.data)
        print(json.dumps(data, indent=4, sort_keys=True))

# Possible paths include but are not limited to:
route = '/students?submitted_assignments=True'
route = '/courses?average_grade=True'
route = '/teachers?assignments_created=True'
route = '/schools?student_engagement_percentage=True'
```
**Terminal**
```
export FLASK_APP=api.py
flask run
```
It will provide you with an IP address that will launch a brower through which you can follow routes and receive JSON responses.