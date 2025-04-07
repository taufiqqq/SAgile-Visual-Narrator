from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import json
from main.main import Main

class Boundary:
    def __init__(self) -> None:
        self.main = None
        self.request = None
        self.response = None
        
    def check_request(self, request) -> HttpResponseBadRequest:
        self.request = request
        
        # check if content in JSON type
        if self.request.content_type != 'application/json':
            return HttpResponseBadRequest('Invalid content type')
        
        # get user stories from request
        try:
            json_data = json.loads(self.request.body)
            userStories = json_data['user_stories']
            systemName = json_data['system_name']
            print("\n=== Request Data ===")
            print(f"User Stories: {userStories}")
            print(f"System Name: {systemName}")
            print("==================\n")
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON payload')
        
        # check if user stories in a list
        if not isinstance(userStories, list) or len(userStories) == 0:
            return HttpResponseBadRequest('Invalid payload format: user_stories need to be in a list')
        
        # check if all user stories are strings
        if not all(isinstance(item, str) for item in userStories):
            return HttpResponseBadRequest('Invalid payload format: some (or all) items in user_stories are not strings')
        
        # check if system name exists
        if not isinstance(systemName, str) or len(systemName) == 0:
            return HttpResponseBadRequest('Invalid payload format: system_name must be a string and cannot be empty')
        
        self.main = Main(userStories, systemName)
        return None
        
    def create_response(self) -> None:
        self.main.init_parsing()
        self.main.init_transform()
        
        image_data = self.main.get_image_data()
        if image_data:
            self.response = HttpResponse(image_data, content_type='image/png')
        else:
            self.response = HttpResponseBadRequest('Failed to generate image')
        
    def get_response(self) -> HttpResponse:
        return self.response