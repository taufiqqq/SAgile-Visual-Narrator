from api.boundary import Boundary

# Create your views here.
def ucd_request(request):
    boundary = Boundary()
    
    response = boundary.check_request(request)
    
    if response is None:
        boundary.create_response()
        return boundary.get_response()
    else:
        return response