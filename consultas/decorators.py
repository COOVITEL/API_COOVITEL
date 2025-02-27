from django.http import JsonResponse

ALLOWED_IPS = ['']

def restrict_ip(view_func):
    def _wrapped_view(request, *args, **kwargs):
        ip = get_client_ip(request)
        if ip not in ALLOWED_IPS:
            return JsonResponse({'success': False, 'message': 'No tienes permiso para acceder a esta vista'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip