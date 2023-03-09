import requests

from connect_teachbase import Connect_teachbase
from courser.models import Users


class Course:

    def __init__(self):
        self.connect_teachbase = Connect_teachbase()


    def get_courses(self):
        url = 'courses'

        response_json = self.requests_teachbase(url, type_r='GET')

        return response_json


    def get_course_id(self, id):
        url = f'courses/{id}'

        response_json = self.requests_teachbase(url, type_r='GET')

        return response_json


    def create_user(self, user_obj:Users):
        url = f'users/create'

        from django.core import serializers
        import json
        data_user = json.loads(serializers.serialize("json", [user_obj]))[0]

        data_user = data_user.get('fields')
        
        data = {
            "users": [
                data_user
            ],
            "external_labels": True,
            "options": {
                "activate": True,
                "verify_emails": True,
                "skip_notify_new_users": True,
                "skip_notify_active_users": True
            }
        }
        
        response_json = self.requests_teachbase(url, data, type_r='POST')

        return response_json


    def get_course_sessions(self):
        url = 'course_sessions?filter=active'
        
        response_json = self.requests_teachbase(url, type_r='GET')

        return response_json


    def course_sessions_register(self, sessions_id, user_id, email, phone):
        url = f'course_sessions/{sessions_id}/register'
        
        data = {
            "email": email,
            "phone": phone,
            "user_id": user_id
        }
        
        response_json = self.requests_teachbase(url, data, type_r='POST')

        return response_json


    def course_sessions_delete(self, sessions_id, user_id):
        data = {
            "users": [user_id],
            "session_id": sessions_id
        }
        url = f'course_sessions/{sessions_id}/remove_users'
        
        response_json = self.requests_teachbase(url, data, type_r='DELETE')

        return response_json
    

    def courses_course_id_course_sessions(self, course_id):
        '''https://go.teachbase.ru/endpoint/v1/courses/55894/course_sessions?filter=active'''

        url = f'courses/{course_id}/course_sessions?filter=active'

        response_json = self.requests_teachbase(url, type_r='GET')

        return response_json
    

    def course_sessions_id_listeners_user_id(self, id, user_id):
        '''https://go.teachbase.ru/endpoint/v1/course_sessions/495682/listeners/3903503'''

        url = f'/course_sessions/{id}/listeners/{user_id}'

        response_json = self.requests_teachbase(url, type_r='GET')

        return response_json
    

    def requests_teachbase(self, url, data = {}, type_r: str = 'get'):
        ''' стандартизировал запрос с нашей стороны '''
        
        header = self.connect_teachbase.add_tocken_in_header()

        url_teachbase = 'https://go.teachbase.ru/endpoint/v1/' + url

        if type_r == 'GET':
            response = requests.get(url_teachbase, json=data, headers=header)
        elif type_r == 'POST':
            response = requests.post(url_teachbase, json=data, headers=header)
        elif type_r == 'DELETE':
            response = requests.delete(url_teachbase, json=data, headers=header)
        else:
            print('ERROR requests_teachbase')

        return response.json()