from django.shortcuts import render


class BanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_banned:
            if not request.path.startswith('/accounts/logout'):
                return render(request, 'accounts/banned.html', status=403)
        return self.get_response(request)