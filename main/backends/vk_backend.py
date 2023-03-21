from social_core.backends.vk import VKOAuth2
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomVKOAuth2(VKOAuth2):
    name = 'vk-custom'

    def get_access_token(self, *args, **kwargs):
        request = self.strategy.request
        header = JWTAuthentication().get_header(request)
        if header:
            return header.split()[1]
        return None