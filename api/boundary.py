from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import json
import base64
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
            # Convert image data to base64 for JSON response
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            plantuml_text = self.main.transformer.get_plantuml_text()
            plantuml_url = self.main.transformer.get_plantuml_url()
            
            # Create response with all data
            response_data = {
                'image': image_base64,
                'plantuml_text': plantuml_text,
                'plantuml_url': plantuml_url,
                'success': True
            }
            
            print("\n=== Response Data ===")
            print("Success: True")
            print(f"PlantUML Text: {plantuml_text}")
            print(f"PlantUML URL: {plantuml_url}")
            print(f"Image data length: {len(image_base64)} bytes")
            print("==================\n")
            
            self.response = JsonResponse(response_data)
        else:
            print("\n=== Response Data ===")
            print("Success: False")
            print("Error: Failed to generate image")
            print("==================\n")
            
            self.response = HttpResponseBadRequest('Failed to generate image')
        
    def get_response(self) -> HttpResponse:
        return self.response