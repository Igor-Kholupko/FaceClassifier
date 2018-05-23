from django.utils.deprecation import MiddlewareMixin
from .models import Profile


class OnlineNowMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated:
            return

        Profile.update_user_activity(user)
