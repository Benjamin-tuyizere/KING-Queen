from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Custom middleware to force login on all views.
    Redirects non-authenticated users to the login page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated, if not, redirect to the login page
        if not request.user.is_authenticated and not request.path.startswith(reverse('login')):
            return redirect('login')  # Redirect to login page

        response = self.get_response(request)
        return response
