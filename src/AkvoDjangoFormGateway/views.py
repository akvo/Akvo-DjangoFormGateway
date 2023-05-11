from django.http import JsonResponse
from django.conf import settings
# from django.conf.settings import TWILIO_ACCOUNT_SID
# from django.conf.settings import TWILIO_AUTH_TOKEN
# credentials = f"{TWILIO_ACCOUNT_SID}{TWILIO_AUTH_TOKEN}"


def check_view(request):
    if request.method == 'GET':
        return JsonResponse({'message': settings.TWILIO_ACCOUNT_SID})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
