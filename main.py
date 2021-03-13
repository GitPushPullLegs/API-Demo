import api
import json


if __name__ == '__main__':
    with api.app.test_client() as client:
        route = '/schools?student_engagement_percentage=True'
        resp = client.get(route)
        data = json.loads(resp.data)
        print(json.dumps(data, indent=4, sort_keys=True))

