from django.http import JsonResponse

def chat_room(request):
    return JsonResponse({"message": "Welcome to Chat!"})
