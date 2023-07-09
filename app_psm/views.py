from api.boundary import Boundary
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def ucd_request(request):
    if request.method == 'POST':
        boundary = Boundary()
        
        response = boundary.check_request(request)
        
        if response is None:
            boundary.create_response()
            return boundary.get_response()
        else:
            return response
    else:
        response_data = {"message": "Invalid request method"}
        return JsonResponse(response_data, status=405)