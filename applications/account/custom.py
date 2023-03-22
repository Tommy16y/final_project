# from django.contrib.auth import get_user_model

# User = get_user_model()

# def create_user_from_social_network(strategy, backend, user=None, *args, **kwargs):
#     if user:
#         return {'is_new': False}

#     email = kwargs['details'].get('email')
#     if not email:
#         return {'is_new': False}

#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         user = User.objects.create_user(email=email)

#     return {'is_new': True, 'user': user}
