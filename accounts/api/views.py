from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import AccountsSerializer



# directly getting from api defaults bypassig the settings.py imports

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler    = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER



User = get_user_model()


class CustomAuthAPIView(APIView):
    permission_classes      = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        #print(request.user)
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)

        # APIView uses request.data insted of request.POST as the data dict
        #print(request.data)

        data = request.data
        username = data.get('username') # username or email address
        password = data.get('password')
        
        #user = authenticate(username=username, password=password)
        qs = User.objects.filter(
                Q(username__iexact=username)|
                Q(email__iexact=username)
            ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        return Response({"detail": "Invalid credentials"}, status=401)




class RegisterAPIView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountsSerializer
    queryset = User.objects.all() # queryset ta lagie lage, kon model chenar jonno



# class RegisterAPIView(APIView):
#     permission_classes      = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         #print(request.user)
#         if request.user.is_authenticated:
#             return Response({'detail': 'You are already authenticated'}, status=400)

#         # APIView uses request.data insted of request.POST as the data dict
#         #print(request.data)

#         data = request.data
#         username = data.get('username') # username or email address
#         email = data.get('email')
#         password = data.get('password')
#         password2 = data.get('password2')


#         if password != password2:
#             return Response({"detail": "Passwords Doesn't match"}, status=401)

#         #user = authenticate(username=username, password=password)
#         qs = User.objects.filter(
#                 Q(username__iexact=username)|
#                 Q(email__iexact=username)
#             ).distinct()

#         if qs.exists():
#             return Response({"detail": "User Already exists"}, status=401)
#         else:

#             if (username and len(username) > 2) and (email and len(email) > 2):
#                 user_obj = User.objects.create(username=username, email=email)
#                 user_obj.set_password(password)
#                 user_obj.save()

#                 return Response({"detail": "Thank you for Registering !!"}, status=201)

#         return Response({"detail": "Invalid credentials"}, status=401)