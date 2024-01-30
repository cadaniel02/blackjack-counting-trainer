from django.http import JsonResponse

def simple_api(request):
    data = {"message": "Hello, this is a hardcoded response!"}
    return JsonResponse(data)