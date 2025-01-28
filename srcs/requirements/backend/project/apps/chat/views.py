from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import BlockedUser, GameInvitation

def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse({
        'username': user.username,
        'email': user.email,
    })

def block_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        blocked_user_id = request.POST.get('blocked_user_id')
        BlockedUser.objects.create(user_id=user_id, blocked_user_id=blocked_user_id)
        return JsonResponse({'status': 'success'})

def send_game_invitation(request):
    if request.method == 'POST':
        sender_id = request.POST.get('sender_id')
        recipient_id = request.POST.get('recipient_id')
        GameInvitation.objects.create(sender_id=sender_id, recipient_id=recipient_id)
        return JsonResponse({'status': 'success'})