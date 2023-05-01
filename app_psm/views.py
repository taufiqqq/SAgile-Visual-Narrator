from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.http import FileResponse
import json
import os
from main.main import main

# Create your views here.
def ucd_request(request):
    # check if content in JSON type
    if request.content_type != 'application/json':
        return HttpResponseBadRequest('Invalid content type')
    
    # get user stories from request
    try:
        json_data = json.loads(request.body)
        userStories = json_data['user_stories']
        systemName = json_data['system_name']
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
    
    path, filename = main(userStories, systemName)
    
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plantuml_dir = os.path.join(app_dir, 'transformer', 'plantuml')
    
    filename = filename.replace('.txt', '.png')
    image_path = os.path.join(plantuml_dir, filename)
    print(image_path)
    
    file = open(image_path, 'rb')
    response = FileResponse(file, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response