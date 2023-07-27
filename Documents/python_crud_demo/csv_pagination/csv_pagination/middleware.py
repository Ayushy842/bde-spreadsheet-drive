from django.shortcuts import redirect
from django.urls import reverse

def auth_middleware(get_response):
    def middleware(request):
        if request.path != '/login/' and not request.session.get('user'):
            return redirect('/login/')
        response = get_response(request)
        return response
    return middleware

    