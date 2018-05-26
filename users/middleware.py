from django.utils.deprecation import MiddlewareMixin
from .models import CustomUser


class OnlineNowMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated:
            return

        CustomUser.update_user_activity(user)
